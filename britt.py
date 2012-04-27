from pycparser import c_ast

results = []
_c = 2

prim_void = _c
prim_char = 8 * _c
prim_short = 2 * prim_char
prim_int = 2 * prim_short

types = {
    'void': prim_void,
    'char': prim_char,
    'short': prim_short,
    'int': prim_int,
    }


class ExtDecl(c_ast.NodeVisitor):
  def __init__(self):
    self.complexities = []
  
  def visit_Decl(self, node):
    #This only works when structs are here
    self.complexities.append((node.type.name, britt_metric(node)))

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
    for decl in ast.decls:
      prod *= britt_metric(decl, seen.append(ast.name))
    types[ast.name] = prod
    return prod
  else:
    print 'ast not yet defined'
    print ast
    return 1


#Not a good route to take, bname is too ambiguous
#Unfinished - decided to pursue the node visitor instead
#def britt_metric(ast):
#
#  for name, child in ast.children():
#    bname = name.rstrip('[0123456789]')
#
#    #top of the ast - contains declarations, typedefs and function defs
#    if (bname == 'ext'):
#      return britt_metric(child)
#
#    # name: the variable being declared
#    # quals: list of qualifiers (const, volatile)
#    # funcspec: list function specifiers (i.e. inline in C99)
#    # storage: list of storage specifiers (extern, register, etc.)
#    # type: declaration type (probably nested with all the modifiers)
#    # init: initialization value, or None
#    # bitsize: bit field size, or None
#    #TODO add quals, storage etc...
#    elif (bname == 'decl'):
#      return britt_metric(child)
#    elif (bname == 'type'):
#      return britt_metric(child)
#    elif (bname == '
