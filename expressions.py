# expressions.py

from pydantic.dataclasses import dataclass
from luna_types import Expression, EvalExpr

# Note: pydantic dataclasses automatically handles type checking.

@dataclass
class Block(Expression):
  value: EvalExpr

@dataclass
class VarGet(Expression):
  varname: str
  
@dataclass
class VarSet(Expression):
  varname: str
  value: EvalExpr

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
  fn: EvalExpr
  args: EvalExpr

@dataclass
class SwitchBranches(Expression):
  branches: EvalExpr

@dataclass
class Switch(Expression):
  condition: EvalExpr
  cases: EvalExpr
  branches: EvalExpr
  default_branch: EvalExpr = False

@dataclass
class SwitchCall(Expression):
  switch: EvalExpr

@dataclass
class Return(Expression):
  e: EvalExpr

@dataclass
class ToBoolean(Expression):
  e: EvalExpr

@dataclass
class ToNumber(Expression):
  e: EvalExpr

@dataclass
class ToString(Expression):
  e: EvalExpr

@dataclass
class ToList(Expression):
  e: EvalExpr

@dataclass
class Inverse(Expression):
  e: EvalExpr
  
@dataclass
class Sum(Expression):
  e: EvalExpr

@dataclass
class Difference(Expression):
  e: EvalExpr

@dataclass
class Product(Expression):
  e: EvalExpr

@dataclass
class Quotient(Expression):
  e: EvalExpr

@dataclass
class All(Expression):
  e: EvalExpr

@dataclass
class Some(Expression):
  e: EvalExpr

@dataclass
class Equals(Expression):
  e: EvalExpr

@dataclass
class Lt(Expression):
  e: EvalExpr

@dataclass
class Lte(Expression):
  e: EvalExpr

@dataclass
class Gt(Expression):
  e: EvalExpr

@dataclass
class Gte(Expression):
  e: EvalExpr
