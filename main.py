import scipy.integrate as sp
from model import Model
from initial_conditions import initial_conditions
from parameters import params
from plotter import Plotter

obj = Model(params, initial_conditions)
sol = sp.solve_ivp(obj.get, obj.get_time_span(), obj.x, atol=1e-12, rtol=1e-10, dense_output=True)

plot = Plotter(initial_conditions, sol, obj)
plot.plot_all()
