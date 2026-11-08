# test_inequality.py

import pytest
from .inequality import *
from .reductions import *

def test_lt():
  assert luna_lt("a", "aa") == True
  assert luna_lt("aa", "aa") == False
  assert luna_lt("aa", "a") == False
  assert luna_lt(3, 4) == True
  assert luna_lt(4, 4) == False
  assert luna_lt(4, 3) == False
  assert luna_lt(3.5, 4.5) == True
  assert luna_lt(4.5, 4.5) == False
  assert luna_lt(4.5, 3.5) == False
  assert luna_lt([1], [1,2]) == True
  assert luna_lt([1],[1]) == False
  assert luna_lt([1,2],[1]) == False  
  assert luna_lt(False, True) == True
  assert luna_lt(True, True) == False
  assert luna_lt(False, False) == False
  assert luna_lt(True, False) == False  
  with pytest.raises(Exception):
    assert luna_lt({}, {})

def test_gt():
  assert luna_gt("a", "aa") == False
  assert luna_gt("aa", "aa") == False
  assert luna_gt("aa", "a") == True
  assert luna_gt(3, 4) == False
  assert luna_gt(4, 4) == False
  assert luna_gt(4, 3) == True
  assert luna_gt(3.5, 4.5) == False
  assert luna_gt(4.5, 4.5) == False
  assert luna_gt(4.5, 3.5) == True
  assert luna_gt([1], [1,2]) == False
  assert luna_gt([1],[1]) == False
  assert luna_gt([1,2],[1]) == True  
  assert luna_gt(False, True) == False
  assert luna_gt(True, True) == False
  assert luna_gt(False, False) == False
  assert luna_gt(True, False) == True  
  with pytest.raises(Exception):
    assert luna_gt({}, {})

def test_lte():
  assert luna_lte("a", "aa") == True
  assert luna_lte("aa", "aa") == True
  assert luna_lte("aa", "a") == False
  assert luna_lte(3, 4) == True
  assert luna_lte(4, 4) == True
  assert luna_lte(4, 3) == False
  assert luna_lte(3.5, 4.5) == True
  assert luna_lte(4.5, 4.5) == True
  assert luna_lte(4.5, 3.5) == False
  assert luna_lte([1], [1,2]) == True
  assert luna_lte([1],[1]) == True
  assert luna_lte([1,2],[1]) == False  
  assert luna_lte(False, True) == True
  assert luna_lte(True, True) == True
  assert luna_lte(False, False) == True
  assert luna_lte(True, False) == False  
  with pytest.raises(Exception):
    assert luna_lte({}, {})

def test_gte():
  assert luna_gte("a", "aa") == False
  assert luna_gte("aa", "aa") == True
  assert luna_gte("aa", "a") == True
  assert luna_gte(3, 4) == False
  assert luna_gte(4, 4) == True
  assert luna_gte(4, 3) == True
  assert luna_gte(3.5, 4.5) == False
  assert luna_gte(4.5, 4.5) == True
  assert luna_gte(4.5, 3.5) == True
  assert luna_gte([1], [1,2]) == False
  assert luna_gte([1],[1]) == True
  assert luna_gte([1,2],[1]) == True  
  assert luna_gte(False, True) == False
  assert luna_gte(True, True) == True
  assert luna_gte(False, False) == True
  assert luna_gte(True, False) == True
  with pytest.raises(Exception):
    assert luna_gte({}, {})

def test_lt_all():
  assert luna_lt_all([]) == False 
  assert luna_lt_all([1]) == True
  assert luna_lt_all(["a", "aa","aaa"]) == True
  assert luna_lt_all(["aa", "aa","aa"]) == False
  assert luna_lt_all(["aaa", "aa","a"]) == False
  assert luna_lt_all([3, 4,5]) == True
  assert luna_lt_all([4, 4,4]) == False
  assert luna_lt_all([4, 3,2]) == False
  assert luna_lt_all([3.5, 4.5,5.5]) == True
  assert luna_lt_all([4.5, 4.5,4.5]) == False
  assert luna_lt_all([4.5, 3.5,2.5]) == False
  assert luna_lt_all([[1], [1,2],[1,2,3]]) == True
  assert luna_lt_all([[1],[1],[1]]) == False
  assert luna_lt_all([[1,2,3],[1,2],[1]]) == False  
  assert luna_lt_all([False, True]) == True
  assert luna_lt_all([True, True]) == False
  assert luna_lt_all([False, False]) == False
  assert luna_lt_all([True, False]) == False 
  with pytest.raises(Exception):
    assert luna_lt_all([{}, {}])

def test_gt_all():
  assert luna_gt_all([]) == False 
  assert luna_gt_all([1]) == True
  assert luna_gt_all(["a", "aa","aaa"]) == False
  assert luna_gt_all(["aa", "aa","aa"]) == False
  assert luna_gt_all(["aaa", "aa","a"]) == True
  assert luna_gt_all([3, 4,5]) == False
  assert luna_gt_all([4, 4,4]) == False
  assert luna_gt_all([4, 3,2]) == True
  assert luna_gt_all([3.5, 4.5,5.5]) == False
  assert luna_gt_all([4.5, 4.5,4.5]) == False
  assert luna_gt_all([4.5, 3.5,2.5]) == True
  assert luna_gt_all([[1], [1,2],[1,2,3]]) == False
  assert luna_gt_all([[1],[1],[1]]) == False
  assert luna_gt_all([[1,2,3],[1,2],[1]]) == True
  assert luna_gt_all([False, True]) == False
  assert luna_gt_all([True, True]) == False
  assert luna_gt_all([False, False]) == False
  assert luna_gt_all([True, False]) == True
  with pytest.raises(Exception):
    assert luna_gt_all([{}, {}])

def test_lte_all():
  assert luna_lte_all([]) == False 
  assert luna_lte_all([1]) == True
  assert luna_lte_all(["a", "aa","aaa"]) == True
  assert luna_lte_all(["aa", "aa","aa"]) == True
  assert luna_lte_all(["aaa", "aa","a"]) == False
  assert luna_lte_all([3, 4,5]) == True
  assert luna_lte_all([4, 4,4]) == True
  assert luna_lte_all([4, 3,2]) == False
  assert luna_lte_all([3.5, 4.5,5.5]) == True
  assert luna_lte_all([4.5, 4.5,4.5]) == True
  assert luna_lte_all([4.5, 3.5,2.5]) == False
  assert luna_lte_all([[1], [1,2],[1,2,3]]) == True
  assert luna_lte_all([[1],[1],[1]]) == True
  assert luna_lte_all([[1,2,3],[1,2],[1]]) == False
  assert luna_lte_all([False, True]) == True
  assert luna_lte_all([True, True]) == True
  assert luna_lte_all([False, False]) == True
  assert luna_lte_all([True, False]) == False
  with pytest.raises(Exception):
    assert luna_lte_all([{}, {}])

def test_gte_all():
  assert luna_gte_all([]) == False 
  assert luna_gte_all([1]) == True
  assert luna_gte_all(["a", "aa","aaa"]) == False
  assert luna_gte_all(["aa", "aa","aa"]) == True
  assert luna_gte_all(["aaa", "aa","a"]) == True
  assert luna_gte_all([3, 4,5]) == False
  assert luna_gte_all([4, 4,4]) == True
  assert luna_gte_all([4, 3,2]) == True
  assert luna_gte_all([3.5, 4.5,5.5]) == False
  assert luna_gte_all([4.5, 4.5,4.5]) == True
  assert luna_gte_all([4.5, 3.5,2.5]) == True
  assert luna_gte_all([[1], [1,2],[1,2,3]]) == False
  assert luna_gte_all([[1],[1],[1]]) == True
  assert luna_gte_all([[1,2,3],[1,2],[1]]) == True
  assert luna_gte_all([False, True]) == False
  assert luna_gte_all([True, True]) == True
  assert luna_gte_all([False, False]) == True
  assert luna_gte_all([True, False]) == True 
  with pytest.raises(Exception):
    assert luna_gte_all([{}, {}])
