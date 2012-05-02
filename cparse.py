import sys
import os

from pycparser import parse_file, c_ast, c_parser
from subprocess import Popen, PIPE
from britt import *
from utils import *

ignore_dirs = ['CVS', '.git', '.hg']
parse_files = ['c', 'C', 'h', 'H']
preprocess_directives = ['#include', '#define', '#ifdef', '#else', '#endif']


def file_walker(root):
  results = []
  for directory, dirs, files in os.walk(root):
    #remove dirs we don't need to walk
    for d in ignore_dirs:
      if d in dirs:
        dirs.remove(d)
    for f in files:
      if f.split('.')[-1] in parse_files:
        results.append(parse(os.path.join(directory, f)))
  return results

def parse(fil):
  pipe = Popen(['cpp',fil], stdout=PIPE, universal_newlines=True)
  text = pipe.communicate()[0]
  text = extractCode(text)
  parser = c_parser.CParser()
  ast = parser.parse(text)
  ed = ExtDecl()
  ed.visit(ast)
  return fil, ed

if __name__ == '__main__':
  f = sys.argv[1]
  if os.path.isdir(f):
    res = file_walker(f)
  else:
    res = [parse(f)]
  print res
  for f, r in res:
    print f
    print r


