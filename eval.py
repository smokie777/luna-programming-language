# eval.py

from expressions import *
from typeutils import *
from arithmetic import *
from reductions import *
from utils import *
from Env import Env

# Evaluates an expression recursively.
# Each function call creates a new scope.
def luna_eval(expr, env=None):
  env = Env() if env is None else env

  if env.return_value is not None:
    return env.return_value
  
  if not isinstance(expr, Expression):
    luna_throw(f'Can\'t evaluate non-expression: {expr}')
  if not isinstance(env, Env):
    luna_throw(f'Can\'t evaluate invalid env: {env}')

  match expr:
    case V(v):
      return v
    case L(es):
      return [luna_eval(e, env) for e in es]
    case Block(es):
      # Blocks are intentionally designed as lists,
      # even though only the last result is needed,
      # so that they can be disassembled and composed.
      return False if len(es) == 0 else [luna_eval(e, env) for e in es][-1]
    case Function(e, env):
      expr.closure = env
      return expr
    case FunctionCall(fn, args):
      args = luna_eval(args, env)
      fn = luna_eval(fn, env)
      if not isinstance(args, list) or len(args) != len(fn.args_varnames):
        luna_throw(f'FunctionCall expected {len(fn.args_varnames)} args in a list. Got: {args}')
      if not isinstance(fn, Function):
        luna_throw(f'Tried to FunctionCall a non-function: {fn}')
      scope = Env({}, fn.closure)
      for i in range(len(args)):
        scope.set(fn.args_varnames[i], args[i])
      return luna_eval(fn.block, scope)
    case Return(e):
      return env.set_return_value(luna_eval(e, env))
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
    case All(es): # short-circuits
      return luna_and(
        (luna_eval(e, env) for e in es)
      )
    case Some(es): # short-circuits
      return luna_or(
        (luna_eval(e, env) for e in es)
      )
    case Equals(es): # short-circuits
      return luna_equals_all(
        (luna_eval(e, env) for e in es)
      )
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
