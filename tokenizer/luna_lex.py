# luna_lex.py

from .Token import *

# lexes keyword combos into single keywords, and manages whitespace.
# example: [-, >] becomes [VarSet] instead of [Minus, GreaterThan]
# TODO: suppress newlines directly after any open brace
def luna_lex(tokens):
  ret = []
  i = 0
  while i < len(tokens):
    if (
      i < len(tokens) - 1
      and tokens[i].type == TokenType.MINUS
      and tokens[i+1].type == TokenType.GT
    ):
      ret.append(Token(TokenType.VARSET, None, tokens[i].line_number))
      i += 1
    elif (
      i < len(tokens) - 1
      and tokens[i].type == TokenType.EQUALS
      and tokens[i+1].type == TokenType.GT
    ):
      ret.append(Token(TokenType.VARSET_GLOBAL, None, tokens[i].line_number))
      i += 1
    elif (
      i < len(tokens) - 1
      and tokens[i].type == TokenType.GT
      and tokens[i+1].type == TokenType.GT
    ):
      ret.append(Token(TokenType.TERNARY_IF, None, tokens[i].line_number))
      i += 1
    elif (
      i < len(tokens) - 1
      and tokens[i].type == TokenType.EXCLAMATION
      and tokens[i+1].type == TokenType.GT
    ):
      ret.append(Token(TokenType.TERNARY_ELSE, None, tokens[i].line_number))
      i += 1
    elif (
      i < len(tokens) - 1
      and tokens[i].type == TokenType.GT
      and tokens[i+1].type == TokenType.EQUALS
    ):
      ret.append(Token(TokenType.GTE, None, tokens[i].line_number))
      i += 1
    elif (
      i < len(tokens) - 1
      and tokens[i].type == TokenType.LT
      and tokens[i+1].type == TokenType.EQUALS
    ):
      ret.append(Token(TokenType.LTE, None, tokens[i].line_number))
      i += 1
    elif (
      i < len(tokens) - 1
      and tokens[i].type == TokenType.LT
      and tokens[i+1].type == TokenType.GT
    ):
      ret.append(Token(TokenType.FREEZE, None, tokens[i].line_number))
      i += 1
    else:
      ret.append(tokens[i])
    i += 1
  last_line_number = ret[-1].line_number if len(ret) else -1
  ret.append(Token(TokenType.NEWLINE, None, last_line_number + 1))
  return ret
