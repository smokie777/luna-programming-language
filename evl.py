# evl.py

from expressions import *
from typeutils import *
from arithmetic import plus, minus
from utils import throw
from Env import default_env

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
    case Inverse(e):
      return inverse(e, env)
    case Plus(e1, e2, env):
      return plus(evl(e1, env), evl(e2, env))
    case Minus(e1, e2, env):
      return minus(evl(e1, env), evl(e2, env))
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
