# luna_tokenize.py

from .Token import *
from enum import Enum

# Luna's tokenizer is a small state machine with these valid states
class State(Enum):
  IN_NUMBER = "IN_NUMBER"
  IN_STRING = "IN_STRING"
  IN_COMMENT = "IN_COMMENT"
  IN_NUMBER_AND_IS_FLOAT = "IN_NUMBER_AND_IS_FLOAT"
  IN_KEYWORD = "IN_KEYWORD"
  DEFAULT = "DEFAULT"

# Luna's tokenizer is a small finite state machine.
# It takes a string representing the contents of a .luna file, and tokenizes it into a list of Tokens for the parser.
# tokenize() also handles lexing at the end.
def luna_tokenize(s: str) -> list[Token]:
  s += " " # adding whitespace to EOF helps tokenize numbers at EOF
  tokens = []
  line_number = 1
  seq = ""
  state = State.DEFAULT

  def reset_state():
    nonlocal seq, state
    seq = ""
    state = State.DEFAULT

  i = 0
  while i < len(s):
    c = s[i]

    # Luna only allows "keyboard chracters" in the file.
    # This means strings can only contain "keyboard characters".
    if c not in VALID_CHARS:
      raise SyntaxError(f'Invalid character: {c}')

    # single-quote ends the string
    if state == State.IN_STRING:
      if c == "'":
        tokens.append(Token(TokenType.STRING, seq, line_number))
        reset_state()
      else:
        seq += c
    elif state == State.IN_COMMENT:
      # comments do nothing. a comment ends after newline.
      if c == "\n":
        reset_state()
    # only digits and "." are allowed in a number.
    # "." can only occur one time, and there must be a digit before and after it.
    # "-" will be tokenized separately.
    elif state == State.IN_NUMBER or state == State.IN_NUMBER_AND_IS_FLOAT:
      if c in VALID_ALPHA_CHARS:
        raise SyntaxError(f'Number cannot end with a letter: {seq}{c}')
      elif c not in VALID_NUMBER_CHARS_WITH_PERIOD:
        if seq.endswith("."):
          raise SyntaxError(f'Number cannot end with ".": {seq}')
        tokens.append(Token(
          TokenType.NUMBER,
          float(seq) if state == State.IN_NUMBER_AND_IS_FLOAT else int(seq),
          line_number
        ))
        reset_state()
        continue
      elif c == ".":
        if state == State.IN_NUMBER_AND_IS_FLOAT:
          raise SyntaxError(f'Number cannot contain two ".": {seq + "."}')
        seq += c
        state = State.IN_NUMBER_AND_IS_FLOAT
      else:
        seq += c
    # a keyword can be a reserved Luna keyword, or a variable name.
    elif state == State.IN_KEYWORD:
      # single-character symbol keywords are immediately matched.
      if len(seq) == 1 and seq in KEYWORD_TO_TOKEN_TYPE_MAP:
        tokens.append(Token(KEYWORD_TO_TOKEN_TYPE_MAP.get(seq), None, line_number))
        reset_state()
        continue
      elif c in VALID_ALPHA_CHARS or c in VALID_NUMBER_CHARS:
        seq += c
      else:
        token_type = KEYWORD_TO_TOKEN_TYPE_MAP.get(seq)
        if token_type is not None:
          tokens.append(Token(token_type, None, line_number))
        else:
          tokens.append(Token(TokenType.IDENTIFIER, seq, line_number))
        reset_state()
        continue
    # in default state, either skip whitespace, or enter a valid state.
    elif state == State.DEFAULT:
      if c in VALID_WHITESPACE_CHARS:
        pass
      elif c == "#":
        state = State.IN_COMMENT
      elif c == "'":
        state = State.IN_STRING
      elif c in VALID_NUMBER_CHARS:
        state = State.IN_NUMBER
        seq += c
      elif c in VALID_KEYWORD_CHARS:
        state = State.IN_KEYWORD
        seq += c
      else:
        raise SyntaxError(f'Invalid character outside of string: {c}')

    # "\n" increments line number
    if c == "\n":
      if state != State.IN_STRING:
        tokens.append(Token(TokenType.NEWLINE, None, line_number))
      line_number += 1

    i += 1

  if state not in (State.DEFAULT, State.IN_COMMENT):
    raise SyntaxError(f'Invalid sequence found at end of file: {seq}')

  return luna_lex(tokens)

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
      and tokens[i+1].type == TokenType.GREATER_THAN
    ):
      ret.append(Token(TokenType.VARSET, None, tokens[i].line_number))
      i += 1
    else:
      ret.append(tokens[i])
    i += 1
  last_line_number = ret[-1].line_number if len(ret) else -1
  ret.append(Token(TokenType.NEWLINE, None, last_line_number + 1))
  return ret
