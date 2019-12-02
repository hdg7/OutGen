import sys
import numpy
from pycparser import parse_file, c_generator
import os

sys.path.append(os.environ["EURY_HOME"])

from backend.visitors.cVisitors import BranchIdentifier
vis=BranchIdentifier.BranchIdentifier()

filename=sys.argv[1]

ast = parse_file(filename)
print(vis.identifyLine(ast.ext[0]))
