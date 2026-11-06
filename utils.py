# utils.py

from luna_types import Lv
def luna_throw(message: str):
  raise Exception(f'[LUNA ERROR] {message}')

# Returns the inverse of a value.
def luna_inverse(v: Lv) -> Lv:
  match v:
    case str():
      return v[::-1]
    case bool():
      return not v
    case int() | float():
      return v * -1
    case list():
      return v[::-1]
    case _:
      luna_throw(f'can\'t call inverse on: {v}')

# Returns the falsey value associated with the given value's type
def luna_void(v: Lv) -> Lv:
  match v:
    case str():
      return ""
    case bool():
      return False
    case int() | float():
      return 0
    case list():
      return []
    case _:
      luna_throw(f'can\'t call void on: {v}')
