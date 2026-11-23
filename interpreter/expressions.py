# expressions.py

from pydantic.dataclasses import dataclass
from pydantic import Field
from .luna_types import Expression, EvalExpr
from .operators import EqualityOp, AdditionOp, MultiplicationOp

# Note: pydantic dataclasses automatically handles type checking.

@dataclass
class Map(Expression):
  args: list[EvalExpr] = Field(default_factory=list)

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
  args: list[EvalExpr] = Field(default_factory=list)

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
      raise ValueError(f'Function argument names must be unique. Got: {self.params}')

@dataclass
class Switch(Expression):
  condition: EvalExpr
  cases: list[EvalExpr]
  branches: list[EvalExpr]
  default_branch: EvalExpr | None = None
  def __post_init__(self):
    if len(self.cases) != len(self.branches):
      raise ValueError(f'Switch number of cases and branches must be equal. Got: {len(self.cases)} cases, {len(self.branches)} branches')

@dataclass
class SwitchCatchAllCase(Expression):
  pass

@dataclass
class IfThenElse(Expression):
  condition: EvalExpr
  if_branch: EvalExpr | None
  else_branch: EvalExpr | None

@dataclass
class Loop(Expression):
  iterable: EvalExpr
  iterator_varname: str | None
  index_varname: str | None
  body: Program

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
class All(Expression):
  items: list[EvalExpr]

@dataclass
class Some(Expression):
  items: list[EvalExpr]

def validate_chain(items, operators, chain_type):
  if len(items) < 2 or len(operators) + 1 != len(items):
    raise ValueError(f"{chain_type} must have n items and n - 1 operators, where n >= 2. Got: {len(items)} items, {len(operators)} operators.")

@dataclass
class EqualityChain(Expression):
  items: list[EvalExpr]
  operators: list[EqualityOp]
  def __post_init__(self):
    validate_chain(self.items, self.operators, "EqualityChain")

@dataclass
class AdditionChain(Expression):
  items: list[EvalExpr]
  operators: list[AdditionOp]
  def __post_init__(self):
    validate_chain(self.items, self.operators, "AdditionChain")

@dataclass
class MultiplicationChain(Expression):
  items: list[EvalExpr]
  operators: list[MultiplicationOp]
  def __post_init__(self):
    validate_chain(self.items, self.operators, "MultiplicationChain")

@dataclass
class Exponent(Expression):
  items: list[EvalExpr]

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

# helpers to generatee expressions, only to be used during testing.

def Sum(l: list[EvalExpr]):
  return AdditionChain(l, [AdditionOp.PLUS for _ in range(len(l) - 1)])

def Difference(l: list[EvalExpr]):
  return AdditionChain(l, [AdditionOp.MINUS for _ in range(len(l) - 1)])

def Product(l: list[EvalExpr]):
  return MultiplicationChain(l, [MultiplicationOp.TIMES for _ in range(len(l) - 1)])

def Quotient(l: list[EvalExpr]):
  return MultiplicationChain(l, [MultiplicationOp.DIVIDE for _ in range(len(l) - 1)])

def RemainderAll(l: list[EvalExpr]):
  return MultiplicationChain(l, [MultiplicationOp.PERCENT for _ in range(len(l) - 1)])

def Lt(l: list[EvalExpr]):
  return EqualityChain(l, [EqualityOp.LT for _ in range(len(l) - 1)])

def Lte(l: list[EvalExpr]):
  return EqualityChain(l, [EqualityOp.LTE for _ in range(len(l) - 1)])

def Gt(l: list[EvalExpr]):
  return EqualityChain(l, [EqualityOp.GT for _ in range(len(l) - 1)])

def Gte(l: list[EvalExpr]):
  return EqualityChain(l, [EqualityOp.GTE for _ in range(len(l) - 1)])

def Equals(l: list[EvalExpr]):
  return EqualityChain(l, [EqualityOp.EQ for _ in range(len(l) - 1)])
