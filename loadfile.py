import re
import os
import sys
from subprocess import Popen, PIPE
from pycparser import c_parser, c_ast, parse_file

from britt import *
from utils import *


#f = open('ps.h', 'r')

parser = c_parser.CParser()

ed = ExtDecl()

pipe = Popen(['cpp', '/Users/adam/programming/openbsd/src/sys/kern/clock_subr.c'], stdout=PIPE, universal_newlines=True)
text = pipe.communicate()[0]
#ast = parser.parse(text)
