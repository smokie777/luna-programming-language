# Env.py

from utils import luna_throw

class Env:
  def __init__(self, parent=None):
    self.values = {}
    self.parent = parent

  def get(self, varname):
    if type(varname) != str:
      luna_throw(f'varname must be str. Got: {varname}')
    if varname in self.values:
      return self.values[varname]
    luna_throw(f'could not find variable: {varname}')

  def set(self, varname, value):
    if type(varname) != str:
      luna_throw(f'varname must be str. Got: {varname}')
    self.values[varname] = value
    return self.values[varname]

default_env = Env()
