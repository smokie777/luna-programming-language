# create_default_env.py

from .Env import Env
from .builtins_generic import builtins_generic
from .builtins_list import builtins_list
from .builtins_map import builtins_map
from .builtins_string import builtins_string

def create_default_env():
  return Env(
    builtins_generic
    | builtins_list
    | builtins_map
    | builtins_string
  )
