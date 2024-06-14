import numpy as np


class Model:

    def __init__(self, params, init_cond):
        self.c1 = float(params["Aortic compliance (mmHg1 cm3)"])
        self.c2 = float(params["Arterial systemic compliance (mmHg1 cm3)"])
        self.c3 = float(params["Venous systemic compliance (mmHg1 cm3)"])
        self.c4 = float(params["Pulmonary artery compliance (mmHg1 cm3)"])
        self.c5 = float(params["Arterial pulmonary compliance (mmHg1 cm3)"])
        self.c6 = float(params["Venous pulmonary compliance (mmHg1 cm3)"])
        self.ed_l = float(params["Left elastance while diastole (mmHg cm3)"])
        self.ed_r = float(params["Right elastance while diastole (mmHg cm3)"])
        self.es_l = float(params["Left elastance while systole (mmHg cm3)"])
        self.es_r = float(params["Right elastance while systole (mmHg cm3)"])
        self.l1 = float(params["Aortic-systemic inertance (mmHg s2 cm3)"])
        self.l2 = float(params["Systemic inertance (mmHg s2 cm3)"])
        self.l3 = float(params["Pulmonary artery inertance (mmHg s2 cm3)"])
        self.l4 = float(params["Pulmonary inertance (mmHg s2 cm3)"])
        self.pipl = float(params["Left peak isovolumic pressure (mmHg)"])
        self.pipr = float(params["Right peak isovolumetric pressure (mmHg)"])
        self.r1 = float(params["Aortic valve resistance (mmHg s cm3)"])
        self.r2 = float(params["Aortic-systemic resistance (mmHg s cm3)"])
        self.r3 = float(params["Systemic resistance (mmHg s cm3)"])
        self.r4 = float(params["Tricuspid valve resistance (mmHg s cm3)"])
        self.r5 = float(params["Pulmonary valve resistance (mmHg s cm3)"])
        self.r6 = float(params["Pulmonary artery resistance (mmHg s cm3)"])
        self.r7 = float(params["Pulmonary resistance (mmHg s cm3)"])
        self.r8 = float(params["Mitral valve resistance (mmHg s cm3)"])
        self.rml = float(params["Left myo. viscosity resistance (mmHg s cm3)"])
        self.rmr = float(params["Right myo. viscosity resistance (mmHg s cm3)"])
        self.tc = float(params["Cardiac period (s)"])
        self.ti = float(init_cond["Simulation initial instant (s)"])
        self.tf = float(init_cond["Simulation final instant (s)"])
        self.x = [
            float(init_cond["Initial Aortic Pressure (mmHg)"]),
            float(init_cond["Initial Blood Flow in Arterial Systemic Circulation (cm³/s)"]),
            float(init_cond["Initial Systemic Pressure (mmHg)"]),
            float(init_cond["Initial Blood Flow in Venous Systemic Circulation (cm³/s)"]),
            float(init_cond["Initial Right Venous-atrial Pressure (mmHg)"]),
            float(init_cond["Initial Right Ventricle Volume (cm³)"]),
            float(init_cond["Initial Pulmonary Venous Pressure (mmHg)"]),
            float(init_cond["Initial Blood Flow in Arterial Pulmonary Circulation (cm³/s)"]),
            float(init_cond["Initial Pulmonary Pressure (mmHg)"]),
            float(init_cond["Initial Blood Flow in Venous Pulmonary Circulation (cm³/s)"]),
            float(init_cond["Initial Left Venous-atrial Pressure (mmHg)"]),
            float(init_cond["Initial Left Ventricle Volume (cm³)"])
        ]

    def get_time_span(self):
        span = (self.ti, self.tf)
        return span

    def activation(self, t):
        ts = 0.16 + 0.3 * self.tc
        tm = np.mod(t, self.tc)
        a = (tm < ts) * ((1 - np.cos(2 * np.pi * tm / ts)) / 2)
        return a

    def pressure_right_ventricle(self, t):
        pir = self.pipr * self.activation(t)
        return pir

    def pressure_left_ventricle(self, t):
        pil = self.pipl * self.activation(t)
        return pil

    def elastance_right_ventricle(self, t):
        er = self.ed_r + self.es_r * self.activation(t)
        return er

    def elastance_left_ventricle(self, t):
        el = self.ed_l + self.es_l * self.activation(t)
        return el

    def get(self, t, y):
        x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12 = y
        delta_p1 = self.pressure_left_ventricle(t) + x12 * self.elastance_left_ventricle(t) - x1
        delta_p2 = x5 - self.pressure_right_ventricle(t) - x6 * self.elastance_right_ventricle(t)
        delta_p3 = self.pressure_right_ventricle(t) + x6 * self.elastance_right_ventricle(t) - x7
        delta_p4 = x11 - self.pressure_left_ventricle(t) - x12 * self.elastance_left_ventricle(t)
        s1 = delta_p1 > 0
        s2 = delta_p2 > 0
        s3 = delta_p3 > 0
        s4 = delta_p4 > 0

        dx1_dt = (1 / self.c1) * (s1 * delta_p1 / (self.rml + self.r1) - x2)
        dx2_dt = (1 / self.l1) * (x1 - self.r2 * x2 - x3)
        dx3_dt = (1 / self.c2) * (x2 - x4)
        dx4_dt = (1 / self.l2) * (x3 - self.r3 * x4 - x5)
        dx5_dt = (1 / self.c3) * (x4 - (s2 * delta_p2 / self.r4))
        dx6_dt = (s2 * delta_p2 / self.r4) - ((s3 * delta_p3) / (self.rmr + self.r5))
        dx7_dt = (1 / self.c4) * (((s3 * delta_p3) / (self.rmr + self.r5)) - x8)
        dx8_dt = (1 / self.l3) * (x7 - self.r6 * x8 - x9)
        dx9_dt = (1 / self.c5) * (x8 - x10)
        dx10_dt = (1 / self.l4) * (x9 - self.r7 * x10 - x11)
        dx11_dt = (1 / self.c6) * (x10 - (s4 * delta_p4 / self.r8))
        dx12_dt = (s4 * delta_p4 / self.r8) - ((s1 * delta_p1) / (self.r1 + self.rml))

        return [dx1_dt, dx2_dt, dx3_dt, dx4_dt, dx5_dt, dx6_dt, dx7_dt, dx8_dt, dx9_dt, dx10_dt, dx11_dt, dx12_dt]
