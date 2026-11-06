# test_operations.py

from typeutils import *
from arithmetic import *
from equals import luna_equals
from utils import *
import pytest

def test_coerce():
  matrix_axis = ["a", True, 3, [4]]
  expected = [
    ("a", "a"), ("a", "true"), ("a", "3"), (["a"], [4]),
    ("true", "a"), (True, True), (1, 3), ([True], [4]),
    ("3", "a"), (3, 1), (3, 3), ([3], [4]),
    ([4], ["a"]), ([4], [True]), ([4], [3]), ([4], [4]),
  ]
  i = 0
  for x in matrix_axis:
    for y in matrix_axis:
      assert luna_coerce(x, y) == expected[i]
      i = i + 1

def test_to_boolean():
  assert luna_to_boolean("foo") == True
  assert luna_to_boolean("") == False
  assert luna_to_boolean(True) == True
  assert luna_to_boolean(False) == False
  assert luna_to_boolean(3) == True
  assert luna_to_boolean(0) == False
  assert luna_to_boolean(3.5) == True
  assert luna_to_boolean(0.0) == False
  assert luna_to_boolean([]) == False
  assert luna_to_boolean([1]) == True
  with pytest.raises(Exception):
    luna_to_boolean({})

def test_to_number():
  assert luna_to_number("-3.6") == -3.6
  assert luna_to_number("4") == 4
  assert luna_to_number("0") == 0
  assert luna_to_number("") == 0
  assert luna_to_number("3.3.3") == 0
  assert luna_to_number("3-") == 0
  assert luna_to_number("3.") == 0
  assert luna_to_number(True) == 1
  assert luna_to_number(False) == 0
  assert luna_to_number(3) == 3
  assert luna_to_number(3.5) == 3.5
  with pytest.raises(Exception):
    luna_to_number([])

def test_to_string():
  assert luna_to_string("foo") == "foo"
  assert luna_to_string(True) == "true"
  assert luna_to_string(False) == ""
  assert luna_to_string(3) == "3"
  assert luna_to_string(3.5) == "3.5"
  with pytest.raises(Exception):
    luna_to_string([])

def test_to_list():
  assert luna_to_list("foo") == ["f", "o", "o"]
  assert luna_to_list(True) == [True]
  assert luna_to_list(False) == []
  assert luna_to_list(3) == [3]
  assert luna_to_list(3.5) == [3.5]
  assert luna_to_list([]) == []
  assert luna_to_list(["foo"]) == ["foo"]
  with pytest.raises(Exception):
    luna_to_list({})

def test_inverse():
  assert luna_inverse("foo") == "oof"
  assert luna_inverse(True) == False
  assert luna_inverse(False) == True
  assert luna_inverse(34) == -34
  assert luna_inverse(3.5) == -3.5
  assert luna_inverse([1,2]) == [2,1]
  with pytest.raises(Exception):
    luna_inverse({})

def test_equals():
  matrix_axis = ["1", True, 1, 1.0, [1]]
  expected = [
    True, False, False, False, False,
    False, True, False, False, False,
    False, False, True, True, False,
    False, False, True, True, False,
    False, False, False, False, True
  ]
  i = 0
  for x in matrix_axis:
    for y in matrix_axis:
      assert luna_equals(x, y) == expected[i], f"[FAIL] x={x!r}, y={y!r}, idx={i}"
      i = i + 1

def test_inverse_concatenate():
  assert luna_inverse_concatenate([1,2,3], [2,3]) == [1]
  assert luna_inverse_concatenate([1,2,3], [1,2,3]) == []
  assert luna_inverse_concatenate([1,2,3], [1,2,3,4]) == [1,2,3]
  assert luna_inverse_concatenate([1,2,3], [3,2]) == [1,2,3]
  assert luna_inverse_concatenate("123", "23") == "1"
  assert luna_inverse_concatenate("123", "123") == ""
  assert luna_inverse_concatenate("123", "1234") == "123"
  assert luna_inverse_concatenate("123", "32") == "123"
  assert luna_inverse_concatenate([1,2,3], 3) == [1,2]
  assert luna_inverse_concatenate("123", ["3"]) == ["1","2"]
  assert luna_inverse_concatenate("123", [2]) == ["1","2","3"]
  assert luna_inverse_concatenate(True, True) == ""
  assert luna_inverse_concatenate(3, True) == "3"
  assert luna_inverse_concatenate("true", True) == ""
  assert luna_inverse_concatenate("true", False) == "true"

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
      assert luna_plus(x, y) == expected[i]
      i = i + 1
  assert luna_plus(True, True) == 2
  assert luna_plus(False, False) == 0
  assert luna_plus(True, False) == 1
  assert luna_plus(False, True) == 1

def test_minus():
  matrix_axis_x = ["a", True, 3, [7]]
  matrix_axis_y = ["a", False, 5, [1]]
  expected = [
    "", "a", "a", ["a"],
    "true", 1, -4, [True],    
    "3", 3, -2, [3],
    [7], [7], [7], [7],
  ]
  i = 0
  for x in matrix_axis_x:
    for y in matrix_axis_y:
      assert luna_minus(x, y) == expected[i]
      i = i + 1

def test_plus_minus_round_trip():
  a = [1,2,3]
  b = [2,3,4]
  c = luna_plus(a, b)
  assert c == [1,2,3,2,3,4]
  c = luna_minus(c, b)
  assert c == a

def test_times():
  assert luna_times(True, True) == 1
  assert luna_times(False, False) == 0
  assert luna_times(True, False) == 0
  assert luna_times(False, True) == 0
  assert luna_times(2, 3) == 6
  assert luna_times(3, 2) == 6
  assert luna_times(-2, 3) == -6
  assert luna_times(3, -2) == -6
  assert luna_times(-2, -3) == 6
  assert luna_times("ab", 2) == "abab"
  assert luna_times(2, "ab") == "abab"
  assert luna_times([1, 2], 2) == [1,2,1,2]
  assert luna_times(2, [1, 2]) == [1,2,1,2]
  assert luna_times("ab", -2) == "baba"
  assert luna_times(-2, "ab") == "baba"
  assert luna_times([1, 2], -2) == [2,1,2,1]
  assert luna_times(-2, [1, 2]) == [2,1,2,1]
  with pytest.raises(Exception):
    luna_times("a", "b")
  with pytest.raises(Exception):
    luna_times("a", [3])
  with pytest.raises(Exception):
    luna_times([3], "a")
  with pytest.raises(Exception):
    luna_times([3], [3])

def test_times_one():
  cases = [True, 2, "3", [4], False, 1, 0, "", []]
  for i in cases:
    assert luna_times(i, 1) == i
    assert luna_times(1, i) == i

def test_times_zero():
  cases = [True, 2, "3", [4], False, 1, 0, "", []]
  for i in cases:
    assert luna_times(i, 0) == luna_void(i)
    assert luna_times(0, i) == luna_void(i)

def test_divide():
  assert luna_divide(6, 3) == 2
  assert luna_divide(3, 6) == 0.5
  assert luna_divide(-6, 3) == -2
  assert luna_divide(3, -6) == -0.5
  assert luna_divide(-3, -6) == 0.5
  assert luna_divide("abab", "ab") == 2
  assert luna_divide("abab", 2) == "ab"
  assert luna_divide("abab", -2) == "ba"
  assert luna_divide([1,2,1,2],[1,2]) == 2
  assert luna_divide([1,2,1,2],2) == [1,2]
  assert luna_divide([1,2,1,2],-2) == [2,1]

def test_divide_one():
  cases = [2, "3", [4], 1, 0, "", []]
  for i in cases:
    assert luna_divide(i, 1) == i

def test_invalid_division():
  cases = [2, "3", [4], 1, 0, "", []]
  for i in cases:
    with pytest.raises(Exception):
      luna_divide(True, i)
    with pytest.raises(Exception):
      luna_divide(False, i)
    with pytest.raises(Exception):
      luna_divide(i, 0)
    with pytest.raises(Exception):
      luna_divide(i, [])
    with pytest.raises(Exception):
      luna_divide(i, "")
    with pytest.raises(Exception):
      luna_divide(i, False)
