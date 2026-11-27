# utils.py

from .luna_types import Lv, LvNum, LvMap
from .equals import luna_equals

def luna_throw(message: str):
  raise Exception(f'[LUNA INTERPRETER ERROR] {message}')

# Returns the inverse of a value.
def luna_inverse(v:Lv) -> Lv:
  match v:
    case str():
      return v[::-1]
    case bool():
      return not v
    case int() | float():
      return v * -1
    case list():
      return v[::-1]
    case LvMap():
      result_aa = []
      for key, value in v.aa:
        for idx, kvp in enumerate(result_aa):
          if luna_equals(value, kvp[0]):
            luna_throw(f'map can\'t have a duplicate key: {key}')
        result_aa.append([value, key])
      from .expressions import Map
      return Map(result_aa)
    case _:
      luna_throw(f'can\'t call inverse on: {v}')

# Returns the falsey value associated with the given value's type
def luna_void(v:Lv) -> Lv:
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

# Clamp a number between a min_val and a max_val
def clamp(n:LvNum, min_val:LvNum, max_val:LvNum) -> LvNum:
  return max(min_val, min(n, max_val))

# modify a list of args to have an exact number of args,
# filling in missing args with None.
def mutate_exact_num_args(args:list, exact_num_args:int, description: str) -> list:
  if len(args) > exact_num_args:
    luna_throw(f'{description} takes {exact_num_args} args, got: {len(args)}')
  while len(args) < exact_num_args:
    args.append(None)
  return args
