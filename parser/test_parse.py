# test_parse.py

import pytest
from .luna_parse import luna_parse
from interpreter.expressions import *
from interpreter.operators import *
from tokenizer.luna_tokenize import luna_tokenize

def assert_parse_expr_tokens(source, expected):
  assert luna_parse(luna_tokenize(source)) == Program([expected])

def test_parse_ternary():
  assert_parse_expr_tokens("3 >> 'three' !> 'not three'", IfThenElse( 
    3, "three", "not three"
  ))
  with pytest.raises(Exception):
    luna_parse(luna_tokenize("3 >> 'three'"))
  with pytest.raises(Exception):
    luna_parse(luna_tokenize("3 !> 'three'"))

def test_parse_ifthenelse():
  assert_parse_expr_tokens("if(3){'three'}", IfThenElse(
    3, Program(["three"]), None
  ))
  assert_parse_expr_tokens("if(3){'three'}else{'notthree'}", IfThenElse(
    3, Program(["three"]), Program(["notthree"])
  ))

def test_parse_or():
  assert_parse_expr_tokens("3 | 4", Some([3,4])) 
  assert_parse_expr_tokens("3 | 4 | 5", Some([3,4,5])) 

def test_parse_and():
  assert_parse_expr_tokens("3 & 4", All([3,4])) 
  assert_parse_expr_tokens("3 & 4 & 5", All([3,4,5])) 

def test_parse_equality():
  assert_parse_expr_tokens("3 < 4", Lt([3, 4]))
  assert_parse_expr_tokens("3 < 4 < 5", Lt([3, 4, 5]))
  assert_parse_expr_tokens("3 <= 4", Lte([3, 4]))
  assert_parse_expr_tokens("3 <= 4 <= 5", Lte([3, 4, 5]))
  assert_parse_expr_tokens("3 > 4", Gt([3, 4]))
  assert_parse_expr_tokens("3 > 4 > 5", Gt([3, 4, 5]))
  assert_parse_expr_tokens("3 >= 4", Gte([3, 4]))
  assert_parse_expr_tokens("3 >= 4 >= 5", Gte([3, 4, 5]))
  assert_parse_expr_tokens("3 = 4", Equals([3, 4]))
  assert_parse_expr_tokens("3 = 4 = 5", Equals([3, 4, 5]))

def test_parse_addition():
  assert_parse_expr_tokens("3 + 4", Sum([3,4])) 
  assert_parse_expr_tokens("3 + 4 + 5", Sum([3,4,5])) 
  assert_parse_expr_tokens("3 - 4", Difference([3,4])) 
  assert_parse_expr_tokens("3 - 4 - 5", Difference([3,4,5])) 

def test_parse_multiplication():
  assert_parse_expr_tokens("3 * 4", Product([3,4])) 
  assert_parse_expr_tokens("3 * 4 * 5", Product([3,4,5])) 
  assert_parse_expr_tokens("3 / 4", Quotient([3,4])) 
  assert_parse_expr_tokens("3 / 4 / 5", Quotient([3,4,5])) 
  assert_parse_expr_tokens("3 % 4", RemainderAll([3,4])) 
  assert_parse_expr_tokens("3 % 4 % 5", RemainderAll([3,4,5])) 

def test_parse_exponent():
  assert_parse_expr_tokens("3 ^ 4", Exponent([3,4])) 
  assert_parse_expr_tokens("3 ^ 4 ^ 5", Exponent([3,4,5])) 

def test_parse_inverse():
  assert_parse_expr_tokens("-3", Inverse(3))
  assert_parse_expr_tokens("---3", Inverse(Inverse(Inverse(3))))
  assert_parse_expr_tokens("3- -3", Difference([3, Inverse(3)]))

def test_parse_newlines():
  assert_parse_expr_tokens("3+(\n4+5\n)", Sum([3, Sum([4,5])])) 

def test_parse_operator_chain():
  assert_parse_expr_tokens(
    "3 >> 3 | 4 & 5 <= 6 + 7 * 8 ^ -9(10) !> 'not three'",
    IfThenElse(
      3,
      Some([
        3,
        All([
          4,
          EqualityChain([
            5,
            Sum([
              6,
              Product([
                7,
                Exponent([
                  8,
                  Inverse(
                    Invoke(9, [10])
                  )
                ])
              ])
            ])
          ], [EqualityOp.LTE])
        ])
      ]),
      "not three"
    )
  )

def test_parse_keyword_no_args():
  assert_parse_expr_tokens("true", True)
  assert_parse_expr_tokens("false", False)
  assert_parse_expr_tokens("continue", Continue())
  assert_parse_expr_tokens("break", Break())

def test_parse_keyword_with_args():
  assert_parse_expr_tokens("return", Return(False))
  assert_parse_expr_tokens("return(3)", Return(3))
  assert_parse_expr_tokens("return(3+4)", Return(Sum([3, 4])))
  assert_parse_expr_tokens("boolean(3)", ToBoolean(3))
  assert_parse_expr_tokens("boolean(3+4)", ToBoolean(Sum([3, 4])))
  assert_parse_expr_tokens("string(3)", ToString(3))
  assert_parse_expr_tokens("string(3+4)", ToString(Sum([3, 4])))
  assert_parse_expr_tokens("number(3)", ToNumber(3))
  assert_parse_expr_tokens("number(3+4)", ToNumber(Sum([3, 4])))
  assert_parse_expr_tokens("print(3)", Print(3))
  assert_parse_expr_tokens("print(3+4)", Print(Sum([3, 4])))

def test_parse_args():
  # enable once we can make fn with no args
  # assert_parse_expr_tokens("print(\n\n\n)", Print(Sum([3, 4])))
  with pytest.raises(Exception):
    assert_parse_expr_tokens("print(3,4)", Print(Sum([3, 4])))
  with pytest.raises(Exception):
    assert_parse_expr_tokens("print(3+4", Print(Sum([3, 4])))
  with pytest.raises(Exception):
    assert_parse_expr_tokens("print3+4)", Print(Sum([3, 4])))

def test_parse_varset():
  assert_parse_expr_tokens("-> x 4", VarSet("x", 4))
  assert_parse_expr_tokens("-> x 3 + 4", VarSet("x", Sum([3, 4])))
  assert_parse_expr_tokens("=> x 4", VarSetGlobal("x", 4))

def test_parse_freeze():
  assert_parse_expr_tokens("<>print(3)", Frozen(Print(3)))

def test_parse_program():
  assert_parse_expr_tokens("{3}", Program([3]))
  assert_parse_expr_tokens("{3+4}", Program([Sum([3,4])]))
  assert_parse_expr_tokens("{3\n4}", Program([3, 4]))
  with pytest.raises(Exception):
    luna_parse(luna_tokenize("{3 3}"))

def test_parse_function():
  assert_parse_expr_tokens("function(){}", Function([], Program([])))
  assert_parse_expr_tokens("function(arg){4}", Function(["arg"], Program([4])))

def test_parse_loop():
  assert_parse_expr_tokens("loop(3){4}", Loop(3, None, None, Program([4])))
  assert_parse_expr_tokens("loop(3, item){4}", Loop(3, "item", None, Program([4])))
  assert_parse_expr_tokens("loop(3, item, idx){4}", Loop(3, "item", "idx", Program([4])))

def test_parse_invalid_chars_after_expr():
  with pytest.raises(Exception):
    luna_parse(luna_tokenize("3 3"))

def test_parse_list():
  assert_parse_expr_tokens("[]", [])
  assert_parse_expr_tokens("[1,2,3]", [1,2,3])
  assert_parse_expr_tokens("[1,2,3+4]", [1,2,Sum([3,4])])

def test_parse_map():
  assert_parse_expr_tokens("map()", Map([]))
  assert_parse_expr_tokens("map([1,2])", Map([[1,2]]))
  assert_parse_expr_tokens("map([1,2],[3,4])", Map([[1,2],[3,4]]))

def test_parse_switch():
  assert_parse_expr_tokens(
    "switch(3+4)`6:'six',7:'seven'`",
    Switch(Sum([3, 4]), [6, 7], ["six", "seven"])
  )
  assert_parse_expr_tokens(
    "switch(3+4)`6:'six',7:'seven',_:'default_branch'`",
    Switch(Sum([3, 4]), [6, 7, SwitchCatchAllCase()], ["six", "seven", "default_branch"])
  )
  assert_parse_expr_tokens(
    """
    switch(3+4)`
      6: 'six',
      7:'seven',
      _:'default_branch'
    `
    """,
    Switch(Sum([3, 4]), [6, 7, SwitchCatchAllCase()], ["six", "seven", "default_branch"])
  )
  
def test_parse_invocation():
  assert_parse_expr_tokens("x()", Invoke(VarGet("x"), []))
  assert_parse_expr_tokens("x(1, 2, 3)", Invoke(VarGet("x"), [1, 2, 3]))
  assert_parse_expr_tokens("function(arg){4}()", Invoke(Function(["arg"], Program([4]))))
  assert_parse_expr_tokens("x()()()", Invoke(Invoke(Invoke(VarGet("x"), []), []), []))

def test_parse_program_newlines():
  assert_parse_expr_tokens("1+\n2", Sum([1, 2]))
  assert luna_parse(luna_tokenize("1+2\n3+4")) == Program([Sum([1, 2]), Sum([3, 4])])
  # assert_parse_expr_tokens("{\n1\n2\n}", Program([1, 2]))
