import geatpy as ea
from Problems import MyProblem
from Optimizer import Atemplet, Wtemplet


def hybridDE_ave_exe(Dim, max_iter, NIND, func, scale_range):
    obj_trace = []
    problem = MyProblem.problem(Dim, func, scale_range, obj_trace)  # 实例化问题对象
    population = ea.Population(Encoding="RI", NIND=NIND)
    """===========================算法参数设置=========================="""
    myAlgorithm = Atemplet.soea_DE_currentToBest_1_L_templet(problem, population)
    myAlgorithm.MAXGEN = max_iter
    myAlgorithm.drawing = 0
    """=====================调用算法模板进行种群进化====================="""
    solution = ea.optimize(myAlgorithm, verbose=False, outputMsg=False, drawLog=False, saveFlag=False)
    return obj_trace


def hybridDE_w_exe(Dim, max_iter, NIND, func, scale_range):
    obj_trace = []
    problem = MyProblem.problem(Dim, func, scale_range, obj_trace)  # 实例化问题对象
    population = ea.Population(Encoding="RI", NIND=NIND)
    """===========================算法参数设置=========================="""
    myAlgorithm = Wtemplet.soea_DE_currentToBest_1_L_templet(problem, population)
    myAlgorithm.MAXGEN = max_iter
    myAlgorithm.drawing = 0
    """=====================调用算法模板进行种群进化====================="""
    solution = ea.optimize(myAlgorithm, verbose=False, outputMsg=False, drawLog=False, saveFlag=False)
    return obj_trace
