# test_eval.py

from .expressions import *
from .eval import luna_eval
import pytest

fn = Function(
  ["a", "b"],
  Program([Sum([VarGet("a"), VarGet("b")])])
)

def test_eval_non_expression():
  with pytest.raises(Exception):
    assert luna_eval({})
    
def test_eval_non_env():
  with pytest.raises(Exception):
    assert luna_eval(3, "nonenv")

def test_eval_env_isolation():
  luna_eval(VarSet('my_var', 3))
  with pytest.raises(Exception):
    assert luna_eval(VarGet('my_var'))

def test_get_and_set_variables():
  luna_eval(Program([
    VarSet("a", 1),
    VarGet("a")
  ])) == 1
  with pytest.raises(Exception):
    luna_eval(Program([
      VarSet("a", 1),
      VarGet("b")
    ]))

def test_eval_values():
  assert luna_eval(3) == 3
  assert luna_eval(0) == 0
  assert luna_eval("foo") == "foo"
  assert luna_eval("") == ""
  assert luna_eval(True) == True
  assert luna_eval(False) == False

def test_eval_lists():
  assert luna_eval([1,2]) == [1,2]
  assert luna_eval([]) == []
  assert luna_eval([1+1,2+2]) == [2,4]
  assert luna_eval([
    Product([2,3]),
    Product([3,3]),
    Product([4,3]),
  ]) == [6,9,12]

def test_eval_maps():
  assert luna_eval(Map([["k", "v"]])) == [["k", "v"]]
  assert luna_eval(Map()) == []
  assert luna_eval(Map([[1+1,2+2]])) == [[2,4]]
  assert luna_eval(Map([
    [Product([2,3]),Product([3,4])],
    [Sum([2,3]),Sum([3,4])],
  ])) == [
    [6,12],
    [5,7]
  ]

def test_eval_program_returns_last_expr_only():
  assert luna_eval(Program([
    1,
    2
  ])) == 2

def test_block_return_outside_fn_throws():
  with pytest.raises(Exception):
    assert luna_eval(Program([
      1,
      Return(2),
      3,
    ]))

def test_eval_frozen_block():
  assert luna_eval(Program([
    VarSet("a", 1),
    VarSet("foo", Frozen([VarSet("a", 2)])),
    VarGet("a")
  ])) == 1
  assert luna_eval(Program([
    VarSet("a", 1),
    VarSet("foo", Frozen([VarSet("a", 2)])),
    Invoke(VarGet("foo")),
    VarGet("a")
  ])) == 2

def test_eval_variables():
  assert luna_eval(Program([
    VarSet('my_var', 3),
  ])) == 3
  assert luna_eval(Program([
    VarSet('my_var', 3),
    VarGet('my_var')
  ])) == 3
  with pytest.raises(Exception):
    luna_eval(VarGet("not_set"))
  with pytest.raises(Exception):
    luna_eval(VarSet(3, 3))
  with pytest.raises(Exception):
    luna_eval(VarGet(3,))

def test_eval_type_conversions():
  assert luna_eval(ToBoolean(3)) == True
  assert luna_eval(ToNumber("3")) == 3
  assert luna_eval(ToString(3)) == "3"
  
def test_eval_inverse():
  assert luna_eval(Inverse(3)) == -3

def test_eval_all():
  assert luna_eval(All([True, False])) == False
  assert luna_eval(All([1, 2])) == True
  assert luna_eval(All([1, 0])) == False
  assert luna_eval(All([0, 0])) == False

def test_eval_some():
  assert luna_eval(Some([True, False])) == True
  assert luna_eval(Some([1, 2])) == True
  assert luna_eval(Some([1, 0])) == True
  assert luna_eval(Some([0, 0])) == False

def test_eval_equality_chain():
  assert luna_eval(EqualityChain(
    [1,1,1],
    [EqualityOp.EQ, EqualityOp.EQ]
  )) == True
  assert luna_eval(EqualityChain(
    [1,2,3,3,2,1],
    [EqualityOp.LT, EqualityOp.LTE, EqualityOp.EQ, EqualityOp.GT, EqualityOp.GTE]
  )) == True
  assert luna_eval(EqualityChain(
    [1,1,2],
    [EqualityOp.EQ, EqualityOp.EQ]
  )) == False
  assert luna_eval(EqualityChain(
    [9,2,3,3,2,1],
    [EqualityOp.LT, EqualityOp.LTE, EqualityOp.EQ, EqualityOp.GT, EqualityOp.GTE]
  )) == False

def test_eval_addition_chain():
  # same type
  assert luna_eval(Sum([True, False, True])) == 2
  assert luna_eval(Sum([1,2,3])) == 6
  assert luna_eval(Sum(["a", "b", "c"])) == "abc"
  assert luna_eval(Sum([[1], [2], [3]])) == [1, 2, 3]
  # different type
  assert luna_eval(Sum([False, 1])) == 1
  assert luna_eval(Sum([False, 1, "2"])) == "12"
  assert luna_eval(Sum([False, 1, "2", [4]])) == ["1", "2", 4]
  # same type
  assert luna_eval(Difference([True, False, True, True])) == -1
  assert luna_eval(Difference([1,2,3])) == -4
  assert luna_eval(Difference(["abc", "c", "b"])) == "a"
  assert luna_eval(Difference([[1, 2, 3], [3], [2]])) == [1]
  # different type
  assert luna_eval(Difference([False, 1])) == -1
  assert luna_eval(Difference([False, 1, "2"])) == "-1"
  assert luna_eval(Difference([False, 1, "2", [4]])) == ["-", "1"]
  # interesting examples
  assert luna_eval(Difference([True, 1])) == 0
  assert luna_eval(Difference([12345, "345"])) == "12"
  assert luna_eval(Difference([12345, "345", 2])) == "1"
  assert luna_eval(Difference([12345, [12345]])) == []
  assert luna_eval(Difference([True, 1, 1, 1])) == -2
  assert luna_eval(Difference([True, 1, 1, 1, "ue"])) == "-2"
  assert luna_eval(Difference(["footrue", True, "o", "o"])) == "f"
  # cross type
  assert luna_eval(AdditionChain([1, 2, 3, 4], [AdditionOp.PLUS, AdditionOp.MINUS, AdditionOp.PLUS])) == 4

def test_eval_multiplication_chain():
  assert luna_eval(Product([1, 2, 3])) == 6
  assert luna_eval(Quotient([6, 3, 2])) == 1
  assert luna_eval(RemainderAll([3, 6, 6])) == 3
  assert luna_eval(MultiplicationChain(
    [4, 3, 2, 3],
    [MultiplicationOp.TIMES, MultiplicationOp.DIVIDE, MultiplicationOp.TIMES]
  )) == 18
  assert luna_eval(MultiplicationChain(
    [4, 3, 2, 3, 5],
    [MultiplicationOp.TIMES, MultiplicationOp.DIVIDE, MultiplicationOp.TIMES, MultiplicationOp.PERCENT]
  )) == 3

def test_eval_invoke_random_stuff():
  assert luna_eval(Invoke(All([True, True]))) == True
