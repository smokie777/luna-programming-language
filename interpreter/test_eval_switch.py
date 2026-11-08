# test_eval_switch.py

from .expressions import *
from .eval import luna_eval
import pytest

def test_switch_basic():
  sc = Switch(
    2,
    [1,2,3],
    ["one","two","three"],
    "default"
  )
  assert luna_eval(sc) == "two"

def test_switch_default():
  sc = Switch(
    4,
    [1,2,3],
    ["one","two","three"],
    "default"
  )
  assert luna_eval(sc) == "default"

def test_switch_multi_case_match_first_wins():
  sc = Switch(
    4,
    [3,4,4],
    ["one","two","three"],
    "default"
  )
  assert luna_eval(sc) == "two"

def test_switch_non_visited_branches_no_eval():
  p = Program([
    VarSet("a", 0),
    Switch(
      4,
      [3,4,5],
      [
        VarSet("a", Sum([VarGet("a"), 1])),
        VarSet("a", Sum([VarGet("a"), 10])),
        VarSet("a", Sum([VarGet("a"), 100]))
      ],
      VarSet("a", Sum([VarGet("a"), 1000]))
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == 10

def test_switch_nesting():
  sc = Switch(
    Switch(
      2,
      [1,2,3],
      ["one","two","three"],
      "default"
    ),
    ["one","two","three"],
    ["fail","success","fail"],
    "default"
  )
  assert luna_eval(sc) == "success"

def test_switch_composition():
  assert luna_eval(Program([
    VarSet("my_switch", Frozen(Switch(
      2,
      [1,2,3],
      ["one","two","three"],
      "default"
    ))),
    VarSet("two_variable", VarGet("my_switch")),
    Invoke(VarGet("two_variable"))
  ])) == "two"

def test_switch_variable_lookup_context():
  assert luna_eval(Program([
    VarSet("a", 1),
    VarSet("my_switch", Frozen(Switch(
      VarGet("a"),
      [1,2,3,99],
      ["one","two","three","ninetynine"],
      "default"
    ))),
    VarSet("a", 99),
    VarSet("result", VarGet("my_switch")),
    Invoke(VarGet("result"))
  ])) == "ninetynine"
