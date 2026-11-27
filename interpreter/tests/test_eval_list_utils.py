# test_eval_list_utils.py

from ..expressions import *
from ..luna_eval import luna_eval
from .test_utils import assert_builtin_fn_call
from ..equals import luna_equals
import pytest

def assert_builtin_not_mutate(builtin_name:str, builtin_args:list):
  assert luna_eval(Program([
    VarSet("a", [1, 2, 3]),
    Invoke(VarGet(builtin_name), builtin_args),
    VarGet("a")
  ])) == [1,2,3]

def test_list_equality():
  assert luna_equals([],[])
  assert luna_equals([1,2],[1,2])
  assert luna_equals([1,2,[3]],[1,2,[3]])
  assert luna_equals([1,2],[2,1]) == False

def test_eval_lmap():
  fn = Function(["i"], Program([Product([VarGet("i"), 2])]))
  assert_builtin_fn_call("lmap", [[], fn], [])
  assert_builtin_fn_call("lmap", [[1, 2, 3], fn], [2, 4, 6])
  assert_builtin_not_mutate("lmap", [VarGet("a"), fn])

def test_eval_filter():
  fn = Function(["i"], Program([Equals([VarGet("i"), 2])]))
  assert_builtin_fn_call("filter", [[], fn], [])
  assert_builtin_fn_call("filter", [[1, 2, 3], fn], [2])
  assert_builtin_not_mutate("filter", [VarGet("a"), fn])

def test_eval_insert():
  def create_program(insert_expr):
    return Program([VarSet("a", [1, 2, 3]), insert_expr, VarGet("a")])
  cases = [
    (Invoke(VarGet("insert"), [VarGet("a"), ["new"]]), [1, 2, 3, ["new"]]),
    (Invoke(VarGet("insert"), [VarGet("a"), 4, 0]), [4, 1, 2, 3]),
    (Invoke(VarGet("insert"), [VarGet("a"), 4, -1]), [4, 1, 2, 3]),
    (Invoke(VarGet("insert"), [VarGet("a"), 4, -2]), [4, 1, 2, 3]),
    (Invoke(VarGet("insert"), [VarGet("a"), 4, 1]), [1, 4, 2, 3]),
    (Invoke(VarGet("insert"), [VarGet("a"), 4, 2]), [1, 2, 4, 3]),
    (Invoke(VarGet("insert"), [VarGet("a"), 4, 3]), [1, 2, 3, 4]),
    (Invoke(VarGet("insert"), [VarGet("a"), 4, 4]), [1, 2, 3, 4]),
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert_builtin_fn_call("insert", [[1, 2, 3], 4, 0], 4)

def test_eval_pop():
  def create_program(pop_expr):
    return Program([VarSet("a", [1, 2, 3]), pop_expr, VarGet("a")])
  cases = [
    (Invoke(VarGet("pop"), [VarGet("a"), -2]), [2, 3]),
    (Invoke(VarGet("pop"), [VarGet("a"), -1]), [2, 3]),
    (Invoke(VarGet("pop"), [VarGet("a"), 0]), [2, 3]),
    (Invoke(VarGet("pop"), [VarGet("a"), 1]), [1, 3]),
    (Invoke(VarGet("pop"), [VarGet("a"), 2]), [1, 2]),
    (Invoke(VarGet("pop"), [VarGet("a"), 3]), [1, 2]),
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert_builtin_fn_call("pop", [[1, 2, 3], 1], 2)

def test_eval_get():
  def create_program(get_expr):
    return Program([VarSet("a", [1, 2, 3]), get_expr])
  cases = [
    (Invoke(VarGet("get"), [VarGet("a"), -2]), 1),
    (Invoke(VarGet("get"), [VarGet("a"), -1]), 1),
    (Invoke(VarGet("get"), [VarGet("a"), 0]), 1),
    (Invoke(VarGet("get"), [VarGet("a"), 1]), 2),
    (Invoke(VarGet("get"), [VarGet("a"), 2]), 3),
    (Invoke(VarGet("get"), [VarGet("a"), 3]), 3),
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert_builtin_not_mutate("get", [VarGet("a"), 0])

def test_eval_getindex():
  def create_program(getindex_expr):
    return Program([VarSet("a", [1, 2, 3]), getindex_expr])
  cases = [
    (Invoke(VarGet("getindex"), [VarGet("a"), 3]), 2),
    (Invoke(VarGet("getindex"), [VarGet("a"), 4]), False),
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert_builtin_not_mutate("getindex", [VarGet("a"), 3])

def test_eval_contains():
  def create_program(contains_expr):
    return Program([VarSet("a", [1, 2, 3]), contains_expr])
  cases = [
    (Invoke(VarGet("contains"), [VarGet("a"), 3]), True),
    (Invoke(VarGet("contains"), [VarGet("a"), 4]), False),
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert_builtin_not_mutate("contains", [VarGet("a"), 3])

def test_eval_find():
  def create_program(find_expr):
    return Program([VarSet("a", [1, 2, 3]), find_expr])
  cases = [
    (Invoke(VarGet("find"), [VarGet("a"), Function(["i"], Program([Equals([VarGet("i"), 2])]))]), 2),
    (Invoke(VarGet("find"), [VarGet("a"), Function(["i"], Program([Equals([VarGet("i"), 4])]))]), False),
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert luna_eval(
    Program([
      VarSet("a", [[1], [2], [3]]), 
      Invoke(VarGet("find"), [
        VarGet("a"), 
        Function(["i"], Program([
          Invoke(VarGet("find"), [
            VarGet("i"), 
            Function(["j"], Program([Equals([VarGet("j"), 2])]))
          ])
        ]))
      ])
    ])
  ) == [2]
  assert_builtin_not_mutate(
    "find",
    [VarGet("a"), Function(["j"], Program([Equals([VarGet("j"), 2])]))]
  )
  
def test_eval_findindex():
  def create_program(findindex_expr):
    return Program([VarSet("a", [1, 2, 3]), findindex_expr])
  cases = [
    (Invoke(VarGet("findindex"), [VarGet("a"), Function(["i"], Program([Equals([VarGet("i"), 2])]))]), 1),
    (Invoke(VarGet("findindex"), [VarGet("a"), Function(["i"], Program([Equals([VarGet("i"), 4])]))]), False),
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert_builtin_not_mutate(
    "find",
    [VarGet("a"), Function(["i"], Program([Equals([VarGet("i"), 2])]))]
  )
  
def test_eval_slice():
  def create_program(slice_expr):
    return Program([VarSet("a", [1, 2, 3]), slice_expr])
  cases = [
    (Invoke(VarGet("slice"), [VarGet("a"), 1, 1]), []),
    (Invoke(VarGet("slice"), [VarGet("a"), 0, 3]), [1, 2, 3]),
    (Invoke(VarGet("slice"), [VarGet("a"), -10, 10]), [1, 2, 3]),
    (Invoke(VarGet("slice"), [VarGet("a"), 1, 10]), [2, 3]),
    (Invoke(VarGet("slice"), [VarGet("a"), -10, 2]), [1, 2]),
    (Invoke(VarGet("slice"), [VarGet("a"), 1, 2]), [2]),
    (Invoke(VarGet("slice"), [VarGet("a"), 2, 1]), [])
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert_builtin_not_mutate("slice", [VarGet("a"), 1, 2])

def test_eval_builtin_chains():
  assert_builtin_fn_call("sum", [[1,2,3]], 6)
  assert_builtin_fn_call("difference", [[10,3,2]], 5)
  assert_builtin_fn_call("product", [[2,3,4]], 24)
  assert_builtin_fn_call("quotient", [[24,2,3]], 4)
  assert_builtin_fn_call("remainder", [[10,3]], 1)
  assert_builtin_fn_call("lt", [[1,2,3]], True)
  assert_builtin_fn_call("lte", [[1,2,2]], True)
  assert_builtin_fn_call("gt", [[3,2,1]], True)
  assert_builtin_fn_call("gte", [[3,2,2]], True)
  assert_builtin_fn_call("equals", [[5,5,5]], True)
  assert_builtin_fn_call("all", [[True, True, True]], True)
  assert_builtin_fn_call("some", [[False, True, False]], True)
  