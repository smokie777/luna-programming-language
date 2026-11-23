# test_recursion.py

from .expressions import *
from .eval import luna_eval
import pytest

def test_recursion_factorial_switch():
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

def test_recursion_factorial_if():
  fact = Function(
    ["n"],
    Program([
      IfThenElse(
        Lte([VarGet("n"), 2]),
        VarGet("n"),
        Product([
          VarGet("n"),
          Invoke(VarGet("fact"), [Difference([VarGet("n"), 1])])
        ])
      )
    ])
  )
  p = Program([
    VarSet("fact", fact),
    Invoke(VarGet("fact"), [4])
  ])
  assert luna_eval(p) == 24
