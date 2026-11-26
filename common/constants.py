# constants.py

from enum import StrEnum

class ReservedKeywords(StrEnum):
  FALSE = "false"
  TRUE = "true"
  CONTINUE = "continue"
  RETURN = "return"
  BREAK = "break"
  FUNCTION = "function"
  F = "f"
  LOOP = "loop"
  SWITCH = "switch"
  PRINT = "print"
  BOOLEAN = "boolean"
  STRING = "string"
  NUMBER = "number"
  MAP = "map"
  IF = "if"
  ELSE = "else"
  LMAP = "lmap"
  FILTER = "filter"
  INSERT = "insert"
  POP = "pop"
  GET = "get"
  GETINDEX = "getindex"
  FIND = "find"
  FINDINDEX = "findindex"
  SLICE = "slice"
  
RESERVED_KEYWORDS_SET = { e.value for e in ReservedKeywords }
