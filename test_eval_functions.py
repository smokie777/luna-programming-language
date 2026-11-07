# test_eval_functions.py

from expressions import *
from eval import luna_eval
import pytest

fn = Function(
  ["a", "b"],
  Block([Sum([VarGet("a"), VarGet("b")])])
)
def test_can_set_and_get_function():
  assert luna_eval(VarSet("add_two", fn)) == fn
  assert luna_eval(Block([
    VarSet("add_two", fn),
    VarGet("add_two")
   ])) == fn
    
def test_function_execution():
  program = Block([
    VarSet("add_two", fn),
    FunctionCall(fn, L([V(1), V(2)]))
  ])
  assert luna_eval(program) == 3

def test_function_execution_with_var_lookup():
  program = Block([
    VarSet("add_two", fn),
    FunctionCall(VarGet("add_two"), L([V(1), V(2)]))
  ])
  assert luna_eval(program) == 3

def test_function_execution_dynamic_args():
  program = Block([
    VarSet("add_two", fn),
    FunctionCall(
      VarGet("add_two"),
      L([
        FunctionCall(VarGet("add_two"), L([V(1), V(2)])),
        FunctionCall(VarGet("add_two"), L([V(3), V(4)]))
      ]),
    )
  ])
  assert luna_eval(program) == 10

def test_function_call_invalid_args_or_fn():
  p1 = Block([
    VarSet("add_two", fn),
    FunctionCall(VarGet("add_two"), L([V(1)]))
  ])
  p2 = Block([
    VarSet("add_two", fn),
    FunctionCall(VarGet("add_two"), V(1))
  ])
  p3 = Block([
    FunctionCall(V(1), L([V(1)]))
  ])
  with pytest.raises(Exception):
    assert luna_eval(p1)
  with pytest.raises(Exception):
    assert luna_eval(p2)
  with pytest.raises(Exception):
    assert luna_eval(p3)

def test_scopes():
  p1 = Block([
    VarSet("add_two", fn),
    VarSet("a", V(1)),
    VarSet("b", V(2)),
    FunctionCall(
      VarGet("add_two"),
      L([VarGet("a"), VarGet("b")]),
    )
  ])
  assert luna_eval(p1) == 3

  set_inner = Function(
    ["val"],
    Block([VarSet("a", VarGet("val"))])
  )
  p2 = Block([
    VarSet("set_inner", set_inner),
    VarSet("a", V(1)),
    FunctionCall(
      VarGet("set_inner"),
      L([V(9)]),
    ),
    VarGet("a")
  ])
  assert luna_eval(p2) == 1

def test_function_return():
  return_two = Function(
    [],
    Block([
      VarSet("a", V(2)),
      Return(VarGet("a")),
      VarSet("a", V(4)),
    ])
  )
  program = Block([
    VarSet("return_two", return_two),
    FunctionCall(
      VarGet("return_two"),
      L([]),
    )
  ])
  assert luna_eval(program) == 2

# I need a Switch to finish this function
def test_recursion_using_factorial():
  factorial = Function(
    ["n"],
    Block([
      All([Equals([V(2),VarGet("n")])])
    ])
  )
