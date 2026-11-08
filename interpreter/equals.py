# equals.py

from .luna_types import Lv

# Returns whether two values are equal.
# Different types are never equal.
# List equality is defined as: both lists have the same length,
# and the value at each index of both lists are equal.
def luna_equals(a: Lv, b: Lv) -> bool:
  match a:
    case str():
      match b:
        case str():
          return a == b
        case _:
          return False
    case bool():
      match b:
        case bool():
          return a == b
        case _:
          return False
    case int() | float():
      match b:
        case bool():
          return False
        case int() | float():
          return float(a) == float(b)
        case _:
          return False
    case list():
      match b:
        case list():
          if len(a) != len(b):
            return False
          return all([luna_equals(a[i], b[i]) for i in range(len(a))])
        case _:
          return False
    case _:
      return False
