# eval.py

from .expressions import *
from .typeutils import *
from .utils import *
from .Env import Env
from .luna_types import EvalExpr
from .equals import luna_equals
from common.mappings import equality_op_to_eval_fn, addition_op_to_eval_fn, multiplication_op_to_eval_fn

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
    case Map(aa):
      return [
        [luna_eval(i[0], env), luna_eval(i[1], env)]
        for i in aa
      ]
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
          if len(params) != len(args):
            luna_throw(f'Function expected {len(params)} args. Got: {len(args)}')
          scope = Env({}, env)
          scope.depth = env.depth + 1
          for i in range(len(args)):
            scope.set(params[i], luna_eval(args[i], env))
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
    case IfThenElse(condition, if_branch, else_branch):
      if luna_to_boolean(luna_eval(condition, env)):
        return False if if_branch is None else luna_eval(if_branch, env)
      else:
        return False if else_branch is None else luna_eval(else_branch, env)
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
    case Loop(iterable, iterator_varname, index_varname, body):
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
    case VarSetGlobal(varname, e):
      env.setGlobal(varname, luna_eval(e, env))
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
    case All(items):
      return all((luna_to_boolean(luna_eval(i, env)) for i in items))
    case Some(items):
      return any((luna_to_boolean(luna_eval(i, env)) for i in items))
    case EqualityChain(items, operators):
      prev = None
      curr = luna_eval(items[0], env)
      for idx, op in enumerate(operators):
        prev = curr
        curr = luna_eval(items[idx + 1], env)
        result = equality_op_to_eval_fn[op](prev, curr)
        if not result:
          return False
      return True
    case AdditionChain(items, operators):
      acc = luna_eval(items[0], env)
      for idx, op in enumerate(operators):
        acc = addition_op_to_eval_fn[op](acc, luna_eval(items[idx + 1], env))
      return acc
    case MultiplicationChain(items, operators):
      acc = luna_eval(items[0], env)
      for idx, op in enumerate(operators):
        acc = multiplication_op_to_eval_fn[op](acc, luna_eval(items[idx + 1], env))
      return acc
    case Exponent(items):
      acc = None
      for i in items:
        if acc is None:
          acc = i
        else:
          acc = acc ** i
      return acc
    case _:
      luna_throw(f'can\'t evalute a non-expression: {expr}')
