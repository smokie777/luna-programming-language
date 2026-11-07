# test_eval_switch.py

from expressions import *
from eval import luna_eval
import pytest

def test_switch_basic():
  sc = SwitchCall(Switch(
    2,
    [1,2,3],
    SwitchBranches(["one","two","three"]),
    "default"
  ))
  assert luna_eval(sc) == "two"

def test_switch_default():
  sc = SwitchCall(Switch(
    4,
    [1,2,3],
    SwitchBranches(["one","two","three"]),
    "default"
  ))
  assert luna_eval(sc) == "default"

def test_switch_nesting():
  sc = SwitchCall(Switch(
    SwitchCall(Switch(
      2,
      [1,2,3],
      SwitchBranches(["one","two","three"]),
      "default"
    )),
    ["one","two","three"],
    SwitchBranches(["fail","success","fail"]),
    "default"
  ))
  assert luna_eval(sc) == "success"

def test_switch_composition():
  assert luna_eval(Block([
    VarSet("my_switch", Switch(
      2,
      [1,2,3],
      SwitchBranches(["one","two","three"]),
      "default"
    )),
    VarSet("two_variable", SwitchCall(VarGet("my_switch"))),
    VarGet("two_variable")
  ])) == "two"

def test_switch_variable_lookup_context():
  assert luna_eval(Block([
    VarSet("my_switch", Switch(
      VarGet("a"),
      [1,2,3,99],
      SwitchBranches(["one","two","three","ninetynine"]),
      "default"
    )),
    VarSet("a", 99),
    VarSet("result", SwitchCall(VarGet("my_switch"))),
    VarGet("result")
  ])) == "ninetynine"
