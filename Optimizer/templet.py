# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea  # 导入geatpy库
from cmaes import CMA
import math


def individual_verify(individual, VarType, scale_range):
    Dim = len(individual)
    for i in range(Dim):
        if VarType[i] == 1:
            individual[i] = int(individual[i])
            if individual[i] < scale_range[0][i]:
                individual[i] = scale_range[0][i]
            if individual[i] > scale_range[1][i]:
                individual[i] = scale_range[1][i]
    return individual


class soea_DE_currentToBest_1_L_templet(ea.SoeaAlgorithm):
    """
soea_DE_currentToBest_1_L_templet : class - 差分进化DE/current-to-best/1/bin算法类

算法描述:
    为了实现矩阵化计算，本算法类采用打乱个体顺序来代替随机选择差分向量。算法流程如下：
    1) 初始化候选解种群。
    2) 若满足停止条件则停止，否则继续执行。
    3) 对当前种群进行统计分析，比如记录其最优个体、平均适应度等等。
    4) 采用current-to-best的方法选择差分变异的各个向量，对当前种群进行差分变异，得到变异个体。
    5) 将当前种群和变异个体合并，采用指数交叉方法得到试验种群。
    6) 在当前种群和实验种群之间采用一对一生存者选择方法得到新一代种群。
    7) 回到第2步。

参考文献:
    [1] Das, Swagatam & Suganthan, Ponnuthurai. (2011). Differential Evolution:
        A Survey of the State-of-the-Art.. IEEE Trans. Evolutionary Computation. 15. 4-31.

"""

    def __init__(self,
                 problem,
                 population,
                 MAXGEN=None,
                 MAXTIME=None,
                 MAXEVALS=None,
                 MAXSIZE=None,
                 logTras=None,
                 verbose=None,
                 outFunc=None,
                 drawing=None,
                 trappedValue=None,
                 maxTrappedCount=None,
                 dirName=None,
                 **kwargs):
        # 先调用父类构造方法
        super().__init__(problem, population, MAXGEN, MAXTIME, MAXEVALS, MAXSIZE, logTras, verbose, outFunc, drawing, trappedValue, maxTrappedCount, dirName)
        if population.ChromNum != 1:
            raise RuntimeError('传入的种群对象必须是单染色体的种群类型。')
        self.name = 'DE/current-to-best/1/L'
        if population.Encoding == 'RI':
            self.mutOper = ea.Mutde(F=0.5)  # 生成差分变异算子对象
            self.recOper = ea.Xovexp(XOVR=0.5, Half_N=True)  # 生成指数交叉算子对象，这里的XOVR即为DE中的Cr
        else:
            raise RuntimeError('编码方式必须为''RI''.')

    def run(self, prophetPop=None):  # prophetPop为先知种群（即包含先验知识的种群）
        # ==========================初始化配置===========================
        population = self.population
        NIND = population.sizes
        self.initialization()  # 初始化算法类的一些动态参数
        # ===========================准备进化============================
        population.initChrom(NIND)  # 初始化种群染色体矩阵
        # 插入先验知识（注意：这里不会对先知种群prophetPop的合法性进行检查）
        if prophetPop is not None:
            population = (prophetPop + population)[:NIND]  # 插入先知种群
        self.call_aimFunc(population)  # 计算种群的目标函数值
        population.FitnV = ea.scaling(population.ObjV, population.CV, self.problem.maxormins)  # 计算适应度
        sigma = 1.3
        # ===========================开始进化============================
        while not self.terminated(population):

            """Apply LS based on CMA-ES between best individual"""
            best_indi = np.argmax(population.FitnV)
            LS_size = int(NIND / 10)
            LSPop = ea.Population(population.Encoding, population.Field, LS_size)  # 存储LS个体
            Generator = CMA(mean=np.array(population.Chrom[best_indi]), bounds=self.problem.ranges.T, sigma=sigma,
                            population_size=LS_size + NIND)
            Phen = []
            CV = []
            ObjV = []
            solutions = []
            for _ in range(LS_size):
                x = Generator.ask()
                x = individual_verify(x, self.problem.varTypes, self.problem.ranges)
                obj, cv = self.problem.evalVars(x)
                if math.isnan(obj[0]):
                    obj = [1e10]
                Phen.append(x)
                CV.append(cv)
                ObjV.append(obj)
            LSPop.ObjV = np.array(ObjV)
            LSPop.Chrom = np.array(Phen)
            LSPop.Phen = np.array(Phen)
            LSPop.CV = -np.array(CV)
            tPop = population + LSPop
            tPop.FitnV = ea.scaling(tPop.ObjV, tPop.CV, self.problem.maxormins)  # 计算适应度
            sort_index = np.argsort(-np.array(tPop.FitnV[:, 0]))
            population = tPop[sort_index[0:NIND]]
            for i in range(LS_size + NIND):
                solutions.append((tPop.Phen[i], tPop.ObjV[i]))
            Generator.tell(solutions)
            sigma = Generator._sigma

            # 进行差分进化操作
            r0 = np.arange(NIND)
            r_best = ea.selecting('ecs', population.FitnV, NIND)  # 执行'ecs'精英复制选择
            experimentPop = ea.Population(population.Encoding, population.Field, NIND)  # 存储试验个体
            experimentPop.Chrom = self.mutOper.do(population.Encoding, population.Chrom, population.Field,
                                                  [r0, None, None, r_best, r0])  # 变异
            experimentPop.Chrom = self.recOper.do(np.vstack([population.Chrom, experimentPop.Chrom]))  # 重组
            self.call_aimFunc(experimentPop)  # 计算目标函数值
            tempPop = population + experimentPop  # 临时合并，以调用otos进行一对一生存者选择
            tempPop.FitnV = ea.scaling(tempPop.ObjV, tempPop.CV, self.problem.maxormins)  # 计算适应度
            population = tempPop[ea.selecting('otos', tempPop.FitnV, NIND)]  # 采用One-to-One Survivor选择，产生新一代种群
            population.shuffle()

        return self.finishing(population)  # 调用finishing完成后续工作并返回结果
