# inequality.py

from .equals import luna_equals
from .luna_types import Lv
from .utils import luna_throw

# Rules for Luna inequality:
# Returns false if different types are encountered.
# List/string inequality is based on length.
# boolean inequality is: True > False.

# Returns whether a is less than b
def luna_lt(a: Lv, b: Lv) -> bool:
  match a:
    case str():
      match b:
        case str():
          return len(a) < len(b)
        case _:
          return False
    case bool():
      match b:
        case bool():
          return b and not a
        case _:
          return False
    case int() | float():
      match b:
        case bool():
          return False
        case int() | float():
          return a < b
        case _:
          return False
    case list():
      match b:
        case list():
          return len(a) < len(b)
        case _:
          return False
    case _:
      luna_throw(f'can\'t perform inequality check between: {b},{a}')


# Returns whether a is greater than b
def luna_gt(a: Lv, b: Lv) -> bool:
  return luna_lt(b, a)

# Returns whether a is less than or equal to b
def luna_lte(a: Lv, b: Lv) -> bool:
  return luna_lt(a, b) or luna_equals(a, b)

# Returns whether a is greater than or equal to b
def luna_gte(a: Lv, b: Lv) -> bool:
  return luna_lt(b, a) or luna_equals(a, b)
