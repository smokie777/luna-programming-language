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

  if env.return_value is not None:
    return env.return_value
  
  if not isinstance(expr, EvalExpr):
    luna_throw(f'Invalid expr type for luna_eval: {expr}')
  if not isinstance(env, Env):
    luna_throw(f'Invalid env for luna_eval: {env}')

  match expr:
    case str() | int() | float() | bool():
      return expr;
    case list():
      return [luna_eval(i, env) for i in expr]
    case Block(e):
      # Blocks are intentionally designed as lists,
      # even though only the last result is needed,
      # so that they can be disassembled and composed.
      l = eval_to_list_or_throw(e, env, "Block")
      return False if len(l) == 0 else [luna_eval(e, env) for e in l][-1]
    case Function() as fn:
      fn.closure = env
      return expr
    case FunctionCall(fn, args):
      fn = luna_eval(fn, env)
      if not isinstance(fn, Function):
        luna_throw(f'Tried to FunctionCall a non-function: {fn}')
      args = luna_eval(args, env)
      if not isinstance(args, list) or len(args) != len(fn.args_varnames):
        luna_throw(f'FunctionCall expected {len(fn.args_varnames)} args in a list. Got: {args}')
      scope = Env({}, fn.closure)
      for i in range(len(args)):
        scope.set(fn.args_varnames[i], args[i])
      return luna_eval(fn.block, scope)
    case Return(e):
      return env.set_return_value(luna_eval(e, env))
    case Switch() as sw:
      return sw
    case SwitchBranches() as swb:
      return swb
    case SwitchCall(e):
      sw = luna_eval(e, env)
      if not isinstance(sw, Switch):
        luna_throw(f'Tried to SwitchCall a non-switch: {sw}')
      condition = luna_eval(sw.condition, env)
      # TODO: short circuiting for switch cases?
      # probably not - if your switch case generation has side effects,
      # then you should probably re-write your code!
      cases = luna_eval(sw.cases, env)
      if not isinstance(cases, list):
        luna_throw(f'Switch cases must be a list. Got: {cases}')
      switch_branches = luna_eval(sw.branches, env)
      if not isinstance(switch_branches, SwitchBranches):
        luna_throw(f'Switch branches must be SwitchBranches. Got: {switch_branches}')
      branches = switch_branches.branches
      if (
        not isinstance(branches, list)
        or isinstance(branches, list) and len(branches) != len(cases)
      ):
        luna_throw(f'Switch cases and branches lists must have equal length. Got: {len(cases)} cases, {len(branches)} branches')
      for idx in range(len(cases)):
        if luna_equals(cases[idx], condition):
          return luna_eval(branches[idx], env)
      return luna_eval(sw.default_branch, env)
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
    case All(e):
      if isinstance(e, list):
        # short circuit
        return luna_and((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "All")
      return luna_and([luna_eval(i, env) for i in l])
    case Some(e):
      if isinstance(e, list):
        # short circuit
        return luna_or((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "Some")
      return luna_or([luna_eval(i, env) for i in l])
    case Equals(e):
      if isinstance(e, list):
        # short circuit
        return luna_equals_all((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "Equals")
      return luna_equals_all([luna_eval(i, env) for i in l])
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
