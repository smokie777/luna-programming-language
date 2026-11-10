# Env.py

from .utils import luna_throw

class Env:
  def __init__(self, values=None, parent=None):
    self.values = {} if values is None else values
    self.parent = parent
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

  def setGlobal(self, varname, value):
    if type(varname) != str:
      luna_throw(f'varname must be str. Got: {varname}')
    did_set = False
    def run_set_global(env):
      nonlocal did_set
      if varname in env.values:
        env.values[varname] = value
        did_set = True
      if env.parent:
        run_set_global(env.parent)
    run_set_global(self)
    if not did_set:
      return self.set(varname, value)
    return value
  
  def has(self, varname):
    return varname in self.values

  def delete(self, varname):
    if self.has(varname):
      del self.values[varname]
    return None
