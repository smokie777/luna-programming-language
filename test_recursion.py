# test_eval_functions.py

from expressions import *
from eval import luna_eval
import pytest

def test_recursion_factorial():
  fact = Function(
    ["n"],
    Program([
      Switch(
        Lte([VarGet("n"), 2]),
        [True, False],
        [
          Return(VarGet("n")),
          Return(Product([
            VarGet("n"),
            Invoke(VarGet("fact"), [Difference([VarGet("n"), 1])])
          ]))
        ],
      )
    ])
  )
  p = Program([
    VarSet("fact", fact),
    Invoke(VarGet("fact"), [4])
  ])
  assert luna_eval(p) == 24
