# builtins_generic.py

from .luna_types import LvMap
from .typeutils import luna_to_boolean, luna_to_string, luna_to_number, luna_to_list
from .utils import mutate_exact_num_args, luna_throw, clamp
from .expressions import BuiltinFunction
from .eval_helpers import eval_to_int_or_throw
from .equals import luna_equals

def builtin_print(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "print")
  print(eval_fn(args[0], env))
  return True

def builtin_to_boolean(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "boolean")
  return luna_to_boolean(eval_fn(args[0], env))

def builtin_to_string(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "string")
  return luna_to_string(eval_fn(args[0], env))

def builtin_to_number(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "number")
  return luna_to_number(eval_fn(args[0], env))

def builtin_to_list(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "list")
  return luna_to_list(eval_fn(args[0], env))

def builtin_get(eval_fn, env, args):
  mutate_exact_num_args(args, 2, "get")
  collection = eval_fn(args[0], env)
  if isinstance(collection, list):
    idx = eval_to_int_or_throw(args[1], eval_fn, env, "get arg 2 (index), if provided,")
    return collection[clamp(idx, 0, len(collection)-1)]
  if isinstance(collection, LvMap):
    key = eval_fn(args[1], env)
    for k, v in collection.aa:
      if luna_equals(k, key):
        return v
    return False
  luna_throw(f'builtin "get" is only supported for list/Map. Got: {collection}')

def builtin_size(eval_fn, env, args):
  mutate_exact_num_args(args, 2, "size")
  collection = eval_fn(args[0], env)
  if isinstance(collection, list):
    return len(collection)
  if isinstance(collection, LvMap):
    return len(collection.aa)
  return 1

builtins_generic = {
  "print": BuiltinFunction(builtin_print),
  "toboolean": BuiltinFunction(builtin_to_boolean),
  "tostring": BuiltinFunction(builtin_to_string),
  "tonumber": BuiltinFunction(builtin_to_number),
  "tolist": BuiltinFunction(builtin_to_list),
  "get": BuiltinFunction(builtin_get),
  "size": BuiltinFunction(builtin_size)
}
