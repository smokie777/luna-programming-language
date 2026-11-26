# test_eval_list_utils.py

from .expressions import *
from .luna_eval import luna_eval
import pytest

def test_eval_lmap():
  fn = Function(["i"], Program([Product([VarGet("i"),2])]))
  assert luna_eval(Lmap([], fn)) == []
  assert luna_eval(Lmap([1,2,3], fn)) == [2,4,6]

def test_eval_filter():
  fn = Function(["i"], Program([Equals([VarGet("i"),2])]))
  assert luna_eval(Filter([], fn)) == []
  assert luna_eval(Filter([1,2,3], fn)) == [2]

def test_eval_insert():
  def create_program(insert_expr):
    return Program([VarSet("a", [1,2,3]), insert_expr, VarGet("a")])
  cases = [
    (Insert(VarGet("a"), ["new"], None), [1,2,3,["new"]]),
    (Insert(VarGet("a"), 4, 0), [4,1,2,3]),
    (Insert(VarGet("a"), 4, -1), [4,1,2,3]),
    (Insert(VarGet("a"), 4, -2), [4,1,2,3]),
    (Insert(VarGet("a"), 4, 1), [1,4,2,3]),
    (Insert(VarGet("a"), 4, 2), [1,2,4,3]),
    (Insert(VarGet("a"), 4, 3), [1,2,3,4]),
    (Insert(VarGet("a"), 4, 4), [1,2,3,4]),
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert luna_eval(Insert([1,2,3], 4, 0)) == 4

def test_eval_pop():
  def create_program(pop_expr):
    return Program([VarSet("a", [1,2,3]), pop_expr, VarGet("a")])
  cases = [
    (Pop(VarGet("a"), -2), [2,3]),
    (Pop(VarGet("a"), -1), [2,3]),
    (Pop(VarGet("a"), 0), [2,3]),
    (Pop(VarGet("a"), 1), [1,3]),
    (Pop(VarGet("a"), 2), [1,2]),
    (Pop(VarGet("a"), 3), [1,2]),
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert luna_eval(Pop([1,2,3], 1)) == 2

def test_eval_get():
  def create_program(get_expr):
    return Program([VarSet("a", [1,2,3]), get_expr])
  cases = [
    (Get(VarGet("a"), -2), 1),
    (Get(VarGet("a"), -1), 1),
    (Get(VarGet("a"), 0), 1),
    (Get(VarGet("a"), 1), 2),
    (Get(VarGet("a"), 2), 3),
    (Get(VarGet("a"), 3), 3),
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert luna_eval(Program([VarSet("a", [1,2,3]), Get(VarGet("a"), 0), VarGet("a")])) == [1,2,3]

def test_eval_getindex():
  def create_program(getindex_expr):
    return Program([VarSet("a", [1,2,3]), getindex_expr])
  cases = [
    (GetIndex(VarGet("a"), 3), 2),
    (GetIndex(VarGet("a"), 4), False),
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert luna_eval(
    Program([
      VarSet("a", [1,2,3]),
      GetIndex(VarGet("a"), 3),
      VarGet("a")
    ])) == [1,2,3]

def test_eval_find():
  def create_program(find_expr):
    return Program([VarSet("a", [1,2,3]), find_expr])
  cases = [
    (Find(VarGet("a"), Function(["i"], Program([Equals([VarGet("i"), 2])]))), 2),
    (Find(VarGet("a"), Function(["i"], Program([Equals([VarGet("i"), 4])]))), False),
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert luna_eval(
    Program([
      VarSet("a", [1,2,3]),
      Find(VarGet("a"), Function(["i"], Program([Equals([VarGet("i"), 2])]))),
      VarGet("a")
    ])) == [1,2,3]
  assert luna_eval(Program([VarSet("a", [[1],[2],[3]]), 
    Find(VarGet("a"), Function(["i"], Program([
      Find(VarGet("i"), Function(["j"], Program([Equals([VarGet("j"), 2])])))
    ])))
  ])) == [2]

def test_eval_findindex():
  def create_program(findindex_expr):
    return Program([VarSet("a", [1,2,3]), findindex_expr])
  cases = [
    (FindIndex(VarGet("a"), Function(["i"], Program([Equals([VarGet("i"), 2])]))), 1),
    (FindIndex(VarGet("a"), Function(["i"], Program([Equals([VarGet("i"), 4])]))), False),
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert luna_eval(
    Program([
      VarSet("a", [1,2,3]),
      FindIndex(VarGet("a"), Function(["i"], Program([Equals([VarGet("i"), 2])]))),
      VarGet("a")
    ])) == [1,2,3]

def test_eval_slice():
  def create_program(slice_expr):
    return Program([VarSet("a", [1,2,3]), slice_expr])
  cases = [
    (Slice(VarGet("a"), 1, 1), []),
    (Slice(VarGet("a"), 0, 3), [1,2,3]),
    (Slice(VarGet("a"), -10, 10), [1,2,3]),
    (Slice(VarGet("a"), 1, 10), [2,3]),
    (Slice(VarGet("a"), -10, 2), [1,2]),
    (Slice(VarGet("a"), 1, 2), [2]),
    (Slice(VarGet("a"), 2, 1), [])
  ]
  for i, expected in cases:
    assert luna_eval(create_program(i)) == expected
  assert luna_eval(Program([VarSet("a", [1,2,3]), Slice(VarGet("a"), 1, 2), VarGet("a")])) == [1,2,3]
