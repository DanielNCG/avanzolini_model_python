import numpy as np
import matplotlib.pyplot as mpl
# In this file is the definition of the Plotter class. This class uses the data provided by the simulation and plots all
# the graphs via the MatPlotLib library.


class Plotter:

    def __init__(self, init_conds, sol, obj):
        # Defining the plot parameters.
        self.t = sol.t
        self.x = sol.y
        self.index = np.where((sol.t >= init_conds["Simulation initial instant (s)"]) &
                              (sol.t <= (init_conds["Simulation initial instant (s)"] +
                                         init_conds["Graph time range (s)"])))
        self.obj = obj
        # Giving names to all graphs plotted.
        self.names = [
            "Aortic Pressure (mmHg) x Time (s)",
            "Blood Flow in Arterial Systemic Circulation (cm³/s) x Time (s)",
            "Systemic Pressure (mmHg) x Time (s)",
            "Blood Flow in Venous Systemic Circulation (cm³/s) x Time (s)",
            "Right Venous-atrial Pressure (mmHg) x Time (s)",
            "Right Ventricle Volume (cm³) x Time (s)",
            "Pulmonary Venous Pressure (mmHg) x Time (s)",
            "Blood Flow in Arterial Pulmonary Circulation (cm³/s) x Time (s)",
            "Pulmonary Pressure (mmHg) x Time (s)",
            "Blood Flow in Venous Pulmonary Circulation (cm³/s) x Time (s)",
            "Left Venous-atrial Pressure (mmHg) x Time (s)",
            "Left Ventricle Volume (cm³) x Time (s)",
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
        # Giving labels to each variable.
        self.labels = [
            "Aortic",
            "Arterial Systemic Circulation",
            "Systemic",
            "Venous Systemic Circulation",
            "Venous-atrial Pressure",
            "Right Ventricle",
            "Pulmonary Venous",
            "Arterial Pulmonary Circulation",
            "Pulmonary",
            "Venous Pulmonary Circulation",
            "Left Venous-atrial",
            "Left Ventricle"
        ]

    # This method plots all the P-V diagrams.
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
        mpl.plot(self.x[5], pressure_right, label=self.labels[5])
        mpl.plot(self.x[11], pressure_left, label=self.labels[11])
        mpl.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        mpl.title("PV diagram for both ventricles")
        mpl.ylabel("Pressure (mmHg)")
        mpl.xlabel("Volume (cm³)")
        mpl.savefig(f"./graphs/pv_diagram_both.png", transparent=False, dpi="figure", format="png",
                    bbox_inches='tight')
        mpl.clf()

    # This method plots the graph of the specified variable in relation to time.
    def plot_time_graph(self, i):
        mpl.plot(self.t[self.index], self.x[i][self.index])
        mpl.title(self.names[i])
        mpl.ylabel(self.labels[i])
        mpl.xlabel("Time (s)")
        mpl.savefig(self.file_names[i], transparent=False, dpi="figure", format="png")
        mpl.clf()

    # The plot_time_graph_all() method plots 2 graphs: the first is a graph of all pressures by time and the second
    # is a graph of all blood flows by time.
    def plot_time_graph_all(self):

        # In the following code block, there's a for loop that runs over all the even index variables (pressures).
        # Those variables are then plotted in the same graph in order to better visualize the data.
        for i in range(0, 10, 2):
            mpl.plot(self.t[self.index], self.x[i][self.index], label=self.labels[i])
        mpl.title("Pressures (mmHg) x Time (s)")
        mpl.ylabel("Pressure (mmHg)")
        mpl.xlabel("Time (s)")
        mpl.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        mpl.savefig(f"./graphs/all_pressures.png", transparent=False, dpi="figure", format="png",
                    bbox_inches='tight')
        mpl.clf()

        # In the following code block, there's a for loop that runs over all variables.
        # Then, odd index variables (blood flow), except x5 and x11 (volumes) are plotted in the same graph.
        for i in range(12):
            if np.mod(i, 2) != 0 and i != 5 and i != 11:
                mpl.plot(self.t[self.index], self.x[i][self.index], label=self.labels[i])
        mpl.title("Blood Flows (cm³/s) x Time (s)")
        mpl.ylabel("Blood Flow (cm³/s)")
        mpl.xlabel("Time (s)")
        mpl.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        mpl.savefig(f"./graphs/all_flows.png", transparent=False, dpi="figure", format="png",
                    bbox_inches='tight')
        mpl.clf()

    # The plot_all() function calls the plot_loops() and plot_time_graph_all() functions, generating its respective
    # graphs. After that, a for loop runs over all the variables to plot each one in respect to time using the
    # plot_time_graph() method.
    def plot_all(self):
        self.plot_loops()
        self.plot_time_graph_all()
        for x in range(12):
            self.plot_time_graph(x)

