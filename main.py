import scipy.integrate as sp
from model import Model
from initial_conditions import initial_conditions
from parameters import params
from plotter import Plotter


# Instantiating the model class.
obj = Model(params, initial_conditions)
# Generating the data by applying 5th order Runge-Kutta to numerically solve the model.
sol = sp.solve_ivp(obj.get, obj.get_time_span(), obj.x, atol=1e-12, rtol=1e-10, dense_output=True,
                   t_eval=obj.get_time_eval())

# Instantiating the plotter class.
plot = Plotter(initial_conditions, sol, obj)
# Plotting all the graphs.
plot.plot_all()
