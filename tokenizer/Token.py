# Token.py

from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
  TRUE = "TRUE"
  FALSE = "FALSE"
  NUMBER = "NUMBER"
  STRING = "STRING"
  PLUS = "PLUS"
  MINUS = "MINUS"
  TIMES = "TIMES"
  DIVIDE = "DIVIDE"
  EQUALS = "EQUALS"
  PAREN_OPEN = "PAREN_OPEN"
  PAREN_CLOSE = "PAREN_CLOSE"

KEYWORD_TO_TOKEN_TYPE_MAP = {
  "(": TokenType.PAREN_OPEN,
  ")": TokenType.PAREN_CLOSE,
  "+": TokenType.PLUS,
  "-": TokenType.MINUS,
  "*": TokenType.TIMES,
  "/": TokenType.DIVIDE,
  "=": TokenType.EQUALS,
  "true": TokenType.TRUE,
  "false" : TokenType.FALSE,
}
MAX_KEYWORD_LENGTH = max([len(i) for i in KEYWORD_TO_TOKEN_TYPE_MAP])

VALID_ALPHA_CHARS = set("abcdefghijklmnopqrstuvwxyz")
VALID_NUMBER_CHARS = set("1234567890")
VALID_NUMBER_CHARS_WITH_PERIOD = VALID_NUMBER_CHARS | {"."}
VALID_SYMBOL_CHARS = set("`~!@#$%^&*()_+-=[]{}|;:'\",<.>/?")
VALID_WHITESPACE_CHARS = set(" \n")
VALID_CHARS = VALID_ALPHA_CHARS | VALID_NUMBER_CHARS | VALID_SYMBOL_CHARS | VALID_WHITESPACE_CHARS
VALID_KEYWORD_CHARS = VALID_CHARS & set("".join(KEYWORD_TO_TOKEN_TYPE_MAP))

@dataclass
class Token:
  type: TokenType
  value: str | int | float
  line_number: int
