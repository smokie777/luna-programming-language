# luna_types.py

from pydantic.dataclasses import dataclass

@dataclass
class Expression:
  pass

LvNum = int | float
LvPrimitive = str | bool | LvNum
LvList = list[LvPrimitive]
Lv = LvPrimitive | LvList
EvalExpr = Lv | Expression | list[Expression | Lv]
