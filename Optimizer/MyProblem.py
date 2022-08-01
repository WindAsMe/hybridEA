import geatpy as ea
import numpy as np


class Problem(ea.Problem):

    def __init__(self, Dim, benchmark, scale_range, obj_trace, VarType):
        name = 'MyProblem'
        M = 1
        maxormins = [1]
        self.Dim = Dim
        varTypes = VarType
        lb = scale_range[0]
        ub = scale_range[1]
        lbin = [1] * self.Dim
        ubin = [1] * self.Dim
        self.benchmark = benchmark
        self.obj_trace = obj_trace
        ea.Problem.__init__(self, name, M, maxormins, self.Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数，pop为传入的种群对象
        Obj = []
        Cons = []

        for p in pop.Phen:
            obj, cons = self.benchmark(p)
            Obj.append(obj)
            Cons.append(cons)
        pop.ObjV = np.array(Obj)
        pop.CV = -np.array(Cons)
        pop.FitV = ea.scaling(pop.ObjV, pop.CV, self.maxormins)
        self.obj_trace.append(Obj[np.argmax(pop.FitV)])

    def evalVars(self, Vars):
        return self.benchmark(Vars)

