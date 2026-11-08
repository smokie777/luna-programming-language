# typeutils.py

from .luna_types import Lv
from .utils import luna_throw
import re

# In Luna, all values can be freely converted across types.
# Additionally, all falsey values can be freely converted between one another.
# Falsey values are: False, 0, "", [].

# Converts a runtime value into a boolean runtime value.
def luna_to_boolean(v: Lv) -> bool:
  match v:
    case str():
      return v != ""
    case bool():
      return v
    case int() | float():
      return v != 0
    case list():
      # ideally, the user would specify a reduction like "and" or "or" instead.
      # but, this case is needed so "and" and "or" don't throw or recurse for nested arrays. 
      return len(v) != 0 
    case _:
      luna_throw(f'can\'t call luna_to_boolean on: {v}')

# Converts a runtime value into a number (float or int) runtime value.
def luna_to_number(v: Lv) -> int | float:
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
      luna_throw(f'can\'t call luna_to_number on list {v}. use a reduction like "sum" instead.')
    case _:
      luna_throw(f'can\'t call luna_to_number on: {v}')

# Converts a runtime value into a string runtime value.
def luna_to_string(v: Lv) -> str:
  match v:
    case str():
      return v
    case bool():
      return "true" if v else ""
    case int() | float():
      # NOTE: this inherits python's behavior for edge cases. may rewrite later
      return str(v)
    case list():
      luna_throw(f'can\'t call luna_to_string on list {v}. use a reduction like "join" instead.')
    case _:
      luna_throw(f'can\'t call luna_to_string on: {v}')

# Converts a runtime value into a list.
def luna_to_list(v: Lv) -> list[Lv]:
  match v:
    case str():
      return list(v)
    case bool():
      return [v] if v else []
    case int() | float():
      return [v]
    case list():
      return v
    case _:
      luna_throw(f'can\'t call luna_to_list on: {v}')

# Returns a tuple of runtime values (a, b)
# where type of b is coerced to that of a.
def _luna_coerce_left(a: Lv, b: Lv) -> Lv:
   match a:
    case str():
      return (a, luna_to_string(b))
    case bool():
      return (a, luna_to_boolean(b))
    case int() | float():
      return (a, luna_to_number(b))
    case list():
      return (a, b) if isinstance(b, list) else (a, luna_to_list(b))
    case _:
      luna_throw(f'can\'t call coerce_left on: {a}, {b}')

  
# Returns a tuple of runtime values (a, b)
# where type of a is coerced to that of b.
def _luna_coerce_right(a: Lv, b: Lv) -> Lv:
  match b:
    case str():
      return (luna_to_string(a), b)
    case bool():
      return (luna_to_boolean(a), b)
    case int() | float():
      return (luna_to_number(a), b)
    case list():
      return (a, b) if isinstance(a, list) else (luna_to_list(a), b)
    case _:
      luna_throw(f'can\'t call coerce_right on: {a}, {b}')

# Returns a tuple (a, b) where both runtime values are
# converted to the same type.
# The type to convert to is determined by the Luna type hierarchy:
# 1. List
# 2. String
# 3. Number
# 4. Boolean
# Lower types will be converted to higher types.
def luna_coerce(a: Lv, b: Lv) -> Lv: 
  match a:
    case str():
      match b:
        case str() | bool() | int() | float():
          return _luna_coerce_left(a, b)
        case list():
          return _luna_coerce_right(a, b)
        case _:
          luna_throw(f'can\'t coerce types of: {a} and {b}.')
    case bool():
      return _luna_coerce_right(a, b)
    case int() | float():
      match b:
        case str() | list():
          return _luna_coerce_right(a, b)
        case bool() | int() | float():
          return _luna_coerce_left(a, b)
        case _:
          luna_throw(f'can\'t coerce types of: {a} and {b}.')
    case list():
      return _luna_coerce_left(a, b)
    case _:
      luna_throw(f'can\'t coerce types of: {a}, {b}')
