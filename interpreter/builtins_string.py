# builtins_string.py

from .eval_helpers import eval_to_string_or_throw
from .utils import mutate_exact_num_args
from .expressions import *

def builtin_trim(eval_fn, env, args):
  mutate_exact_num_args(args, 1, "trim")
  s = eval_to_string_or_throw(args[0], eval_fn, env, "trim arg 1")
  return s.strip()

builtins_string = {
  "trim": BuiltinFunction(builtin_trim),
}
