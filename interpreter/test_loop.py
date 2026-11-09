# test_loop.py

from .expressions import *
from .eval import luna_eval
import pytest

def test_loop_number_iterable():
  p = Program([
    VarSet("a", 0),
    Loop(
      3,
      Program([VarSet("a", Sum([VarGet("a"), 2]))]),
      None,
      None,
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == 6
  p = Program([
    VarSet("a", 0),
    Loop(
      3,
      Program([VarSet("a", Sum([VarGet("a"), VarGet("index")]))]),
      "item",
      "index",
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == 3
  p = Program([
    VarSet("a", 0),
    Loop(
      3,
      Program([VarSet("a", Sum([VarGet("a"), VarGet("item")]))]),
      "item",
      "index",
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == 3

def test_loop_string_iterable():
  p = Program([
    VarSet("a", 0),
    Loop(
      "abc",
      Program([VarSet("a", Sum([VarGet("a"), 2]))]),
      None,
      None,
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == 6
  p = Program([
    VarSet("a", 0),
    Loop(
      "abc",
      Program([VarSet("a", Sum([VarGet("a"), VarGet("index")]))]),
      "item",
      "index",
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == 3
  p = Program([
    VarSet("a", ""),
    Loop(
      "abc",
      Program([VarSet("a", Sum([VarGet("a"), VarGet("item")]))]),
      "item",
      "index",
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == "abc"

def test_loop_list_iterable():
  p = Program([
    VarSet("a", 0),
    Loop(
      ["a", "b", "c"],
      Program([VarSet("a", Sum([VarGet("a"), 2]))]),
      None,
      None,
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == 6
  p = Program([
    VarSet("a", 0),
    Loop(
      ["a", "b", "c"],
      Program([VarSet("a", Sum([VarGet("a"), VarGet("index")]))]),
      "item",
      "index",
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == 3
  p = Program([
    VarSet("a", ""),
    Loop(
      ["a", "b", "c"],
      Program([VarSet("a", Sum([VarGet("a"), VarGet("item")]))]),
      "item",
      "index",
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == "abc"

def test_list_iterable():
  p = Program([
    VarSet("a", 0),
    Loop(
      ["a", "b", "c"],
      Program([VarSet("a", Sum([VarGet("a"), 2]))]),
      None,
      None,
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == 6
  p = Program([
    VarSet("a", 0),
    Loop(
      ["a", "b", "c"],
      Program([VarSet("a", Sum([VarGet("a"), VarGet("index")]))]),
      "item",
      "index",
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == 3
  p = Program([
    VarSet("a", ""),
    Loop(
      ["a", "b", "c"],
      Program([VarSet("a", Sum([VarGet("a"), VarGet("item")]))]),
      "item",
      "index",
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == "abc"

def test_cant_continue_break_outside_loop():
  p1 = Program([
    VarSet("a", 0),
    Break(),
    VarGet("a")
  ])
  p2 = Program([
    VarSet("a", 0),
    Continue(),
    VarGet("a")
  ])
  with pytest.raises(Exception):
    assert luna_eval(p1) == 0
  with pytest.raises(Exception):
    assert luna_eval(p2) == 0
  with pytest.raises(Exception):
    assert luna_eval(Break()) == 0
  with pytest.raises(Exception):
    assert luna_eval(Continue()) == 0

def test_loop_break():
  p = Program([
    VarSet("a", 0),
    Loop(
      ["a", "b", "c"],
      Program([
        VarSet("a", Sum([VarGet("a"), 2])),
        Break(),
        VarSet("a", Sum([VarGet("a"), 100]))
      ]),
      None,
      None,
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == 2

def test_loop_continue():
  p = Program([
    VarSet("a", 0),
    Loop(
      ["a", "b", "c"],
      Program([
        VarSet("a", Sum([VarGet("a"), 2])),
        Continue(),
        VarSet("a", Sum([VarGet("a"), 100]))
      ]),
      None,
      None,
    ),
    VarGet("a")
  ])
  assert luna_eval(p) == 6

def test_loop_return_can_return_outer_function():
  fn = Function(
    [],
    Program([
      Loop(
        ["a", "b", "c"],
        Program([
          VarSet("a", Sum([VarGet("a"), 1])),
          Return(VarGet("a")),
          VarSet("a", Sum([VarGet("a"), 100]))
        ]),
        None,
        None,
      )
    ])
  )
  p = Program([
    VarSet("fn", fn),
    VarSet("a", 0),
    VarSet("a", Invoke(VarGet("fn"), [])),
    VarGet("a")
  ])
  assert luna_eval(p) == 1

def test_cant_break_continue_inside_fn_outside_loop():
  break_fn = Function(
    [],
    Program([Break()])
  )
  continue_fn = Function(
    [],
    Program([Break()])
  )
  p_break = Program([
    VarSet("a", 0),
    Loop(
      ["a", "b", "c"],
      Program([
        VarSet("a", Sum([VarGet("a"), 1])),
        Invoke(break_fn, []),
        VarSet("a", Sum([VarGet("a"), 1]))
      ]),
      None,
      None,
    ),
    VarGet("a")
  ])
  p_continue = Program([
    VarSet("a", 0),
    Loop(
      ["a", "b", "c"],
      Program([
        VarSet("a", Sum([VarGet("a"), 1])),
        Invoke(continue_fn, []),
        VarSet("a", Sum([VarGet("a"), 1]))
      ]),
      None,
      None,
    ),
    VarGet("a")
  ])
  with pytest.raises(Exception):
    assert luna_eval(p_continue)
  with pytest.raises(Exception):
    assert luna_eval(p_break)
