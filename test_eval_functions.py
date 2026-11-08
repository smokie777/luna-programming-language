# test_eval_functions.py

from expressions import *
from eval import luna_eval
import pytest

fn = Function(
  ["a", "b"],
  Block([Sum([VarGet("a"), VarGet("b")])])
)
ffn = Frozen(fn)
def test_can_set_and_get_function():
  assert luna_eval(VarSet("add_two", ffn)) == fn
  assert luna_eval(Block([
    VarSet("add_two", ffn),
    VarGet("add_two")
   ])) == fn
    
def test_function_execution():
  program = Block([
    VarSet("add_two", ffn),
    Invoke(fn, [1, 2])
  ])
  assert luna_eval(program) == 3

def test_function_execution_with_var_lookup():
  program = Block([
    VarSet("add_two", ffn),
    Invoke(VarGet("add_two"), [1, 2])
  ])
  assert luna_eval(program) == 3

def test_function_execution_dynamic_args():
  program = Block([
    VarSet("add_two", fn),
    Invoke(
      VarGet("add_two"),
      [
        Invoke(VarGet("add_two"), [1, 2]),
        Invoke(VarGet("add_two"), [3, 4])
      ],
    )
  ])
  assert luna_eval(program) == 10

def test_function_call_invalid_args_or_fn():
  p1 = Block([
    VarSet("add_two", fn),
    Invoke(VarGet("add_two"), [1])
  ])
  p2 = Block([
    VarSet("add_two", fn),
    Invoke(VarGet("add_two"), 1)
  ])
  with pytest.raises(Exception):
    assert luna_eval(p1)
  with pytest.raises(Exception):
    assert luna_eval(p2)

def test_scopes():
  p1 = Block([
    VarSet("add_two", fn),
    VarSet("a", 1),
    VarSet("b", 2),
    Invoke(
      VarGet("add_two"),
      [VarGet("a"), VarGet("b")],
    )
  ])
  assert luna_eval(p1) == 3

  set_inner = Frozen(Function(
    ["val"],
    Block([VarSet("a", VarGet("val"))])
  ))
  p2 = Block([
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
  return_two = Frozen(Function(
    [],
    Block([
      VarSet("a", 2),
      Return(VarGet("a")),
      VarSet("a", 4),
    ])
  ))
  program = Block([
    VarSet("return_two", return_two),
    Invoke(
      VarGet("return_two"),
      [],
    )
  ])
  assert luna_eval(program) == 2


def test_function_nested_return():
  inner_fn = Frozen(Function(
    [],
    Block([Return(2)])
  ))
  outer_fn = Frozen(Function(
    [],
    Block([
      Invoke(
        VarGet("inner_fn"),
        [],
      ),
      Return(3)
    ])
  ))
  program = Block([
    VarSet("inner_fn", inner_fn),
    VarSet("outer_fn", outer_fn),
    VarSet("three", 0),
    VarSet("three", Invoke(
      VarGet("outer_fn"),
      [],
    )),
    VarGet("three")
  ])
  assert luna_eval(program) == 3

# # I need a Switch to finish this function
# def test_recursion_using_factorial():
#   factorial = Function(
#     ["n"],
#     Block([
#       All([Equals([2, VarGet("n")])])
#     ])
#   )
