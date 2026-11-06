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
  tokens = []
  line_number = 1
  seq = ""
  state = State.DEFAULT

  def reset_state():
    nonlocal seq, state
    seq = ""
    state = State.DEFAULT

  for c in s:
    if not c in VALID_CHARS:
      raise SyntaxError(f'Invalid character: {c}')

    # "\n" increments line number
    if c == "\n":
      line_number += 1

    # all characters are allowed in a string,
    # except "'", which ends the string
    if state == State.IN_STRING:
      if c == "'":
        tokens.append(Token(TokenType.STRING, seq, line_number))
        reset_state()
        continue
      else:
        seq += c
    # only digits and "." are allowed in a number.
    # "." can only occur one time, and there must be a digit before and after it.
    # "-" will be tokenized separately.
    elif state == State.IN_NUMBER:
      if c not in VALID_NUMBER_CHARS_WITH_PERIOD:
        if c.endswith("."):
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
    # all characters are allowed in a keyword except whitespace.
    elif state == State.IN_KEYWORD:
      if c not in VALID_KEYWORD_CHARS or len(seq) > MAX_KEYWORD_LENGTH:
        raise SyntaxError(f'Invalid keyword: {seq}')
      elif seq in KEYWORD_TO_TOKEN_TYPE_MAP:
        tokens.append(KEYWORD_TO_TOKEN_TYPE_MAP[seq], None, line_number)
        reset_state()
    # in default state, either skip whitespace, or enter a valid state.
    elif state == State.DEFAULT:
      if c in VALID_WHITESPACE_CHARS:
        continue
      elif c == "'":
        state = State.IN_STRING
        continue
      elif c in VALID_NUMBER_CHARS:
        state = State.IN_NUMBER
        seq += c
      else:
        state = State.IN_KEYWORD
        seq += c

  # if at EOF and in a state, the only possible token to be made is a number.
  if state == State.IN_NUMBER:
    if c.endswith("."):
      raise SyntaxError(f'Number cannot end with ".": {seq}')
    tokens.append(Token(
      TokenType.NUMBER,
      float(seq) if state == State.IN_NUMBER_AND_IS_FLOAT else int(seq),
      line_number
    ))
    reset_state()

  # if the entire file was sucesssfully tokenized, return all the tokens.
  if state == State.DEFAULT:
    return tokens

  raise SyntaxError(f'Invalid sequence found at end of file: {seq}')
