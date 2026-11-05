# utils.py

from luna_types import Lv
def luna_throw(message: str):
  raise Exception(f'[LUNA ERROR] {message}')

# Returns the inverse of an expression.
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
