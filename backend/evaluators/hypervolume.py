import pandas
import sys
import numpy
from deap.tools._hypervolume import *

file=sys.argv[1]

a=pandas.read_table(file, sep=' ',names=['Ob1','Ob2'])
pareto=numpy.unique(a.values,axis=0)
print(hv.hypervolume(-1*pareto,[0,0]))
