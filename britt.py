from pycparser import c_ast
import math
from operator import itemgetter

pow2 = lambda x: 2**x
log2 = lambda x: math.log(x, 2)

_c = 1
prim_void = _c
prim_char = pow2(8)
prim_short = pow2(16)
prim_int = pow2(32)
prim_long = pow2(32)
prim_long_long = pow2(64)
prim_float = pow2(36)
prim_double = pow2(72)
prim_long_double = pow2(108)
prim_Bool = pow2(1)

"""
This is the list of all known types and their complexity.
"""
types = {
    'void': prim_void,
    'char': prim_char,
    'short': prim_short,
    'int': prim_int,
    'long': prim_long,
    'long long': prim_long_long,
    'float': prim_float,
    'double': prim_double,
    'long double': prim_long_double,
    '_Bool': prim_Bool,
    }


class ExtDecl(c_ast.NodeVisitor):
  """
  This class represents external declarators. This is where all types are
  defined, with the exception of recursive types, which are created as needed
  in the metric and added to the dict of known types when needed.
  
  It uses the node visitor convention.
  """
  def __init__(self):
    self.complexities = []
  
  def visit_Decl(self, node):
    if type(node.type) == c_ast.Struct:
      self.complexities.append((node.type.name, log2(britt_metric(node))))

  def visit_Typedef(self, node):
    self.complexities.append((node.name, log2(britt_metric(node))))

  def visit_FuncDef(self, node):
    self.complexities.append((node.decl.name, log2(britt_metric(node))))

  def __str__(self):
    res = ['  %s complexity: %f' % item for item in sorted(self.complexities, key=itemgetter(1))]
    return'\n'.join(res)


def britt_metric(ast, seen=[]):
  """
  This is where the complexity of each type is calculated.
  """
  global types
  typ = type(ast)

  if (typ == c_ast.FuncDef):
    return britt_metric(ast.decl)
  elif (typ == c_ast.Decl):
    return britt_metric(ast.type)
  elif (typ == c_ast.FuncDecl):
    prod = 0
    if ast.args:
      prod = 1
      for arg in ast.args.params or []:
        prod *= britt_metric(arg)
    return britt_metric(ast.type) + prod
  elif (typ == c_ast.TypeDecl):
    return britt_metric(ast.type)
  elif (typ == c_ast.IdentifierType):
    try:
      return types[ast.names[0]]
    except KeyError:
      print 'KEY ERROR - type not in environment'
      print ast
      raise SystemExit
  elif (typ == c_ast.ArrayDecl):
    return 2 * britt_metric(ast.type)
  elif (typ == c_ast.PtrDecl):
    return 2 * britt_metric(ast.type)
  elif (typ == c_ast.Typedef):
    score = britt_metric(ast.type)
    types[ast.name] = score
    return score
  elif (typ == c_ast.Typename):
    return britt_metric(ast.type)
  elif (typ == c_ast.Struct):
    if (ast.name in types):
      return types[ast.name]
    prod = 1
    #self referencing struct
    if ast.name in seen:
      return 2
    #empty list is for case when there is no struct body
    for decl in ast.decls or []:
      prod *= britt_metric(decl, seen.append(ast.name))
    types[ast.name] = prod
    return prod
  elif (typ == c_ast.Enum):
    return len(ast.values.enumerators)
  else:
    print 'ast not yet defined'
    print ast
    raise SystemExit
