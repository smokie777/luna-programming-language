# expressions.py

from utils import throw

from dataclasses import dataclass

@dataclass
class V:
  value: str | int | float | bool
  def __post_init__(self):
    if type(self.value) not in (str, int, float, bool):
      throw(f'V may only be constructed using a primitive: str, int, float, bool. Got: {self.value}')

@dataclass
class L:
  value: list
  def __post_init__(self):
    if (
      type(self.value) != list
      or any([not isinstance(v, V) for v in self.value]) 
    ):
      throw(f'L may only be constructed as a List of V. Got: {self.value}')

@dataclass
class VarGet:
  varname: str
  def __post_init__(self):
    if type(self.varname) != str:
      throw(f'varname for VarGet may only be a string. Got: {self.varname}')

@dataclass
class VarSet:
  varname: str
  value: object
  def __post_init__(self):
    if type(self.varname) != str:
      throw(f'varname for VarSet may only be a string. Got: {self.varname}')

@dataclass
class ToBoolean:
  e: object

@dataclass
class ToNumber:
  e: object

@dataclass
class ToString:
  e: object

@dataclass
class ToList:
  e: object

@dataclass
class Inverse:
  e: object
  
@dataclass
class Plus:
  l: object

@dataclass
class Minus:
  l: object

@dataclass
class Times:
  l: object

@dataclass
class Divide:
  l: object

@dataclass
class And:
  l: object

@dataclass
class Or:
  l: object

@dataclass
class Equals:
  l: object

@dataclass
class Switch:
  condition: object
  branches: object
