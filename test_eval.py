# test_eval.py

from expressions import *
from eval import luna_eval
import pytest

def lunaify(x):
  match x:
    case str() | bool() | int() | float():
      return V(x)
    case list():
      return L([lunaify(i) for i in x])
    case _:
      return x

def test_eval_non_expression():
  with pytest.raises(Exception):
    assert luna_eval("nonexpression")
    
def test_eval_non_env():
  with pytest.raises(Exception):
    assert luna_eval(V(3), "nonenv")

def test_eval_env_isolation():
  luna_eval(VarSet('my_var', V(3)))
  with pytest.raises(Exception):
    assert luna_eval(VarGet('my_var'))

def test_expression_v():
  assert V("foo").value == "foo"
  assert V(True).value == True
  assert V(3).value == 3
  assert V(3.5).value == 3.5 
  with pytest.raises(Exception):
    V([])

def test_expression_l():
  assert L([V(3)])
  with pytest.raises(Exception):
    L(3)

def test_eval_values():
  assert luna_eval(V(3)) == 3
  assert luna_eval(V(0)) == 0
  assert luna_eval(V("foo")) == "foo"
  assert luna_eval(V("")) == ""
  assert luna_eval(V(True)) == True
  assert luna_eval(V(False)) == False
  with pytest.raises(Exception):
    luna_eval(1)

def test_eval_lists():
  assert luna_eval(lunaify([1,2])) == [1,2]
  with pytest.raises(Exception):
    luna_eval(L([1,2]))

def test_eval_block():
  assert luna_eval(Block([])) == False
  assert luna_eval(Block([
    Product([V(2),V(3)]),
    Product([V(3),V(3)]),
    Product([V(4),V(3)]),
  ])) == 12

def test_block_return():
  assert luna_eval(Block([
    V(1),
    Return(V(2)),
    V(3),
  ])) == 2

def test_eval_variables():
  assert luna_eval(Block([
    VarSet('my_var', V(3)),
  ])) == 3
  assert luna_eval(Block([
    VarSet('my_var', V(3)),
    VarGet('my_var')
  ])) == 3
  with pytest.raises(Exception):
    luna_eval(VarSet("my_var", 3))
  with pytest.raises(Exception):
    luna_eval(VarGet("not_set"))
  with pytest.raises(Exception):
    luna_eval(VarSet(3, V(3)))
  with pytest.raises(Exception):
    luna_eval(VarGet(3,))

def test_eval_type_conversions():
  assert luna_eval(ToBoolean(V(3))) == True
  assert luna_eval(ToNumber(V("3"))) == 3
  assert luna_eval(ToString(V(3))) == "3"

def test_eval_inverse():
  assert luna_eval(Inverse(V(3))) == -3

def test_eval_all():
  assert luna_eval(All([V(True), V(False)])) == False

def test_eval_some():
  assert luna_eval(Some([V(True), V(False)])) == True

def test_eval_equals():
  assert luna_eval(Equals([V(3), V(3)])) == True

def test_eval_sum():
  assert luna_eval(Sum([V(1),V(2),V(3)])) == 6

def test_eval_difference():
  assert luna_eval(Difference([V(1),V(2),V(3)])) == -4

def test_eval_product():
  assert luna_eval(Product([V(1),V(2),V(3),V(4)])) == 24

def test_eval_quotient():
  assert luna_eval(Quotient([V(24),V(2),V(3)])) == 4
