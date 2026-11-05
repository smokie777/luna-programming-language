# arithmetic.py

from typeutils import *
from comparisons import equals
from utils import throw

# Returns a new list or string which is the result of
# removing the sequence b from the end of a.
# Returns a if a does not end with b.
# If neither a nor b are lists or strings, a is converted into a string.
def inverse_concatenate(a, b):
  allowed_types = (str, list)
  if not isinstance(a, allowed_types) and not isinstance(b, allowed_types):
    a = to_string(a)
  (a, b) = coerce(a, b)
  if len(a) < len(b) or len(b) == 0:
    return a
  return a[:len(a)-len(b)] if equals(a[-len(b):], b) else a
  
# Returns the result of adding b to a.
# Plus is intended to be the inverse of Minus.
# numbers: addition
# strings and lists: concatenation
# booleans: convert up hierarchy to numbers
def plus(a, b):
  match a:
    case str():
      match b:
        case str() | bool() | int() | float():
          return a + to_string(b)
        case list():
          return to_list(a) + b
        case _:
          throw(f'can\'t add {b} to {a}.')
    case bool():
      match b:
        case str():
          return to_string(a) + b
        case bool():
          return to_number(a) + to_number(b)
        case int() | float():
          return to_number(a) + b
        case list():
          return to_list(a) + b
        case _:
          throw(f'can\'t add {b} to {a}.')
    case int() | float():
      match b:
        case str():
          return to_string(a) + b
        case bool() | int() | float():
          return a + to_number(b)
        case list():
          return to_list(a) + b
        case _:
          throw(f'can\'t add {b} to {a}.')
    case list():
      match b:
        case str() | bool() | int() | float():
          return a + to_list(b)
        case list():
          return a + b
        case _:
          throw(f'can\'t add {b} to {a}.')
    case _:
      throw(f'can\'t add {b} to {a}.')

# Returns the result of subtracting b from a.
# Minus is intended to be the inverse of Plus.
# numbers: subtraction
# strings and lists: inverse concatenation
# booleans: convert up hierarchy to numbers
def minus(a, b):
  match a:
    case str() | list():
      return inverse_concatenate(a, b)
    case bool():
      match b:
        case str() | list():
          return inverse_concatenate(a, b)
        case bool() | int() | float():
          return to_number(a) - to_number(b)
        case _:
          throw(f'can\'t subtract {b} from {a}.')
    case int() | float():
      match b:
        case str() | list():
          return inverse_concatenate(a, b)
        case bool() | int() | float():
          return a - to_number(b)
        case _:
          throw(f'can\'t subtract {b} from {a}.')
    case _:
      throw(f'can\'t subtract {b} from {a}.')
