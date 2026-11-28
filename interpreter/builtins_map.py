# builtins_map.py

from .eval_helpers import eval_to_map_or_throw
from .utils import mutate_exact_num_args
from .equals import luna_equals
from .expressions import BuiltinFunction

def builtin_keys(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "keys")
  m = eval_to_map_or_throw(args[0], eval_fn, env, "keys arg 1").aa
  return [i[0] for i in m]

def builtin_values(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "values")
  m = eval_to_map_or_throw(args[0], eval_fn, env, "values arg 1").aa
  return [i[1] for i in m]

def builtin_pairs(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "pairs")
  m = eval_to_map_or_throw(args[0], eval_fn, env, "pairs arg 1").aa
  return [i for i in m]

def builtin_containskey(eval_fn, env, args):
  mutate_exact_num_args(args, 2, "containskey")
  m = eval_to_map_or_throw(args[0], eval_fn, env, "containskey arg 1").aa
  key = eval_fn(args[1], env)
  for k, _ in m:
    if luna_equals(k, key):
      return True
  return False

def builtin_containsvalue(eval_fn, env, args):
  mutate_exact_num_args(args, 2, "containsvalue")
  m = eval_to_map_or_throw(args[0], eval_fn, env, "containsvalue arg 1").aa
  value = eval_fn(args[1], env)
  for _, v in m:
    if luna_equals(v, value):
      return True
  return False

def builtin_set(eval_fn, env, args):
  mutate_exact_num_args(args, 3, "set")
  m = eval_to_map_or_throw(args[0], eval_fn, env, "set arg 1").aa
  key = eval_fn(args[1], env)
  value = eval_fn(args[2], env)
  for i in range(len(m)):
    if luna_equals(m[i][0], key):
      m[i][1] = value
      return value
  m.append([key, value])
  return value

def builtin_delete(eval_fn, env, args):
  mutate_exact_num_args(args, 2, "delete")
  m = eval_to_map_or_throw(args[0], eval_fn, env, "delete arg 1").aa
  key = eval_fn(args[1], env)
  for i in range(len(m)):
    if luna_equals(m[i][0], key):
      m.pop(i)
      return True
  return False

builtins_map = {
  "keys": BuiltinFunction(builtin_keys),
  "values": BuiltinFunction(builtin_values),
  "pairs": BuiltinFunction(builtin_pairs),
  "containskey": BuiltinFunction(builtin_containskey),
  "containsvalue": BuiltinFunction(builtin_containsvalue),
  "set": BuiltinFunction(builtin_set),
  "delete": BuiltinFunction(builtin_delete),
}
