import re

regex = re.compile(r'# \d+ "[-\w/\.]+" (?P<flag>\d+)')

def inString(l, s):
  for i in l:
    if i in s:
      return True
  return False

def extractCode(text):
  """
  This is a method that strips out all of the include files after a file has been preprocessed
  """
  extracted = []
  include_depth = 0
  for line in text.split('\n'):
    reg = regex.match(line)
    if reg:
      flag = reg.group('flag')
      if (flag == '1'):
        include_depth += 1
      elif (flag == '2'):
        include_depth -= 1
    if (include_depth == 0):
      extracted.append(line)
  return '\n'.join(extracted)
