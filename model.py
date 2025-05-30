import numpy as np
# In this file is the definition of the Model class in which is the cardiovascular model.


class Model:

    # Defining the parameters and initial conditions
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
        self.p0l = float(params["Left peak isovolumic pressure (mmHg)"])
        self.p0r = float(params["Right peak isovolumetric pressure (mmHg)"])
        self.r1 = float(params["Aortic valve resistance (mmHg s cm3)"])
        self.r2 = float(params["Aortic-systemic resistance (mmHg s cm3)"])
        self.r3 = float(params["Systemic resistance (mmHg s cm3)"])
        self.r4 = float(params["Tricuspid valve resistance (mmHg s cm3)"])
        self.r5 = float(params["Pulmonary valve resistance (mmHg s cm3)"])
        self.r6 = float(params["Pulmonary artery resistance (mmHg s cm3)"])
        self.r7 = float(params["Pulmonary resistance (mmHg s cm3)"])
        self.r8 = float(params["Mitral valve resistance (mmHg s cm3)"])
        self.rl = float(params["Left myo. viscosity resistance (mmHg s cm3)"])
        self.rr = float(params["Right myo. viscosity resistance (mmHg s cm3)"])
        self.tc = float(params["Cardiac period (s)"])
        self.ti = float(init_cond["Simulation initial instant (s)"])
        self.tf = float(init_cond["Simulation final instant (s)"])
        self.reflux = float(params["Aortic reflux (%)"])
        self.number_of_points = int(init_cond["Number of points in simulation"])
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

    # Defining a method that returns the time span required by the Scipy.Integrate PVI solver.
    def get_time_span(self):
        span = (self.ti, self.tf)
        return span

    def get_time_eval(self):
        span = np.linspace(self.ti, self.tf, self.number_of_points)
        return span

    # Defining the activation function that represents the cardiac cycle in the model.
    def activation(self, t):
        ts = 0.16 + 0.3 * self.tc
        tm = np.mod(t, self.tc)
        a = (tm < ts) * ((1 - np.cos(2 * np.pi * tm / ts)) / 2)
        return a

    # Defining a method that returns the pressure in the right ventricle at any given time.
    def pressure_right_ventricle(self, t):
        pr = self.p0r * self.activation(t)
        return pr

    # Defining a method that returns the pressure in the left ventricle at any given time.
    def pressure_left_ventricle(self, t):
        pl = self.p0l * self.activation(t)
        return pl

    # Defining a method that returns the right ventricle's elastance at any given time.
    def elastance_right_ventricle(self, t):
        er = self.ed_r + self.es_r * self.activation(t)
        return er

    # Defining a method that returns the left ventricle's elastance at any given time.
    def elastance_left_ventricle(self, t):
        el = self.ed_l + self.es_l * self.activation(t)
        return el

    # The following method returns the 12 coupled differential equations that describes the cardiovascular model.
    def get(self, t, y):
        x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12 = y
        # This block of code defines the functions that govern the heart valves, represented by the diodes in the model.
        delta_p1 = self.pressure_left_ventricle(t) + x12 * self.elastance_left_ventricle(t) - x1
        delta_p2 = x5 - self.pressure_right_ventricle(t) - x6 * self.elastance_right_ventricle(t)
        delta_p3 = self.pressure_right_ventricle(t) + x6 * self.elastance_right_ventricle(t) - x7
        delta_p4 = x11 - self.pressure_left_ventricle(t) - x12 * self.elastance_left_ventricle(t)
        s1 = (delta_p1 > 0) - self.reflux
        s2 = delta_p2 > 0
        s3 = delta_p3 > 0
        s4 = delta_p4 > 0

        # The 12 differential equations are then laid out explicitly and then returned by the function get().
        dx1_dt = (1 / self.c1) * (s1 * delta_p1 / (self.rl + self.r1) - x2)
        dx2_dt = (1 / self.l1) * (x1 - self.r2 * x2 - x3)
        dx3_dt = (1 / self.c2) * (x2 - x4)
        dx4_dt = (1 / self.l2) * (x3 - self.r3 * x4 - x5)
        dx5_dt = (1 / self.c3) * (x4 - (s2 * delta_p2 / self.r4))
        dx6_dt = (s2 * delta_p2 / self.r4) - ((s3 * delta_p3) / (self.rr + self.r5))
        dx7_dt = (1 / self.c4) * (((s3 * delta_p3) / (self.rr + self.r5)) - x8)
        dx8_dt = (1 / self.l3) * (x7 - self.r6 * x8 - x9)
        dx9_dt = (1 / self.c5) * (x8 - x10)
        dx10_dt = (1 / self.l4) * (x9 - self.r7 * x10 - x11)
        dx11_dt = (1 / self.c6) * (x10 - (s4 * delta_p4 / self.r8))
        dx12_dt = (s4 * delta_p4 / self.r8) - ((s1 * delta_p1) / (self.r1 + self.rl))

        return [dx1_dt, dx2_dt, dx3_dt, dx4_dt, dx5_dt, dx6_dt, dx7_dt, dx8_dt, dx9_dt, dx10_dt, dx11_dt, dx12_dt]
