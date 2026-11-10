# test_eval_functions.py

from .expressions import *
from .eval import luna_eval
import pytest

fn = Function(
  ["a", "b"],
  Program([Sum([VarGet("a"), VarGet("b")])])
)

def test_can_set_and_get_function():
  assert luna_eval(VarSet("add_two", fn)) == fn
  assert luna_eval(Program([
    VarSet("add_two", fn),
    VarGet("add_two")
   ])) == fn
    
def test_function_execution():
  p = Program([
    Invoke(fn, [1, 2])
  ])
  assert luna_eval(p) == 3

def test_function_execution_with_var_lookup():
  p = Program([
    VarSet("add_two", fn),
    Invoke(VarGet("add_two"), [1, 2])
  ])
  assert luna_eval(p) == 3

def test_function_execution_dynamic_args():
  p = Program([
    VarSet("add_two", fn),
    Invoke(
      VarGet("add_two"),
      [
        Invoke(VarGet("add_two"), [1, 2]),
        Invoke(VarGet("add_two"), [3, 4])
      ],
    )
  ])
  assert luna_eval(p) == 10

def test_function_call_invalid_args_or_fn():
  p1 = Program([
    VarSet("add_two", fn),
    Invoke(VarGet("add_two"), [1])
  ])
  p2 = Program([
    VarSet("add_two", fn),
    Invoke(VarGet("add_two"), 1)
  ])
  with pytest.raises(Exception):
    assert luna_eval(p1)
  with pytest.raises(Exception):
    assert luna_eval(p2)

def test_scopes():
  p1 = Program([
    VarSet("add_two", fn),
    VarSet("a", 1),
    VarSet("b", 2),
    Invoke(
      VarGet("add_two"),
      [VarGet("a"), VarGet("b")],
    )
  ])
  assert luna_eval(p1) == 3

  set_inner = Function(
    ["val"],
    Program([VarSet("a", VarGet("val"))])
  )
  p2 = Program([
    VarSet("set_inner", set_inner),
    VarSet("a", 1),
    Invoke(
      VarGet("set_inner"),
      [9],
    ),
    VarGet("a")
  ])
  assert luna_eval(p2) == 1

def test_function_return():
  return_two = Function(
    [],
    Program([
      VarSet("a", 2),
      Return(VarGet("a")),
      VarSet("a", 4),
    ])
  )
  p = Program([
    VarSet("return_two", return_two),
    Invoke(
      VarGet("return_two"),
      [],
    )
  ])
  assert luna_eval(p) == 2

def test_function_nested_return():
  inner_fn = Function(
    [],
    Program([Return(2)])
  )
  outer_fn = Function(
    [],
    Program([
      Invoke(
        VarGet("inner_fn"),
        [],
      ),
      Return(3)
    ])
  )
  p = Program([
    VarSet("inner_fn", inner_fn),
    VarSet("outer_fn", outer_fn),
    VarSet("three", 0),
    VarSet("three", Invoke(
      VarGet("outer_fn"),
      [],
    )),
    VarGet("three")
  ])
  assert luna_eval(p) == 3

def test_var_set_global():
  p = Program([
    VarSet("a", 1),
    Invoke(Function(
      [],
      Program([VarSetGlobal("a", 3)])
    )),
    VarGet("a")
  ])
  assert luna_eval(p) == 3
  p1 = Program([
    Invoke(Function(
      [],
      Program([
        VarSetGlobal("a", 3),
        VarGet("a")
      ])
    )),
  ])
  assert luna_eval(p) == 3
