# test_eval_switch.py

from expressions import *
from eval import luna_eval
import pytest

def test_switch_basic():
  sc = Invoke(Frozen(Switch(
    2,
    [1,2,3],
    ["one","two","three"],
    "default"
  )), [])
  assert luna_eval(sc) == "two"

def test_switch_default():
  sc = Invoke(Frozen(Switch(
    4,
    [1,2,3],
    ["one","two","three"],
    "default"
  )), [])
  assert luna_eval(sc) == "default"

def test_switch_nesting():
  sc = Invoke(Frozen(Switch(
    Invoke(Frozen(Switch(
      2,
      [1,2,3],
      ["one","two","three"],
      "default"
    )), []),
    ["one","two","three"],
    ["fail","success","fail"],
    "default"
  )), [])
  assert luna_eval(sc) == "success"

def test_switch_composition():
  assert luna_eval(Block([
    VarSet("my_switch", Frozen(Switch(
      2,
      [1,2,3],
      ["one","two","three"],
      "default"
    ))),
    VarSet("two_variable", Invoke(VarGet("my_switch"), [])),
    VarGet("two_variable")
  ])) == "two"

def test_switch_variable_lookup_context():
  assert luna_eval(Block([
    VarSet("my_switch", Frozen(Switch(
      VarGet("a"),
      [1,2,3,99],
      ["one","two","three","ninetynine"],
      "default"
    ))),
    VarSet("a", 99),
    VarSet("result", Invoke(VarGet("my_switch"), [])),
    VarGet("result")
  ])) == "ninetynine"
