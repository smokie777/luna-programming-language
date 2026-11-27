# builtins_generic.py

from .typeutils import luna_to_boolean, luna_to_string, luna_to_number, luna_to_list
from .utils import mutate_exact_num_args
from .expressions import BuiltinFunction

def builtin_print(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "print")
  print(args[0])
  return False

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

builtins_generic = {
  "print": BuiltinFunction(builtin_print),
  "boolean": BuiltinFunction(builtin_to_boolean),
  "string": BuiltinFunction(builtin_to_string),
  "number": BuiltinFunction(builtin_to_number),
  "list": BuiltinFunction(builtin_to_list),
}
