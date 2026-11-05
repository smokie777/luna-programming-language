# evl.py

from expressions import *
from runtime import *
from utils import throw
from Env import Env

default_env = Env()

def evl(expr, env = default_env):
  match expr:
    case V(v):
      return v
    case L(es):
      return [evl(e, env) for e in es]
    case VarGet(varname):
      return env.get(varname)
    case VarSet(varname, e):
      env.set(varname, evl(e, env))
      return env.get(varname)
    case ToBoolean(e):
      return to_boolean(evl(e, env))
    case ToNumber(e):
      return to_number(evl(e, env))
    case ToString(e):
      return to_string(evl(e, env))
    case ToList(e):
      return to_list(evl(e, env))
    case Inverse(e):
      return inverse(e, env)
    case Plus(e1, e2, env):
      return plus(e1, e2)
    case _:
      throw(f'can\'t evalute a non-expression: {expr}')

# Returns the inverse of an expression.
def inverse(e, env = default_env):
  v = evl(e, env)
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
      throw(f'can\'t call inverse on: {e}')

# Returns the result of adding expression e2 to expression e1.
def plus(e1, e2, env = default_env):
  v1 = evl(e1, env)
  v2 = evl(e2, env)
  match v1:
    case str():
      match v2:
        case str():
          return v1 + v2
        case bool() | int() | float():
          return v1 + to_string(v2)
        case list():
          return [v1] + v2
        case _:
          throw(f'can\'t add {e2} to {e1}.')
    case bool():
      match v2:
        case str():
          return to_string(v1) + v2
        case bool():
          # adding two booleans is nonsensical.
          # they will be converted the next-higher hierchical type
          return to_number(v1) + to_number(v2)
        case int() | float():
          return to_number(v1) + v2
        case list():
          return [v1] + v2
        case _:
          throw(f'can\'t add {e2} to {e1}.')
    case int() | float():
      match v2:
        case str():
          return to_string(v1) + v2
        case bool():
          return v1 + to_number(v2)
        case int() | float():
          return v1 + v2
        case list():
          return [v1] + v2
        case _:
          throw(f'can\'t add {e2} to {e1}.')
    case list():
      match v2:
        case str() | bool() | int() | float():
          return v1 + [v2]
        case list():
          return v1 + v2
        case _:
          throw(f'can\'t add {e2} to {e1}.')
    case _:
      throw(f'can\'t add {e2} to {e1}.')
