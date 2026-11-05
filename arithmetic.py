# arithmetic.py

from luna_types import Lv
from typeutils import *
from equals import luna_equals
from utils import luna_throw

# Returns a new list or string which is the result of
# removing the sequence b from the end of a.
# Returns a if a does not end with b.
# If neither a nor b are lists or strings, a is converted into a string.
def luna_inverse_concatenate(a: Lv, b: Lv) -> Lv:
  allowed_types = (str, list)
  if not isinstance(a, allowed_types) and not isinstance(b, allowed_types):
    a = luna_to_string(a)
  (a, b) = luna_coerce(a, b)
  if len(a) < len(b) or len(b) == 0:
    return a
  return a[:len(a)-len(b)] if luna_equals(a[-len(b):], b) else a
  
# Returns the result of adding b to a.
# Plus is intended to be the inverse of Minus.
# numbers: addition
# strings and lists: concatenation
# booleans: convert up hierarchy to numbers
def luna_plus(a: Lv, b: Lv) -> Lv:
  match a:
    case str():
      match b:
        case str() | bool() | int() | float():
          return a + luna_to_string(b)
        case list():
          return luna_to_list(a) + b
        case _:
          luna_throw(f'can\'t add {b} to {a}.')
    case bool():
      match b:
        case str():
          return luna_to_string(a) + b
        case bool():
          return luna_to_number(a) + luna_to_number(b)
        case int() | float():
          return luna_to_number(a) + b
        case list():
          return luna_to_list(a) + b
        case _:
          luna_throw(f'can\'t add {b} to {a}.')
    case int() | float():
      match b:
        case str():
          return luna_to_string(a) + b
        case bool() | int() | float():
          return a + luna_to_number(b)
        case list():
          return luna_to_list(a) + b
        case _:
          luna_throw(f'can\'t add {b} to {a}.')
    case list():
      match b:
        case str() | bool() | int() | float():
          return a + luna_to_list(b)
        case list():
          return a + b
        case _:
          luna_throw(f'can\'t add {b} to {a}.')
    case _:
      luna_throw(f'can\'t add {b} to {a}.')

# Returns the result of subtracting b from a.
# Minus is intended to be the inverse of Plus.
# numbers: subtraction
# strings and lists: inverse concatenation
# booleans: convert up hierarchy to numbers
def luna_minus(a: Lv, b: Lv) -> Lv:
  match a:
    case str() | list():
      return luna_inverse_concatenate(a, b)
    case bool():
      match b:
        case str() | list():
          return luna_inverse_concatenate(a, b)
        case bool() | int() | float():
          return luna_to_number(a) - luna_to_number(b)
        case _:
          luna_throw(f'can\'t subtract {b} from {a}.')
    case int() | float():
      match b:
        case str() | list():
          return luna_inverse_concatenate(a, b)
        case bool() | int() | float():
          return a - luna_to_number(b)
        case _:
          luna_throw(f'can\'t subtract {b} from {a}.')
    case _:
      luna_throw(f'can\'t subtract {b} from {a}.')
