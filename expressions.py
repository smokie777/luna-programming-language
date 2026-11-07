# expressions.py

from pydantic.dataclasses import dataclass

# Note: pydantic dataclasses automatically handles type checking.

@dataclass
class Expression:
  pass

# a primitive value
@dataclass
class V(Expression):
  value: str | int | float | bool
  
# a list of primitive values, or a list of expressions.
@dataclass
class L(Expression):
  value: list[Expression]

# similar to L, but will evaluate to the last item in the list
@dataclass
class Block(Expression):
  value: list[Expression]

@dataclass
class VarGet(Expression):
  varname: str
  
@dataclass
class VarSet(Expression):
  varname: str
  value: Expression

@dataclass
class Function(Expression):
  args_varnames: list[str]
  block: Block
  closure: None = None  # this will be set during evaluation
  def __post_init__(self):
    if len(self.args_varnames) != len(set(self.args_varnames)):
      raise ValueError("Function argument names must be unique.")

@dataclass
class FunctionCall(Expression):
  fn: Expression
  args: Expression

@dataclass
class Return(Expression):
  e: Expression

@dataclass
class ToBoolean(Expression):
  e: Expression

@dataclass
class ToNumber(Expression):
  e: Expression

@dataclass
class ToString(Expression):
  e: Expression

@dataclass
class ToList(Expression):
  e: Expression

@dataclass
class Inverse(Expression):
  e: Expression
  
@dataclass
class Sum(Expression):
  l: list[Expression]

@dataclass
class Difference(Expression):
  l: list[Expression]

@dataclass
class Product(Expression):
  l: list[Expression]

@dataclass
class Quotient(Expression):
  l: list[Expression]

@dataclass
class All(Expression):
  l: list[Expression]

@dataclass
class Some(Expression):
  l: list[Expression]

@dataclass
class Equals(Expression):
  l: list[Expression]

@dataclass
class Switch(Expression):
  condition: object
  branches: object
