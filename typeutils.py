# typeutils.py

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
      return to_boolean(v[0]) if len(v) else False
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
      return (float(v) if '.' in v else int(v)) if re.fullmatch(pattern, v) else 0
    case bool():
      return 1 if v else 0
    case int() | float():
      return v
    case list():
      return to_number(v[0]) if len(v) else 0
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
      return to_string(v[0]) if len(v) else ""
    case _:
      throw(f'can\'t call to_string on: {v}')

# Converts a runtime value into a list.
def to_list(v):
  match v:
    case str():
      return list(v)
    case bool() | int() | float():
      return [v]
    case list():
      return v
    case _:
      throw(f'can\'t call to_list on: {v}')

# Returns a tuple of runtime values (a, b)
# where type of b is coerced to that of a.
def _coerce_left(a, b):
   match a:
    case str():
      return (a, to_string(b))
    case bool():
      return (a, to_boolean(b))
    case int() | float():
      return (a, to_number(b))
    case list():
      return (a, b) if isinstance(b, list) else (a, to_list(b))
    case _:
      throw(f'can\'t call coerce_left on: {a}, {b}')

  
# Returns a tuple of runtime values (a, b)
# where type of a is coerced to that of b.
def _coerce_right(a, b):
  match b:
    case str():
      return (to_string(a), b)
    case bool():
      return (to_boolean(a), b)
    case int() | float():
      return (to_number(a), b)
    case list():
      return (a, b) if isinstance(a, list) else (to_list(a), b)
    case _:
      throw(f'can\'t call coerce_right on: {a}, {b}')

# Returns a tuple (a, b) where both runtime values are
# converted to the same type.
# The type to convert to is determined by the Luna type hierarchy:
# 1. List
# 2. String
# 3. Number
# 4. Boolean
# Lower types will be converted to higher types.
def coerce(a, b): 
  match a:
    case str():
      match b:
        case str() | bool() | int() | float():
          return _coerce_left(a, b)
        case list():
          return _coerce_right(a, b)
        case _:
          throw(f'can\'t coerce types of: {a} and {b}.')
    case bool():
      return _coerce_right(a, b)
    case int() | float():
      match b:
        case str() | list():
          return _coerce_right(a, b)
        case bool() | int() | float():
          return _coerce_left(a, b)
        case _:
          throw(f'can\'t coerce types of: {a} and {b}.')
    case list():
      return _coerce_left(a, b)
    case _:
      throw(f'can\'t coerce types of: {a}, {b}')
