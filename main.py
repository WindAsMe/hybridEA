from cec2013_func.functions import Benchmark
import numpy as np
from os import path
from Optimizer import CMAES, DE, ES, GA, PSO, hybridDE, Wtemplet, RS


def write_obj(data, path):
    with open(path, 'a') as f:
        f.write(str(data) + ', ')
        f.write('\n')
        f.close()


if __name__ == '__main__':
    Dim = [2, 5, 10]
    this_path = path.realpath(__file__)

    for dim in Dim:
        '''
        DE parameter initialization
        '''
        NIND = 50 * dim
        FEs = 1000 * dim
        trial = 30
        lb, ub = -100, 100
        scale_range = []
        for i in range(dim):
            scale_range.append([lb, ub])
        '''
        Benchmark initialization
        '''
        for func_num in range(1, 29):
            bench = Benchmark(dim)

            """Parameter in Y contains individual and fun_num"""

            CMAES_obj_path = path.dirname(this_path) + '/data/CMAES/' + str(dim) + 'D/f' + str(func_num)
            DE_obj_path = path.dirname(this_path) + '/data/DE/' + str(dim) + 'D/f' + str(func_num)
            ES_obj_path = path.dirname(this_path) + '/data/ES/' + str(dim) + 'D/f' + str(func_num)
            GA_obj_path = path.dirname(this_path) + '/data/GA/' + str(dim) + 'D/f' + str(func_num)
            PSO_obj_path = path.dirname(this_path) + '/data/PSO/' + str(dim) + 'D/f' + str(func_num)
            RS_obj_path = path.dirname(this_path) + '/data/RS/' + str(dim) + 'D/f' + str(func_num)
            hybridDE_ave_obj_path = path.dirname(this_path) + '/data/hybridDE_a/' + str(dim) + 'D/f' + str(func_num)
            hybridDE_w_obj_path = path.dirname(this_path) + '/data/hybridDE_w/' + str(dim) + 'D/f' + str(func_num)

            func = bench.Y
            Max_iter = int(FEs / NIND)
            for i in range(trial):
                print('func: ', func_num, ' trail run: ', i+1)

                # """CMA-ES optimization"""
                # CMAES_trace = CMAES.CMAES_exe(dim, Max_iter, NIND, func, scale_range)
                # write_obj(CMAES_trace, CMAES_obj_path)
                #
                # """DE optimization"""
                # DE_trace = DE.DE_exe(dim, Max_iter, NIND, func, scale_range)
                # write_obj(DE_trace, DE_obj_path)
                #
                # """ES optimization"""
                # ES_trace = ES.ES_exe(dim, Max_iter, NIND, func, scale_range)
                # write_obj(ES_trace, ES_obj_path)
                #
                # """GA optimization"""
                # GA_trace = GA.GA_exe(dim, Max_iter, NIND, func, scale_range)
                # write_obj(GA_trace, GA_obj_path)

                """PSO optimization"""
                # PSO_trace = PSO.PSO_exe(dim, Max_iter, NIND, func)
                # write_obj(PSO_trace, PSO_obj_path)

                """RS optimization"""
                RS_trace = RS.RS_exe(dim, Max_iter, NIND, func)
                write_obj(RS_trace, RS_obj_path)

                # """hybridDE_a with averaging optimization"""
                # hybridDE_ave_trace = hybridDE.hybridDE_ave_exe(dim, Max_iter, NIND, func, scale_range)
                # write_obj(hybridDE_ave_trace, hybridDE_ave_obj_path)
                #
                # """hybridDE_a with weighting optimization"""
                # hybridDE_w_trace = hybridDE.hybridDE_w_exe(dim, Max_iter, NIND, func, scale_range)
                # write_obj(hybridDE_w_trace, hybridDE_w_obj_path)



