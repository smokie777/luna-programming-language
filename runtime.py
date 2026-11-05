# runtime.py

from utils import throw
import re

# Converts a runtime value into a boolean runtime value.
def to_boolean(v):
  match v:
    case str():
      return v != ""
    case bool():
      return v
    case int() | float():
      return v != 0
    case list():
      return v != []
    case _:
      throw(f'can\'t call to_boolean on: {v}')

# Converts a runtime value into a number (float or int) runtime value.
def to_number(v):
  match v:
    case str():
      # rules:
      # 1. only digits, -, and . are allowed.
      # 2. - must occur at index 0, or not at all.
      # 3. . can only occur once, and if so, there must be at least one digit after it.
      pattern = r"-?[0-9]+(\.[0-9]+)?"
      return (float(v) if '.' in v else int(v)) if  re.fullmatch(pattern, v) else 0
    case bool():
      return 1 if v else 0
    case int() | float():
      return v
    case list():
      return len(v)
    case _:
      throw(f'can\'t call to_number on: {v}')

# Converts a runtime value into a string runtime value.
def to_string(v):
  match v:
    case str():
      return v
    case bool():
      return "true" if v else "false"
    case int() | float():
      # NOTE: this inherits python's behavior for edge cases. may rewrite later
      return str(v)
    case list():
      return f'list{len(v)}'
    case _:
      throw(f'can\'t call to_string on: {v}')

# Converts a runtime value into a list runtime value.
def to_list(v):
  match v:
    case str() | bool() | int() | float():
      return [v]
    case list():
      return v
    case _:
      throw(f'can\'t call to_list on: {v}')
