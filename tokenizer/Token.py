# Token.py

from dataclasses import dataclass
from enum import StrEnum

# A Luna Token must have one of these types.
# Multi-character tokens like "->" are separated into two tokens: "-" and ">"
class TokenType(StrEnum):
  NUMBER = "NUMBER"
  STRING = "STRING"
  NAME = "NAME"
  PLUS = "PLUS"
  MINUS = "MINUS"
  TIMES = "TIMES"
  DIVIDE = "DIVIDE"
  PERCENT = "PERCENT"
  EQUALS = "EQUALS"
  PAREN_OPEN = "PAREN_OPEN"
  PAREN_CLOSE = "PAREN_CLOSE"
  BRACE_OPEN = "BRACE_OPEN"
  BRACE_CLOSE = "BRACE_CLOSE"
  BRACKET_OPEN = "BRACKET_OPEN"
  BRACKET_CLOSE = "BRACKET_CLOSE"
  GT = "GT"
  LT = "LT"
  GTE = "GTE"
  LTE = "LTE"
  CARET = "CARET"
  VARSET = "VARSET"
  VARSET_GLOBAL = "VARSET_GLOBAL" 
  IF = "IF"
  ELSE = "ELSE"
  OR = "OR"
  AND = "AND"
  EXCLAMATION = "EXCLAMATION"
  NEWLINE = "NEWLINE"
  COMMA = "COMMA"
  FREEZE = "FREEZE"
  MAP = "MAP"
  BACKTICK = "BACKTICK"
  COLON = "COLON"

KEYWORD_TO_TOKEN_TYPE_MAP = {
  # single character
  "(": TokenType.PAREN_OPEN,
  ")": TokenType.PAREN_CLOSE,
  "{": TokenType.BRACE_OPEN,
  "}": TokenType.BRACE_CLOSE,
  "[": TokenType.BRACKET_OPEN,
  "]": TokenType.BRACKET_CLOSE,
  "+": TokenType.PLUS,
  "-": TokenType.MINUS,
  "*": TokenType.TIMES,
  "/": TokenType.DIVIDE,
  "%": TokenType.PERCENT,
  "^": TokenType.CARET,
  "=": TokenType.EQUALS,
  ">": TokenType.GT,
  "<": TokenType.LT,
  "|": TokenType.OR,
  "&": TokenType.AND,
  "!": TokenType.EXCLAMATION,
  ",": TokenType.COMMA,
  "`": TokenType.BACKTICK,
  ":": TokenType.COLON,
  # multi character
  "->": TokenType.VARSET,
  "=>": TokenType.VARSET_GLOBAL,
  ">>": TokenType.IF,
  "!>": TokenType.ELSE,
  ">=": TokenType.GTE,
  "<=": TokenType.LTE,
  "<>": TokenType.FREEZE
}

lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
VALID_ALPHA_CHARS = set(lowercase_letters + lowercase_letters.upper())
VALID_NUMBER_CHARS = set("1234567890")
VALID_NUMBER_CHARS_WITH_PERIOD = VALID_NUMBER_CHARS | {"."}
VALID_SYMBOL_CHARS = set(r"`~!@#$%^&*()_+-=[]{}|;:'\",<.>/?")
VALID_WHITESPACE_CHARS = set(" \n")
VALID_CHARS = VALID_ALPHA_CHARS | VALID_NUMBER_CHARS | VALID_SYMBOL_CHARS | VALID_WHITESPACE_CHARS
VALID_NAME_CHARS = set("_") | VALID_ALPHA_CHARS | VALID_NUMBER_CHARS
VALID_KEYWORD_CHARS = set("".join(KEYWORD_TO_TOKEN_TYPE_MAP)) | VALID_NAME_CHARS

@dataclass
class Token:
  type: TokenType
  value: str | int | float | None
  line_number: int
