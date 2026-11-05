# Env.py

from utils import throw

class Env:
  def __init__(self, parent=None):
    self.values = {}
    self.parent = parent

  def get(self, varname):
    if type(varname) != str:
      throw(f'varname must be str. Got: {varname}')
    if varname in self.values:
      return self.values[varname]
    throw(f'could not find variable: {varname}')

  def set(self, varname, value):
    if type(varname) != str:
      throw(f'varname must be str. Got: {varname}')
    self.values[varname] = value
    return self.values[varname]
  