import numpy as np
from cec2013single.cec2013 import Benchmark


func_num = 1
bench = Benchmark()
func = bench.get_function(func_num)
print(func(np.zeros(2)))
