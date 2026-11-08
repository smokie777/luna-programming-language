# expressions.py

from pydantic.dataclasses import dataclass
from pydantic import Field
from .luna_types import Expression, EvalExpr

# Note: pydantic dataclasses automatically handles type checking.

@dataclass
class Program(Expression):
  l: list[EvalExpr] # program list cannot be composed.

@dataclass
class Frozen(Expression):
  e: EvalExpr
  def __post_init__(self):
    if isinstance(self.e, Frozen):
      raise ValueError(f'Cannot Freeze an Expression that is already Frozen: {self.e}')

@dataclass
class Invoke(Expression):
  e: EvalExpr
  args: EvalExpr = Field(default_factory=list)

@dataclass
class VarGet(Expression):
  varname: str
  
@dataclass
class VarSet(Expression):
  varname: str
  value: EvalExpr

@dataclass
class Function(Expression):
  params: list[str] # dynamically generating params is not allowed
  body: Program # dynamically generating body is not allowed
  def __post_init__(self):
    if len(self.params) != len(set(self.params)):
      raise ValueError("Function argument names must be unique.")

@dataclass
class Switch(Expression):
  # dynamically generated condition is allowed.
  # dynamically generated cases/branches is not allowed,
  # as then they would be evaluated before the correct case is met.
  condition: EvalExpr
  cases: list[EvalExpr]
  branches: list[EvalExpr]
  default_branch: EvalExpr = False

@dataclass
class Return(Expression):
  e: EvalExpr

@dataclass
class Print(Expression):
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
