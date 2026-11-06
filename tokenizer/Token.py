# Token.py

from dataclasses import dataclass
from enum import Enum

# A Luna Token must be in one of these classifications.
# Multi-character tokens like "->" are separated into two tokens: "-" and ">"
# A variable name will be tokenized as a STRING.
class TokenType(Enum):
  TRUE = "TRUE"
  FALSE = "FALSE"
  NUMBER = "NUMBER"
  STRING = "STRING"
  IDENTIFIER = "IDENTIFIER"
  PLUS = "PLUS"
  MINUS = "MINUS"
  TIMES = "TIMES"
  DIVIDE = "DIVIDE"
  EQUALS = "EQUALS"
  PAREN_OPEN = "PAREN_OPEN"
  PAREN_CLOSE = "PAREN_CLOSE"
  CREATE_VARIABLE = "CREATE_VARIABLE"
  GREATER_THAN = "GREATER_THAN"
  LESS_THAN = "LESS THAN"

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
  ">": TokenType.GREATER_THAN,
  "<": TokenType.LESS_THAN,
}

lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
VALID_ALPHA_CHARS = set(lowercase_letters + lowercase_letters.upper())
VALID_NUMBER_CHARS = set("1234567890")
VALID_NUMBER_CHARS_WITH_PERIOD = VALID_NUMBER_CHARS | {"."}
VALID_SYMBOL_CHARS = set("`~!@#$%^&*()_+-=[]{}|;:'\",<.>/?")
VALID_WHITESPACE_CHARS = set(" \n")
VALID_CHARS = VALID_ALPHA_CHARS | VALID_NUMBER_CHARS | VALID_SYMBOL_CHARS | VALID_WHITESPACE_CHARS
VALID_KEYWORD_CHARS = set("".join(KEYWORD_TO_TOKEN_TYPE_MAP)) | VALID_ALPHA_CHARS | VALID_NUMBER_CHARS

@dataclass
class Token:
  type: TokenType
  value: str | int | float | None
  line_number: int
