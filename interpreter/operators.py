# operators.py

from enum import StrEnum

class EqualityOp(StrEnum):
  LT = "<"
  GT = ">"
  LTE = "<="
  GTE = ">="
  EQ = "="

class AdditionOp(StrEnum):
  PLUS = "+"
  MINUS = "-"

class MultiplicationOp(StrEnum):
  TIMES = "*"
  DIVIDE = "/"
  PERCENT = "%"
  