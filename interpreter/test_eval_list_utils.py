# test_eval_list_utils.py

from .expressions import *
from .eval import luna_eval
import pytest

def test_eval_lmap():
  fn = Function(["i"], Program([Product([VarGet("i"),2])]))
  assert luna_eval(Lmap([1,2,3], fn)) == [2,4,6]
