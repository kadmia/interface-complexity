import re
import os
import sys
from subprocess import Popen, PIPE
from pycparser import c_parser, c_ast, parse_file

from britt import *
from utils import *


f = open('ps.h', 'r')

parser = c_parser.CParser()

ed = ExtDecl()

def inString(l, s):
  for i in l:
    if i in s:
      return True
  return False
