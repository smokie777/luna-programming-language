# test_eval.py

from expressions import *
from eval import luna_eval
import pytest

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

def test_eval_values():
  assert luna_eval(3) == 3
  assert luna_eval(0) == 0
  assert luna_eval("foo") == "foo"
  assert luna_eval("") == ""
  assert luna_eval(True) == True
  assert luna_eval(False) == False

def test_eval_lists():
  assert luna_eval([1,2]) == [1,2]

def test_eval_block():
  assert luna_eval(Block([])) == False
  assert luna_eval(Block([
    Product([2,3]),
    Product([3,3]),
    Product([4,3]),
  ])) == 12

def test_block_return():
  assert luna_eval(Block([
    1,
    Return(2),
    3,
  ])) == 2

  
def test_eval_frozen_block():
  assert luna_eval(Block([
    VarSet("a", 1),
    VarSet("foo", Frozen(Block([VarSet("a", 2)]))),
    VarGet("a")
  ])) == 1
  assert luna_eval(Block([
    VarSet("a", 1),
    VarSet("foo", Frozen(Block([VarSet("a", 2)]))),
    Invoke(VarGet("foo"), []),
    VarGet("a")
  ])) == 2

def test_eval_variables():
  assert luna_eval(Block([
    VarSet('my_var', 3),
  ])) == 3
  assert luna_eval(Block([
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

def test_eval_some():
  assert luna_eval(Some([True, False])) == True

def test_eval_equals():
  assert luna_eval(Equals([3, 3])) == True

def test_eval_lt():
  assert luna_eval(Lt([1,2])) == True

def test_eval_lte():
  assert luna_eval(Lte([1,1,2])) == True

def test_eval_gt():
  assert luna_eval(Gt([2,1])) == True

def test_eval_gte():
  assert luna_eval(Gte([2,1,1])) == True

def test_eval_sum():
  assert luna_eval(Sum([1,2,3])) == 6

def test_eval_difference():
  assert luna_eval(Difference([1,2,3])) == -4

def test_eval_product():
  assert luna_eval(Product([1,2,3,4])) == 24

def test_eval_quotient():
  assert luna_eval(Quotient([24,2,3])) == 4
