# test_parse.py

import pytest
from .luna_parse import luna_parse
from interpreter.expressions import *
from interpreter.operators import *
from tokenizer.luna_tokenize import luna_tokenize

def assert_parse_expr_tokens(source, expected):
  assert luna_parse(luna_tokenize(source)) == Program([expected])

def test_parse_if():
  assert_parse_expr_tokens("3 >> 'three' !> 'not three'", IfThenElse( 
    3, "three", "not three"
  ))
  assert_parse_expr_tokens("3 >> 'three'", IfThenElse( 
    3, "three", None
  ))
  assert_parse_expr_tokens("3 !> 'not three'", IfThenElse( 
    3, None, "not three"
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

def test_parse_newlines():
  assert_parse_expr_tokens("3+(\n4+5\n)", Sum([3, Sum([4,5])])) 

def test_operator_chain():
  assert_parse_expr_tokens(
    "3 >> 3 | 4 & 5 <= 6 + 7 * 8 ^ -9 !> 'not three'",
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
                  Inverse(9)
                ])
              ])
            ])
          ], [EqualityOp.LTE])
        ])
      ]),
      "not three"
    )
  )
