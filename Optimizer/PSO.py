from pymoo.algorithms.soo.nonconvex import pso
from pymoo.optimize import minimize
from Problems import MyProblem
from cec2013_func.functions import Benchmark
from pymoo.factory import get_termination


def PSO_exe(Dim, Max_iter, NIND, func):

    obj_trace = []
    problem = MyProblem.pyProblem(Dim, func, obj_trace)
    termination = get_termination("n_gen", Max_iter)
    algorithm = pso.PSO(pop_size=NIND)
    res = minimize(problem, algorithm, termination=termination)
    return obj_trace