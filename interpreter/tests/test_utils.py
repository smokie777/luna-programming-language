# test_utils.py
from ..expressions import Invoke, VarGet
from ..luna_eval import luna_eval

def assert_builtin_fn_call(name:str, args:list, expected):
  assert luna_eval(Invoke(VarGet(name), args)) == expected
