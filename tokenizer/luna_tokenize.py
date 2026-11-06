# luna_tokenize.py

from .Token import *
from enum import Enum

# Luna's tokenizer is a small state machine with these valid states
class State(Enum):
  IN_NUMBER = "IN_NUMBER"
  IN_STRING = "IN_STRING"
  IN_NUMBER_AND_IS_FLOAT = "IN_NUMBER_AND_IS_FLOAT"
  IN_KEYWORD = "IN_KEYWORD"
  DEFAULT = "DEFAULT"

# Takes a string which represents the text contents of a .luna file,
# and returns a list of Tokens for the parser.
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
      line_number += 1

    i += 1

  # if the entire file was sucesssfully tokenized, return all the tokens.
  if state == State.DEFAULT:
    return tokens

  raise SyntaxError(f'Invalid sequence found at end of file: {seq}')
