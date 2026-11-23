# constants.py

from enum import StrEnum

class ReservedKeywords(StrEnum):
  FALSE = "false"
  TRUE = "true"
  CONTINUE = "continue"
  RETURN = "return"
  BREAK = "break"
  FUNCTION = "function"
  LOOP = "loop"
  SWITCH = "switch"
  PRINT = "print"
  BOOLEAN = "boolean"
  STRING = "string"
  NUMBER = "number"
  MAP = "map"
  IF = "if"
  ELSE = "else"
RESERVED_KEYWORDS_SET = { e.value for e in ReservedKeywords }
