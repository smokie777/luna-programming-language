# test_reductions.py

from .reductions import *
import pytest

def test_reduce():
  assert luna_reduce(0, [1,2,3], lambda a, b: a + b) == 6

def test_and():
  assert luna_and([]) == False
  assert luna_and([1]) == True
  assert luna_and([1,2]) == True
  assert luna_and([1,0]) == False
  assert luna_and([0,0]) == False

def test_or():
  assert luna_and([]) == False
  assert luna_and([1]) == True
  assert luna_or([1,2]) == True
  assert luna_or([1,0]) == True
  assert luna_or([0,0]) == False

def test_equals_all():
  assert luna_equals_all([]) == False
  assert luna_equals_all([1]) == True
  assert luna_equals_all([1, 2]) == False
  assert luna_equals_all([1, 1]) == True
  assert luna_equals_all([1,1,1]) == True
  assert luna_equals_all([1,2,1]) == False

def test_gen_luna_sum_difference_acc():
  assert gen_luna_sum_difference_acc([False, 1, "2", [3]]) == []
  assert gen_luna_sum_difference_acc([False, 1, "2"]) == ""
  assert gen_luna_sum_difference_acc([False, 1]) == 0
  assert gen_luna_sum_difference_acc([False]) == False
  assert gen_luna_sum_difference_acc([]) == False

def test_sum():
  # same type
  assert luna_sum([True, False, True]) == 2
  assert luna_sum([1,2,3]) == 6
  assert luna_sum(["a", "b", "c"]) == "abc"
  assert luna_sum([[1], [2], [3]]) == [1, 2, 3]
  # different type
  assert luna_sum([]) == False
  assert luna_sum([False]) == 0
  assert luna_sum([False, 1]) == 1
  assert luna_sum([False, 1, "2"]) == "12"
  assert luna_sum([False, 1, "2", [4]]) == [1, "2", 4]

def test_difference():
  # same type
  assert luna_difference([True, False, True, True]) == -1
  assert luna_difference([1,2,3]) == -4
  assert luna_difference(["abc", "c", "b"]) == "a"
  assert luna_difference([[1, 2, 3], [3], [2]]) == [1]
  # different type
  assert luna_difference([]) == False
  assert luna_difference([False]) == False
  assert luna_difference([False, 1]) == -1
  assert luna_difference([False, 1, "2"]) == ""
  assert luna_difference([False, 1, "2", [4]]) == []
  # interesting examples
  assert luna_difference([True, 1]) == 0
  assert luna_difference([12345, "345"]) == "12"
  assert luna_difference([12345, "345", 2]) == "1"
  assert luna_difference([12345, [12345]]) == []
  assert luna_difference([True, 1, 1, 1]) == -2
  assert luna_difference([True, 1, 1, 1, "ue"]) == "tr"
  assert luna_difference(["footrue", True, "o", "o"]) == "f"
