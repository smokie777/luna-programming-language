# eval.py

from expressions import *
from typeutils import *
from arithmetic import *
from reductions import *
from utils import *
from Env import Env
from luna_types import EvalExpr

# Evaluates an expression recursively.
# Each function call creates a new scope.
def luna_eval(expr:EvalExpr, env=None) -> EvalExpr:
  env = Env() if env is None else env

  if not isinstance(env, Env):
    luna_throw(f'Invalid env for luna_eval: {env}')
  if not isinstance(expr, EvalExpr):
    luna_throw(f'Invalid expr type for luna_eval: {expr}')

  match expr:
    case str() | int() | float() | bool() | list():
      return expr;
    case Frozen(e):
      return e
    case Block(e):
      # Blocks are intentionally designed as lists,
      # even though only the last result is needed,
      # so that they can be disassembled and composed.
      e = eval_to_list_or_throw(e, env, "Block")
      ret = False
      for i in e:
        ret = luna_eval(i, env)
        if env.get_is_function_returning():
          break
      return ret
    case Invoke(e, args):
      # this eval either:
      # - strips away a Freeze, evaluating whatever is underneath
      # - does nothing to a Switch or Function
      invokable = luna_eval(e, env)
      match invokable:
        case Function(args_varnames, block):
          if len(args) != len(args_varnames):
            luna_throw(f'Invoke Function expected {len(args_varnames)} args. Got: {args}')
          scope = Env({}, env, True)
          for i in range(len(args)):
            scope.set(args_varnames[i], luna_eval(args[i], env))
          return luna_eval(block, scope)
        case Switch(condition, cases, branches, default_branch):
          condition = luna_eval(condition, env)
          # TODO: short circuiting for switch cases?
          # probably not - if your switch case generation has side effects,
          # then you should probably re-write your code!
          cases = luna_eval(cases, env)
          if not isinstance(cases, list):
            luna_throw(f'Switch cases must be a list. Got: {cases}')
          branches = luna_eval(branches, env)
          if (
            not isinstance(branches, list)
            or isinstance(branches, list) and len(branches) != len(cases)
          ):
            luna_throw(f'Switch cases and branches lists must have equal length. Got: {len(cases)} cases, {len(branches)} branches')
          for idx in range(len(cases)):
            if luna_equals(cases[idx], condition):
              return luna_eval(branches[idx], env)
          return luna_eval(default_branch, env)
        case Block(e):
          return luna_eval(invokable, env)
        case _:
          # the invokable has already been evaluated! just return the result.
          return invokable
    case Function() as fn:
      return fn
    case Return(e):
      if env.get_is_function_scope():
        return_value = luna_eval(e, env)
        env.set_is_function_returning()
        return return_value
      else:
        luna_throw(f'Can\'t use return keyword outside function scope.')
    case Switch() as sw:
      return sw
    case VarGet(varname):
      # Important: VarGet does NOT evaluate the variable it got.
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
    case All(e):
      if isinstance(e, list): # short circuit
        return luna_and((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "All")
      return luna_and([luna_eval(i, env) for i in l])
    case Some(e):
      if isinstance(e, list): # short circuit
        return luna_or((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "Some")
      return luna_or([luna_eval(i, env) for i in l])
    case Equals(e):
      if isinstance(e, list): # short circuit
        return luna_equals_all((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "Equals")
      return luna_equals_all([luna_eval(i, env) for i in l])
    case Lt(e):
      if isinstance(e, list): # short circuit
        return luna_lt_all((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "Equals")
      return luna_lt_all([luna_eval(i, env) for i in l])
    case Lte(e):
      if isinstance(e, list): # short circuit
        return luna_lte_all((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "Equals")
      return luna_lte_all([luna_eval(i, env) for i in l])
    case Gt(e):
      if isinstance(e, list): # short circuit
        return luna_gt_all((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "Equals")
      return luna_gt_all([luna_eval(i, env) for i in l])
    case Gte(e):
      if isinstance(e, list): # short circuit
        return luna_gte_all((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "Equals")
      return luna_gte_all([luna_eval(i, env) for i in l])
    case Sum(e):
      l = eval_to_list_or_throw(e, env, "Sum")
      return luna_sum([luna_eval(i, env) for i in l])
    case Difference(e):
      l = eval_to_list_or_throw(e, env, "Difference")
      return luna_difference([luna_eval(i, env) for i in l])
    case Product(e):
      l = eval_to_list_or_throw(e, env, "Product")
      return luna_product([luna_eval(i, env) for i in l])
    case Quotient(e):
      l = eval_to_list_or_throw(e, env, "Quotient")
      return luna_quotient([luna_eval(i, env) for i in l])
    case _:
      luna_throw(f'can\'t evalute a non-expression: {expr}')

def eval_to_list_or_throw(e, env, operation_name):
  l = luna_eval(e, env)
  if not isinstance(l, list):
    luna_throw(f'Operation {operation_name} requires a list. Got: {l}')
  return l
