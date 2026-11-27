# constants.py

from enum import StrEnum

# these keywords describe language syntax, and cannot be used as variable names
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
  IF = "if"
  ELSE = "else"
  MAP = "map"

# these keywords describe built-in function names, and can be used as variable names,
# but a warning will be printed in the console if they are.
class BuiltinKeywords(StrEnum):
  # GENERIC
  PRINT = "print"
  BOOLEAN = "boolean"
  STRING = "string"
  NUMBER = "number"
  LIST = "list"
  # LIST
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
BUILTIN_KEYWORDS_SET = { e.value for e in BuiltinKeywords }
