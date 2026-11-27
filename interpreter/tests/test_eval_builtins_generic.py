# test_eval_builtins_generic.py

from ..expressions import *
from ..luna_eval import luna_eval
from .test_utils import assert_builtin_fn_call
import pytest

def test_builtin_print(capsys):
  assert_builtin_fn_call("print", ["hello"], True)
  assert capsys.readouterr().out == "hello\n"

def test_builtin_type_conversions():
  assert_builtin_fn_call("toboolean", [3], True)
  assert_builtin_fn_call("tonumber", ["3"], 3)
  assert_builtin_fn_call("tostring", [3], "3")
  assert_builtin_fn_call("tolist", [3], [3])

def test_builtin_size():
  assert_builtin_fn_call("size", [[1,2]], 2)
  assert_builtin_fn_call(
    "size",
    [Map([["k1", "v1"], ["k2", "v2"]])],
    2
  )
  assert_builtin_fn_call("size", [3], 1)
  assert_builtin_fn_call("size", [True], 1)
  assert_builtin_fn_call("size", ["string"], 1)
  fn = Function([], Program([]))
  assert_builtin_fn_call("size", [fn], 1)
