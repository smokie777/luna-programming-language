# Env.py

from .utils import luna_throw

# Variables can be get from parent scope if not in current scope.
# Variables will only be set in current scope.
class Env:
  def __init__(self, values=None, parent=None, is_function_scope=False):
    self.values = {} if values is None else values
    self.parent = parent
    self.is_function_scope = is_function_scope
    self.is_function_returning = False
    self.depth = 0

  def get(self, varname):
    if type(varname) != str:
      luna_throw(f'varname must be str. Got: {varname}')
    if varname in self.values:
      return self.values[varname]
    elif self.parent:
      return self.parent.get(varname)
    luna_throw(f'could not find variable: {varname}')

  def set(self, varname, value):
    if type(varname) != str:
      luna_throw(f'varname must be str. Got: {varname}')
    self.values[varname] = value
    return self.values[varname]
