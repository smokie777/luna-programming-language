# arithmetic.py

from .luna_types import Lv
from .typeutils import *
from .equals import luna_equals
from .utils import luna_throw, luna_inverse, luna_void

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

# Repeats a list or string count times.
# If count is zero, the type of seq is set to its falsey value.
# If count is negative, seq is repeated, the inverted.
def luna_repeat_sequence(seq: list | str, count: Lv) -> list | str:
  count_int = int(luna_to_number(count))
  if count_int == 0:
    return luna_void(seq)
  abs_count_int = abs(count_int)
  result = seq * abs_count_int
  return luna_inverse(result) if count_int < 0 else result 

# Divides a list or string by another list or string, or by a count.
# If dividing by a count, returns the contiguous subsequence repeated exactly count times.
# If dividing by a list or string, returns the count that list or string is repeated.
# Division by zero is not allowed.
# Division must be clean = remainders or float counts are not allowed.
def luna_divide_sequence(seq: list | str, divisor: Lv) -> Lv:
  if luna_equals(divisor, luna_void(divisor)):
    luna_throw(f'can\'t divide by a void value: {divisor}')
  if isinstance(divisor, list | str):
    if ( # different types do not divide
      isinstance(seq, list) and isinstance(divisor, str)
      or isinstance(seq, str) and isinstance(divisor, list)
    ):
      return seq
    if len(seq) % len(divisor) != 0:
      return seq
    count = len(seq) // len(divisor)
    if luna_equals(luna_repeat_sequence(divisor, count), seq):
      return count
    inverse_divisor = luna_inverse(divisor)
    inverse_count = len(seq) // len(inverse_divisor)
    if luna_equals(luna_repeat_sequence(inverse_divisor, inverse_count), seq):
      return inverse_count * -1
    return seq
  elif isinstance(divisor, bool | int | float):
    count_int = int(luna_to_number(divisor))
    abs_count_int = abs(count_int)
    if len(seq) % abs_count_int != 0:
      return seq
    subseq = seq[:len(seq)//abs_count_int]
    if count_int < 0:
      subseq = luna_inverse(subseq)
    if luna_equals(luna_repeat_sequence(subseq, count_int), seq):
      return subseq
    return seq
  
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

# Returns the result of multiplying a with b.
# Times is intended to be the inverse of Divide.
# numbers: multiplication
# strings and lists: sequence repetition (but, list and str can't be multiplied together.)
# booleans: convert up hierarchy to numbers
def luna_times(a: Lv, b: Lv) -> Lv:
  match a:
    case str() | list():
      match b:
        case str() | list():
          luna_throw(f'can\'t multiply strings and lists together. Got: {a}*{b}')
        case bool() | int() | float():
          return luna_repeat_sequence(a, b)
        case _:
          luna_throw(f'can\'t multiply {a} with {b}.')
    case bool():
      match b:
        case str() | list():
          return b if a else luna_void(b)
        case bool() | int() | float():
          return luna_to_number(a) * luna_to_number(b)
        case _:
          luna_throw(f'can\'t multiply {a} with {b}.')
    case int() | float():
      match b:
        case str() | list():
          return luna_repeat_sequence(b, a)
        case bool() | int() | float():
          return luna_to_number(a) * luna_to_number(b)
        case _:
          luna_throw(f'can\'t multiply {a} with {b}.')
    case _:
      luna_throw(f'can\'t multiply {a} with {b}.')

# Returns the result of dividing b by a
# Divide is intended to be the inverse of Times.
# numbers: division
# strings and lists: sequence repetition count, or sequence that is repeated
# booleans: error, as Times cannot produce a boolean.
def luna_divide(a: Lv, b: Lv) -> Lv:
  if luna_equals(b, luna_void(b)):
    luna_throw(f'void divisor is not allowed: {b}')
  match a:
    case str() | list():
      return luna_divide_sequence(a, b)
    case bool():
      luna_throw(f'a boolean cannot be divided. Got: {a}')
    case int() | float():
      match b:
        case str() | list() | bool():
          return a
        case int() | float():
          return a / b
        case _:
          luna_throw(f'can\'t divide {a} by {b}.')
    case _:
      luna_throw(f'can\'t divide {a} by {b}.')
