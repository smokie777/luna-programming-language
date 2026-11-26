# eval_helpers.py

from .utils import luna_throw
from .expressions import Function, Expression
from .Env import Env
from collections.abc import Callable

def eval_to_list_or_throw(e:Expression, eval_fn:Callable, env:Env, description:str) -> list:
  ret = eval_fn(e, env)
  if isinstance(ret, list):
    return ret
  luna_throw(f'{description} must be a list, got: {ret}')

def eval_to_function_or_throw(e:Expression, eval_fn:Callable, env:Env, description:str) -> Function:
  ret = eval_fn(e, env)
  if isinstance(ret, Function):
    return ret
  luna_throw(f'{description} must be a Function, got: {ret}')

def eval_to_int_or_throw(e:Expression, eval_fn:Callable, env:Env, description:str) -> int:
  ret = eval_fn(e, env)
  if isinstance(ret, int | float):
    return int(ret)
  luna_throw(f'{description} must be an Integer, got: {ret}')
  