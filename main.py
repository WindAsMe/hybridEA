from cec2013_func.functions import Benchmark
import numpy as np
from os import path


def write_obj(data, path):
    with open(path, 'a') as f:
        f.write(str(data) + ', ')
        f.write('\n')
        f.close()


if __name__ == '__main__':
    # Dim in [2, 10, 30]
    Dim = [2, 10, 30]
    this_path = path.realpath(__file__)

    for dim in Dim:
        '''
        DE parameter initialization
        '''
        NIND = 100 * dim
        EFs = 10000 * dim
        trail = 1
        scale_range = [-100, 100]
        '''
        Benchmark initialization
        '''
        for func_num in range(1, 29):
            bench = Benchmark(dim)

            """Parameter in Y contains individual and fun_num"""
            func = bench.Y
            for i in range(trail):
                print('func: ', func_num, ' trail run: ', i+1)



