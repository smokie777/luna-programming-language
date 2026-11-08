# luna_types.py

from pydantic.dataclasses import dataclass

@dataclass
class Expression:
  pass

LvPrimitive = str | bool | int | float
LvList = list[LvPrimitive]
Lv = LvPrimitive | LvList
EvalExpr = LvPrimitive | list | Expression
