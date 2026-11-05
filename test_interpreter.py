# test_interpreter.py

from expressions import *
from runtime import *
from evl import *
import pytest

def lunaify(x):
  match x:
    case str() | bool() | int() | float():
      return V(x)
    case list():
      return L([lunaify(i) for i in x])
    case _:
      return x

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

def test_evl_values():
  assert evl(V(3)) == 3
  assert evl(V(0)) == 0
  assert evl(V("foo")) == "foo"
  assert evl(V("")) == ""
  assert evl(V(True)) == True
  assert evl(V(False)) == False
  with pytest.raises(Exception):
    evl(1)

def test_evl_lists():
  assert evl(lunaify([1,2])) == [1,2]
  with pytest.raises(Exception):
    evl(L([1,2]))

def test_evl_variables():
  assert evl(VarSet('my_var', V(3))) == 3
  assert evl(VarGet('my_var')) == 3
  with pytest.raises(Exception):
    evl(VarSet("my_var", 3))
  with pytest.raises(Exception):
    evl(VarGet("not_set"))
  with pytest.raises(Exception):
    evl(VarSet(3, V(3)))
  with pytest.raises(Exception):
    evl(VarGet(3,))

def test_to_boolean():
  assert to_boolean("foo") == True
  assert to_boolean("") == False
  assert to_boolean(True) == True
  assert to_boolean(False) == False
  assert to_boolean(3) == True
  assert to_boolean(0) == False
  assert to_boolean(3.5) == True
  assert to_boolean(0.0) == False
  assert to_boolean([]) == False
  assert to_boolean([1]) == True
  with pytest.raises(Exception):
    to_boolean({})

def test_to_number():
  assert to_number("-3.6") == -3.6
  assert to_number("4") == 4
  assert to_number("0") == 0
  assert to_number("") == 0
  assert to_number("3.3.3") == 0
  assert to_number("3-") == 0
  assert to_number("3.") == 0
  assert to_number(True) == 1
  assert to_number(False) == 0
  assert to_number(3) == 3
  assert to_number(3.5) == 3.5
  assert to_number([]) == 0
  assert to_number([1,2,3]) == 3
  with pytest.raises(Exception):
    to_number({})

def test_to_string():
  assert to_string("foo") == "foo"
  assert to_string(True) == "true"
  assert to_string(False) == "false"
  assert to_string(3) == "3"
  assert to_string(3.5) == "3.5"
  assert to_string([]) == "list0"
  assert to_string([1,2,3]) == "list3"
  with pytest.raises(Exception):
    to_string({})

def test_to_list():
  assert to_list("foo") == ["foo"]
  assert to_list(True) == [True]
  assert to_list(3) == [3]
  assert to_list(3.5) == [3.5]
  assert to_list([1]) == [1]
  with pytest.raises(Exception):
    to_list({})

def test_inverse():
  assert inverse(V("foo")) == "oof"
  assert inverse(V(True)) == False
  assert inverse(V(False)) == True
  assert inverse(V(34)) == -34
  assert inverse(V(3.5)) == -3.5
  assert inverse(L([V(1),V(2)])) == [2,1]
  with pytest.raises(Exception):
    inverse(V({}))

def test_plus():
  matrix_axis = ["a", True, 3, [4]]
  expected = [
    "aa", "atrue", "a3", ["a", 4],
    "truea", 2, 4, [True, 4],    
    "3a", 4, 6, [3, 4],
    [4, "a"], [4, True], [4, 3], [4, 4],
  ]
  i = 0
  for x in matrix_axis:
    for y in matrix_axis:
      assert plus(lunaify(x), lunaify(y)) == expected[i]
      i = i + 1
  assert plus(V(True), V(True)) == 2
  assert plus(V(False), V(False)) == 0
  assert plus(V(True), V(False)) == 1
  assert plus(V(False), V(True)) == 1
  