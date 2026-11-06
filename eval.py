# evl.py

from expressions import *
from typeutils import *
from arithmetic import *
from reductions import *
from utils import *
from Env import default_env

def luna_eval(expr, env = default_env):
  match expr:
    case V(v):
      return v
    case L(es):
      return [luna_eval(e, env) for e in es]
    case VarGet(varname):
      return env.get(varname)
    case VarSet(varname, e):
      env.set(varname, luna_eval(e, env))
      return env.get(varname)
    case ToBoolean(e):
      return luna_to_boolean(luna_eval(e, env))
    case ToNumber(e):
      return luna_to_number(luna_eval(e, env))
    case ToString(e):
      return luna_to_string(luna_eval(e, env))
    case Inverse(e):
      return luna_inverse(luna_eval(e, env))
    case Sum(es):
      return luna_sum(
        [luna_eval(e, env) for e in es]
      )
    case Difference(es):
      return luna_difference(
        [luna_eval(e, env) for e in es]
      )
    case Product(es):
      return luna_product(
        [luna_eval(e, env) for e in es]
      )
    case Quotient(es):
      return luna_quotient(
        [luna_eval(e, env) for e in es]
      )
    case _:
      luna_throw(f'can\'t evalute a non-expression: {expr}')
