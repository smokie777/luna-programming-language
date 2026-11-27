# test_inequality.py

import pytest
from ..inequality import *
from ..expressions import Map

map1 = Map([["a", 1]])
map2 = Map([["a", 1], ["b", 2]])

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
  assert luna_lt(map1, map1) == False
  assert luna_lt(map1, map2) == True
  assert luna_lt(map2, map1) == False
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
  assert luna_gt(map1, map1) == False
  assert luna_gt(map1, map2) == False
  assert luna_gt(map2, map1) == True
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
  assert luna_lte(map1, map1) == True
  assert luna_lte(map1, map2) == True
  assert luna_lte(map2, map1) == False
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
  assert luna_gte(map1, map1) == True
  assert luna_gte(map1, map2) == False
  assert luna_gte(map2, map1) == True
  with pytest.raises(Exception):
    assert luna_gte({}, {})
