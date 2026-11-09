# eval.py

from .expressions import *
from .typeutils import *
from .arithmetic import *
from .reductions import *
from .utils import *
from .Env import Env
from .luna_types import EvalExpr

# Evaluates an expression recursively.
# Each function call creates a new scope.
def luna_eval(expr:EvalExpr, env=None) -> EvalExpr:
  env = Env() if env is None else env

  if not isinstance(env, Env):
    luna_throw(f'Invalid env for luna_eval: {env}')
  if not isinstance(expr, EvalExpr):
    luna_throw(f'Invalid expr type for luna_eval: {expr}')
  if env.depth > 50:
    luna_throw(f'Recursion depth of 50 exceeded!')

  match expr:
    case str() | int() | float() | bool():
      return expr;
    case list():
      return [luna_eval(i, env) for i in expr]
    case Frozen(e):
      return e
    case Program(l):
      return [luna_eval(i, env) for i in l][-1]
    case Print(e):
      print(luna_eval(e, env))
      return False
    case Invoke(e, args):
      invokable = luna_eval(e, env)
      match invokable:
        case Function(params, body):
          args = eval_to_list_or_throw(args, env, "Invoke Function")
          if len(params) != len(args):
            luna_throw(f'Function expected {len(params)} args. Got: {len(args)}')
          scope = Env({}, env)
          scope.depth = env.depth + 1
          for i in range(len(args)):
            scope.set(params[i], args[i])
          try:
            return luna_eval(body, scope)
          except ReturnSignal as signal:
            return signal.e
          except BreakSignal:
            luna_throw('Can\'t Break a loop in scope outside current Function scope.')
          except ContinueSignal:
            luna_throw('Can\'t Continue a loop in scope outside current Function scope.')
        # more invokables may be added later such as classes, etc.
        case _:
          # invoking anything else will just function like eval()
          return luna_eval(invokable, env)
    case Function() as fn:
      return fn
    case Switch(condition, cases, branches, default_branch):
      condition = luna_eval(condition, env)
      cases = luna_eval(cases, env)
      if not isinstance(cases, list):
        luna_throw(f'Switch cases must be a list. Got: {cases}')
      if len(branches) != len(cases):
        luna_throw(f'Switch cases and branches lists must have equal length. Got: {len(cases)} cases, {len(branches)} branches')
      for idx in range(len(cases)):
        if luna_equals(cases[idx], condition):
          return luna_eval(branches[idx], env)
      return luna_eval(default_branch, env)
    case Loop(iterable, body, iterator_varname, index_varname):
      iterable = luna_eval(iterable)
      if iterable in (False, "", 0, []):
        return False
      max_idx = 0
      iterator_var_original = None
      index_var_original = None
      if iterator_varname is not None and env.has(iterator_varname):
        iterator_var_original = env.get(iterator_varname)
      if index_varname is not None and env.has(index_varname):
        index_var_original = env.get(index_varname)
      match iterable:
        case str() | list():
          max_idx = len(iterable)
        case bool():
          max_idx = float("inf")
        case int() | float():
          iterable_int = int(iterable)
          if iterable_int < 0:
            luna_throw(f'Iterable number must be >= 0. Got: {iterable_int}')
          max_idx = iterable_int
        case _:
          luna_throw(f'Iterable must be int/float/str/list/bool. Got: {iterable}')
      idx = 0
      item = None
      while idx < max_idx:
        match iterable:
          case str() | list():
            item = iterable[idx]
          case bool():
            item = True
          case int() | float():
            item = idx
        if iterator_varname is not None:
          env.set(iterator_varname, item)
        if index_varname is not None:
          env.set(index_varname, idx)
        try:
          luna_eval(body, env)
        except BreakSignal:
          break
        except ContinueSignal:
          pass
        idx += 1
      if iterator_var_original is not None:
        env.set(iterator_varname, iterator_var_original)
      if index_var_original is not None:
        env.set(index_varname, index_var_original)
      return False
    case VarGet(varname):
      # Important: VarGet does NOT evaluate the variable it got.
      return env.get(varname)
    case VarSet(varname, e):
      env.set(varname, luna_eval(e, env))
      return env.get(varname)
    case Return(e):
      raise ReturnSignal(luna_eval(e, env))
    case Continue():
      raise ContinueSignal
    case Break():
      raise BreakSignal
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
      return luna_and(l)
    case Some(e):
      if isinstance(e, list): # short circuit
        return luna_or((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "Some")
      return luna_or(l)
    case Equals(e):
      if isinstance(e, list): # short circuit
        return luna_equals_all((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "Equals")
      return luna_equals_all(l)
    case Lt(e):
      if isinstance(e, list): # short circuit
        return luna_lt_all((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "Equals")
      return luna_lt_all(l)
    case Lte(e):
      if isinstance(e, list): # short circuit
        return luna_lte_all((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "Equals")
      return luna_lte_all(l)
    case Gt(e):
      if isinstance(e, list): # short circuit
        return luna_gt_all((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "Equals")
      return luna_gt_all(l)
    case Gte(e):
      if isinstance(e, list): # short circuit
        return luna_gte_all((luna_eval(i, env) for i in e))
      l = eval_to_list_or_throw(e, env, "Equals")
      return luna_gte_all(l)
    case Sum(e):
      l = eval_to_list_or_throw(e, env, "Sum")
      return luna_sum(l)
    case Difference(e):
      l = eval_to_list_or_throw(e, env, "Difference")
      return luna_difference(l)
    case Product(e): # can't short circuit; inputs may be lists
      l = eval_to_list_or_throw(e, env, "Product")
      return luna_product(l)
    case Quotient(e): # can't short circuit; inputs may be lists
      l = eval_to_list_or_throw(e, env, "Quotient")
      return luna_quotient(l)
    case _:
      luna_throw(f'can\'t evalute a non-expression: {expr}')

def eval_to_list_or_throw(e, env, operation_name):
  l = luna_eval(e, env)
  if not isinstance(l, list):
    luna_throw(f'Operation {operation_name} requires a list. Got: {l}')
  return l
