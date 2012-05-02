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

pipe = Popen(['cpp', 'testfiles/helloworld.c'], stdout=PIPE, universal_newlines=True)
text = pipe.communicate()[0]
