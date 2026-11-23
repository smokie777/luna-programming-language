# test_eval_switch.py

from .expressions import *
from .eval import luna_eval
import pytest

def test_if_then_else():
  t = "true result"
  f = "false result"
  assert luna_eval(IfThenElse(True, t, f)) == t
  assert luna_eval(IfThenElse("truthy", t, f)) == t
  assert luna_eval(IfThenElse(False, t, f)) == f
  assert luna_eval(IfThenElse(0, t, f)) == f
  assert luna_eval(IfThenElse(True, None, f)) == False
  assert luna_eval(IfThenElse(False, None, f)) == f
  assert luna_eval(IfThenElse(True, t, None)) == t
  assert luna_eval(IfThenElse(False, f, None)) == False

def test_switch_basic():
  sc = Switch(
    2,
    [1,2,3],
    ["one","two","three"]
  )
  assert luna_eval(sc) == "two"

def test_switch_default():
  sc = Switch(
    4,
    [1,SwitchCatchAllCase(),3],
    ["one","two","three"]
  )
  assert luna_eval(sc) == "two"

def test_switch_multi_case_match_first_wins():
  sc = Switch(
    4,
    [3,4,4],
    ["one","two","three"]
  )
  assert luna_eval(sc) == "two"

def test_switch_non_visited_cases_no_eval():
  p = Program([
    VarSet("a", 0),
    Switch(
      4,
      [3,4,VarSet("a", Sum([VarGet("a"), 100]))],
      [
        "three",
        "four",
        "varset"
      ]
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == 0

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
      ]
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
    ["fail","success","fail"]
  )
  assert luna_eval(sc) == "success"

def test_switch_composition():
  assert luna_eval(Program([
    VarSet("my_switch", Frozen(Switch(
      2,
      [1,2,3],
      ["one","two","three"]
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
      ["one","two","three","ninetynine"]
    ))),
    VarSet("a", 99),
    VarSet("result", VarGet("my_switch")),
    Invoke(VarGet("result"))
  ])) == "ninetynine"
