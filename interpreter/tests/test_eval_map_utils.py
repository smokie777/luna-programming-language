# test_eval_map_utils.py

from ..expressions import *
from ..luna_eval import luna_eval
from .test_utils import assert_builtin_fn_call
from ..equals import luna_equals
from ..arithmetic import luna_plus, luna_minus
import pytest

def make_test_map():
  return Map([["a", 1], ["b", "two"], ["c", ["a list"]]])

def assert_builtin_not_mutate(builtin_name:str, builtin_args:list):
  result = luna_eval(Program([
    VarSet("a", make_test_map()),
    Invoke(VarGet(builtin_name), builtin_args),
    VarGet("a")
  ]))
  assert isinstance(result, Map)
  expected = make_test_map()
  assert result.aa == expected.aa

def assert_builtin_mutates(builtin_name:str, builtin_args:list, expected):
  result = luna_eval(Program([
    VarSet("a", make_test_map()),
    Invoke(VarGet(builtin_name), builtin_args),
    VarGet("a")
  ]))
  assert isinstance(result, Map)
  assert isinstance(expected, Map)
  assert result.aa == expected.aa

def test_map_construction():
  Map([])
  Map([["kv", "pair"]])
  Map([[Map([["not", "hashable"]]), Map([["not", "hashable"]])]])
  with pytest.raises(Exception):
    Map("not an aa")
  with pytest.raises(Exception):
    Map([["not a kv pair"]])
  with pytest.raises(Exception):
    Map([["not", "a", "kv pair"]])
  with pytest.raises(Exception):
    Map([["duplicate_key", "v1"], ["duplicate_key", "v2"]])

def test_map_equality():
  assert luna_equals(Map([]), Map([]))
  assert luna_equals(make_test_map(), make_test_map())
  assert luna_equals(Map([["k", Map([])]]), Map([["k", Map([])]]))
  assert luna_equals(
    make_test_map(),
    Map([["a", 1], ["c", ["a list"]], ["b", "two"]])
  )
  assert luna_equals(make_test_map(), Map([])) == False

def test_eval_keys():
  assert_builtin_fn_call("keys", [make_test_map()], ["a", "b", "c"])
  assert_builtin_not_mutate("keys", [VarGet("a")])

def test_eval_values():
  assert_builtin_fn_call("values", [make_test_map()], [1, "two", ["a list"]])
  assert_builtin_not_mutate("values", [VarGet("a")])

def test_eval_pairs():
  assert_builtin_fn_call("pairs", [make_test_map()], make_test_map().aa)
  assert_builtin_not_mutate("pairs", [VarGet("a")])

def test_eval_containskey():
  assert_builtin_fn_call("containskey", [make_test_map(), "b"], True)
  assert_builtin_fn_call("containskey", [make_test_map(), "d"], False)
  assert_builtin_not_mutate("containskey", [VarGet("a"), "b"])

def test_eval_containsvalue():
  assert_builtin_fn_call("containsvalue", [make_test_map(), 1], True)
  assert_builtin_fn_call("containsvalue", [make_test_map(), 99], False)
  assert_builtin_not_mutate("containsvalue", [VarGet("a"), 1])
  
def test_eval_set():
  assert_builtin_fn_call("set", [make_test_map(), "b", "new b"], "new b")
  assert_builtin_fn_call("set", [make_test_map(), "z", "zv"], "zv")
  exp1 = make_test_map()
  exp1.aa[1][1] = "new b"
  assert_builtin_mutates("set", [VarGet("a"), "b", "new b"], exp1)
  exp2 = make_test_map()
  exp2.aa.append(["z", "zv"])
  assert_builtin_mutates("set", [VarGet("a"), "z", "zv"], exp2)

def test_eval_delete():
  assert_builtin_fn_call("delete", [make_test_map(), "b"], True)
  assert_builtin_fn_call("delete", [make_test_map(), "z"], True)
  exp1 = make_test_map()
  exp1.aa.pop(1)
  assert_builtin_mutates("delete", [VarGet("a"), "b"], exp1)
  exp2 = make_test_map()
  assert_builtin_mutates("delete", [VarGet("a"), "z"], exp2)

def test_map_arithmetic():
  a = Map([["a", 1], ["b", 2]])
  b = Map([["a", 9], ["c", 3]])
  assert luna_plus(a, b).aa == Map([
    ["a", 9], ["b", 2], ["c", 3]
  ]).aa
  a = Map([["a", 1], ["b", 2]])
  b = Map([["a", 1], ["c", 3]])
  assert luna_minus(a, b).aa == Map([
    ["b", 2]
  ]).aa
