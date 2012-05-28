from pycparser import c_ast

results = []
_c = 2

prim_void = _c
prim_char = 8 * _c
prim_short = 2 * prim_char
prim_int = 2 * prim_short
prim_Bool = 2

types = {
    'void': prim_void,
    'char': prim_char,
    'short': prim_short,
    'int': prim_int,
    '_Bool': prim_Bool,
    }


class ExtDecl(c_ast.NodeVisitor):
  def __init__(self):
    self.complexities = []
  
  def visit_Decl(self, node):
    #This only works when structs are here
    if type(node.type) == c_ast.Struct:
      self.complexities.append((node.type.name, britt_metric(node)))
#    else:
#        print node.type.type

  def visit_Typedef(self, node):
    self.complexities.append((node.name, britt_metric(node)))

  def visit_FuncDef(self, node):
    self.complexities.append((node.decl.name, britt_metric(node)))

  def __str__(self):
    res = ['  %s complexity: %d' % item for item in self.complexities]
    return'\n'.join(res)


def britt_metric(ast, seen=[]):
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
    #FIXME
    try:
      return types[ast.names[0]]
    except KeyError:
      print 'KEY ERROR'
      print ast.names
      return 1
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
    return 1

