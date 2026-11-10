# expressions.py

from pydantic.dataclasses import dataclass
from pydantic import Field
from .luna_types import Expression, EvalExpr

# Note: pydantic dataclasses automatically handles type checking.

@dataclass
class Program(Expression):
  l: list[EvalExpr]

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
class VarSetGlobal(Expression):
  varname: str
  value: EvalExpr

@dataclass
class Function(Expression):
  params: list[str]
  body: Program
  def __post_init__(self):
    if len(self.params) != len(set(self.params)):
      raise ValueError("Function argument names must be unique.")

@dataclass
class Switch(Expression):
  condition: EvalExpr
  cases: list[EvalExpr]
  branches: list[EvalExpr]
  default_branch: EvalExpr = False

@dataclass
class Loop(Expression):
  iterable: EvalExpr
  body: Program
  iterator_varname: str | None = None
  index_varname: str | None = None

@dataclass
class Return(Expression):
  e: EvalExpr

@dataclass
class Break(Expression):
  pass

@dataclass
class Continue(Expression):
  pass

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

# custom Exceptions related to Expression evaluation

@dataclass
class ReturnSignal(Exception):
  e: EvalExpr

@dataclass
class ContinueSignal(Exception):
  pass

@dataclass
class BreakSignal(Exception):
  pass
