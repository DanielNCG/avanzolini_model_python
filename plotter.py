import numpy as np
import matplotlib.pyplot as mpl


class Plotter:

    def __init__(self, init_conds, sol, obj):
        self.t = sol.t
        self.x = sol.y
        self.index = np.where((sol.t >= init_conds["Simulation initial instant (s)"]) &
                              (sol.t <= (init_conds["Simulation initial instant (s)"] +
                                         init_conds["Graph time range (s)"])))
        self.obj = obj
        self.names = [
            "Aortic Pressure (mmHg) vs Time (s)",
            "Blood Flow in Arterial Systemic Circulation (cm³/s) vs Time (s)",
            "Systemic Pressure (mmHg) vs Time (s)",
            "Blood Flow in Venous Systemic Circulation (cm³/s) vs Time (s)",
            "Right Venous-atrial Pressure (mmHg) vs Time (s)",
            "Right Ventricle Volume (cm³) vs Time (s)",
            "Pulmonary Venous Pressure (mmHg) vs Time (s)",
            "Blood Flow in Arterial Pulmonary Circulation (cm³/s) vs Time (s)",
            "Pulmonary Pressure (mmHg) vs Time (s)",
            "Blood Flow in Venous Pulmonary Circulation (cm³/s) vs Time (s)",
            "Left Venous-atrial Pressure (mmHg) vs Time (s)",
            "Left Ventricle Volume (cm³) vs Time (s)",
        ]
        self.file_names = [
            f"./graphs/aortic_pressure.png",
            f"./graphs/flow_arterial_systemic.png",
            f"./graphs/systemic_pressure.png",
            f"./graphs/flow_venous_systemic.png",
            f"./graphs/right_venousatrial_pressure.png",
            f"./graphs/right_volume.png",
            f"./graphs/pulmonary_venous_pressure.png",
            f"./graphs/flow_arterial_pulmonary.png",
            f"./graphs/pulmonary_pressure.png",
            f"./graphs/flow_venous_pulmonary.png",
            f"./graphs/left_venousatrial_pressure.png",
            f"./graphs/left_volume.png"
        ]
        self.labels = [
            "Pressure (mmHg)",
            "Blood Flow (cm³/s)",
            "Pressure (mmHg)",
            "Blood Flow (cm³/s)",
            "Pressure (mmHg)",
            "Volume (cm³)",
            "Pressure (mmHg)",
            "Blood Flow (cm³/s)",
            "Pressure (mmHg)",
            "Blood Flow (cm³/s)",
            "Pressure (mmHg)",
            "Volume (cm³)"
        ]

    def plot_loops(self):
        pressure_right = []
        pressure_left = []
        for t in self.t:
            pressure_right.append(self.obj.pressure_right_ventricle(t))
            pressure_left.append(self.obj.pressure_left_ventricle(t))
        mpl.plot(self.x[5], pressure_right)
        mpl.title("PV diagram for the right ventricle")
        mpl.ylabel("Pressure (mmHg)")
        mpl.xlabel("Volume (cm³)")
        mpl.savefig(f"./graphs/pv_diagram_right.png", transparent=False, dpi="figure", format="png")
        mpl.clf()
        mpl.plot(self.x[11], pressure_left)
        mpl.title("PV diagram for the left ventricle")
        mpl.ylabel("Pressure (mmHg)")
        mpl.xlabel("Volume (cm³)")
        mpl.savefig(f"./graphs/pv_diagram_left.png", transparent=False, dpi="figure", format="png")
        mpl.clf()
        mpl.plot(self.x[5], pressure_right)
        mpl.plot(self.x[11], pressure_left)
        mpl.title("PV diagram for both ventricles")
        mpl.ylabel("Pressure (mmHg)")
        mpl.xlabel("Volume (cm³)")
        mpl.savefig(f"./graphs/pv_diagram_both.png", transparent=False, dpi="figure", format="png")
        mpl.clf()

    def plot_time_graph(self, i):
        mpl.plot(self.t[self.index], self.x[i][self.index])
        mpl.title(self.names[i])
        mpl.ylabel(self.labels[i])
        mpl.xlabel("Time (s)")
        mpl.savefig(self.file_names[i], transparent=False, dpi="figure", format="png")
        mpl.clf()

    def plot_time_graph_all(self):

        for i in range(0, 10, 2):
            mpl.plot(self.t[self.index], self.x[i][self.index])
        mpl.ylabel("Pressure (mmHg)")
        mpl.xlabel("Time (s)")
        mpl.savefig(f"./graphs/all_pressures.png", transparent=False, dpi="figure", format="png")
        mpl.clf()

        for i in range(12):
            if np.mod(i, 2) != 0 and i != 5 and i != 11:
                mpl.plot(self.t[self.index], self.x[i][self.index])
        mpl.ylabel("Blood Flow (cm³/s)")
        mpl.xlabel("Time (s)")
        mpl.savefig(f"./graphs/all_flows.png", transparent=False, dpi="figure", format="png")
        mpl.clf()

    def plot_all(self):
        self.plot_loops()
        self.plot_time_graph_all()
        for x in range(12):
            self.plot_time_graph(x)

