# builtins_list.py

from .eval_helpers import eval_to_list_or_throw, eval_to_function_or_throw, eval_to_int_or_throw
from .typeutils import luna_to_boolean
from .utils import clamp, mutate_exact_num_args
from .equals import luna_equals
from .expressions import *

def builtin_lmap(eval_fn, env, args):
  mutate_exact_num_args(args, 2, "lmap")
  l = eval_to_list_or_throw(args[0], eval_fn, env, "lmap arg 1")
  fn = eval_to_function_or_throw(args[1], eval_fn, env, "lmap arg 2")
  return [eval_fn(Invoke(fn, [i]), env) for i in l]

def builtin_filter(eval_fn, env, args):
  mutate_exact_num_args(args, 2, "filter")
  l = eval_to_list_or_throw(args[0], eval_fn, env, "filter arg 1")
  fn = eval_to_function_or_throw(args[1], eval_fn, env, "filter arg 2")
  return [i for i in l if luna_to_boolean(eval_fn(Invoke(fn, [i]), env))]

def builtin_insert(eval_fn, env, args):
  mutate_exact_num_args(args, 3, "insert")
  l = eval_to_list_or_throw(args[0], eval_fn, env, "insert arg 1")
  v = eval_fn(args[1], env)
  if args[2] is None:
    l.append(v)
  else:
    idx = eval_to_int_or_throw(args[2], eval_fn, env, "insert arg 3 (index), if provided,")
    l.insert(clamp(idx, 0, len(l)), v)
  return v

def builtin_pop(eval_fn, env, args):
  mutate_exact_num_args(args, 2, "pop")
  l = eval_to_list_or_throw(args[0], eval_fn, env, "pop arg 1")
  if args[1] is None:
    return l.pop()
  idx = eval_to_int_or_throw(args[1], eval_fn, env, "pop arg 2 (index), if provided,")
  return l.pop(clamp(idx, 0, len(l)-1))

def builtin_get(eval_fn, env, args):
  mutate_exact_num_args(args, 2, "get")
  l = eval_to_list_or_throw(args[0], eval_fn, env, "get arg 1")
  idx = eval_to_int_or_throw(args[1], eval_fn, env, "get arg 2 (index), if provided,")
  return l[clamp(idx, 0, len(l)-1)]

def builtin_getindex(eval_fn, env, args):
  mutate_exact_num_args(args, 2, "getindex")
  l = eval_to_list_or_throw(args[0], eval_fn, env, "getindex arg 1")
  v = eval_fn(args[1], env)
  for index, item in enumerate(l):
    if luna_equals(item, v):
      return index
  return False

def builtin_contains(eval_fn, env, args):
  idx = builtin_getindex(eval_fn, env, args)
  return idx is not False

def builtin_find(eval_fn, env, args):
  mutate_exact_num_args(args, 2, "find")
  l = eval_to_list_or_throw(args[0], eval_fn, env, "find arg 1")
  fn = eval_to_function_or_throw(args[1], eval_fn, env, "find arg 2")
  for i in l:
    if luna_to_boolean(eval_fn(Invoke(fn, [i]), env)):
      return i
  return False

def builtin_findindex(eval_fn, env, args):
  mutate_exact_num_args(args, 2, "findindex")
  l = eval_to_list_or_throw(args[0], eval_fn, env, "findindex arg 1")
  fn = eval_to_function_or_throw(args[1], eval_fn, env, "findindex arg 2")
  for index, item in enumerate(l):
    if luna_to_boolean(eval_fn(Invoke(fn, [item]), env)):
      return index
  return False

def builtin_slice(eval_fn, env, args):
  # apparently, end_idx being exclusive results in interesting mathematical elegances.
  mutate_exact_num_args(args, 3, "slice")
  l = eval_to_list_or_throw(args[0], eval_fn, env, "slice arg 1")
  start_idx = clamp(eval_to_int_or_throw(args[1], eval_fn, env, "slice arg 2"), 0, len(l) - 1)
  end_idx = len(l) if args[2] is None else (
    clamp(eval_to_int_or_throw(args[2], eval_fn, env, "slice arg 3"), 0, len(l))
  )
  ret = []
  while start_idx < end_idx:
    ret.append(l[start_idx])
    start_idx += 1
  return ret

def builtin_sum(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "sum")
  return eval_fn(Sum(args[0]), env)

def builtin_difference(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "difference")
  return eval_fn(Difference(args[0]), env)

def builtin_product(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "product")
  return eval_fn(Product(args[0]), env)

def builtin_quotient(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "quotient")
  return eval_fn(Quotient(args[0]), env)

def builtin_remainderall(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "remainderall")
  return eval_fn(RemainderAll(args[0]), env)

def builtin_lt(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "lt")
  return eval_fn(Lt(args[0]), env)

def builtin_lte(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "lte")
  return eval_fn(Lte(args[0]), env)

def builtin_gt(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "gt")
  return eval_fn(Gt(args[0]), env)

def builtin_gte(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "gte")
  return eval_fn(Gte(args[0]), env)

def builtin_equals(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "equals")
  return eval_fn(Equals(args[0]), env)

def builtin_all(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "all")
  return eval_fn(All(args[0]), env)

def builtin_some(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "some")
  return eval_fn(Some(args[0]), env)

builtins_list = {
  "lmap": BuiltinFunction(builtin_lmap),
  "filter": BuiltinFunction(builtin_filter),
  "insert": BuiltinFunction(builtin_insert),
  "pop": BuiltinFunction(builtin_pop),
  "get": BuiltinFunction(builtin_get),
  "getindex": BuiltinFunction(builtin_getindex),
  "contains": BuiltinFunction(builtin_contains),
  "find": BuiltinFunction(builtin_find),
  "findindex": BuiltinFunction(builtin_findindex),
  "slice": BuiltinFunction(builtin_slice),
  "sum": BuiltinFunction(builtin_sum),
  "difference": BuiltinFunction(builtin_difference),
  "product": BuiltinFunction(builtin_product),
  "quotient": BuiltinFunction(builtin_quotient),
  "remainder": BuiltinFunction(builtin_remainderall),
  "lt": BuiltinFunction(builtin_lt),
  "lte": BuiltinFunction(builtin_lte),
  "gt": BuiltinFunction(builtin_gt),
  "gte": BuiltinFunction(builtin_gte),
  "equals": BuiltinFunction(builtin_equals),
  "all": BuiltinFunction(builtin_all),
  "some": BuiltinFunction(builtin_some),
}
