# luna_types.py

from pydantic.dataclasses import dataclass

@dataclass
class Expression:
  pass

@dataclass
class LvMap(Expression):
  pass

type LvNum = int | float
type LvPrimitive = str | bool | LvNum
type Lv = LvPrimitive | list[Lv] | LvMap
type EvalExpr = Lv | Expression | list[EvalExpr]
