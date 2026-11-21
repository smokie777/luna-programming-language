# test_parse.py

import pytest
from .luna_parse import luna_parse
from interpreter.expressions import *
from tokenizer.luna_tokenize import luna_tokenize

def test_parse_if():
  assert luna_parse(luna_tokenize("3 >> 'three' !> 'not three'")) == IfThenElse(
    3, "three", "not three"
  )
  assert luna_parse(luna_tokenize("3 >> 'three'")) == IfThenElse(
    3, "three", None
  )
  assert luna_parse(luna_tokenize("3 !> 'not three'")) == IfThenElse(
    3, None, "not three"
  )

def test_parse_or():
  assert luna_parse(luna_tokenize("3 | 4")) == Some([3,4])
  assert luna_parse(luna_tokenize("3 | 4 | 5")) == Some([3,4,5])

def test_parse_and():
  assert luna_parse(luna_tokenize("3 & 4")) == All([3,4])
  assert luna_parse(luna_tokenize("3 & 4 & 5")) == All([3,4,5])

def test_parse_equality():
  assert luna_parse(luna_tokenize("3 < 4")) == Lt([3,4])
  assert luna_parse(luna_tokenize("3 < 4 < 5")) == Lt([3,4,5])
  assert luna_parse(luna_tokenize("3 <= 4")) == Lte([3,4])
  assert luna_parse(luna_tokenize("3 <= 4 <= 5")) == Lte([3,4,5])  
  assert luna_parse(luna_tokenize("3 > 4")) == Gt([3,4])
  assert luna_parse(luna_tokenize("3 > 4 > 5")) == Gt([3,4,5])
  assert luna_parse(luna_tokenize("3 >= 4")) == Gte([3,4])
  assert luna_parse(luna_tokenize("3 >= 4 >= 5")) == Gte([3,4,5])  
  assert luna_parse(luna_tokenize("3 = 4")) == Equals([3,4])
  assert luna_parse(luna_tokenize("3 = 4 = 5")) == Equals([3,4,5])

def test_parse_addition():
  assert luna_parse(luna_tokenize("3 + 4")) == Sum([3,4])
  assert luna_parse(luna_tokenize("3 + 4 + 5")) == Sum([3,4,5])
  assert luna_parse(luna_tokenize("3 - 4")) == Difference([3,4])
  assert luna_parse(luna_tokenize("3 - 4 - 5")) == Difference([3,4,5])

def test_parse_multiplication():
  assert luna_parse(luna_tokenize("3 * 4")) == Product([3,4])
  assert luna_parse(luna_tokenize("3 * 4 * 5")) == Product([3,4,5])
  assert luna_parse(luna_tokenize("3 / 4")) == Quotient([3,4])
  assert luna_parse(luna_tokenize("3 / 4 / 5")) == Quotient([3,4,5])
  assert luna_parse(luna_tokenize("3 % 4")) == Remainder([3,4])
  assert luna_parse(luna_tokenize("3 % 4 % 5")) == Remainder([3,4,5])

def test_parse_exponent():
  assert luna_parse(luna_tokenize("3 ^ 4")) == Exponent([3,4])
  assert luna_parse(luna_tokenize("3 ^ 4 ^ 5")) == Exponent([3,4,5])

def test_parse_inverse():
  assert luna_parse(luna_tokenize("!3")) == Inverse(3)

def test_operator_chain():
  assert luna_parse(luna_tokenize(
    "3 >> 3 | 4 & 5 <= 6 + 7 * 8 ^ !9 !> 'not three'"
  )) == IfThenElse(
    3,
    Some([
      3,
      All([
        4,
        Lte([
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
        ])
      ])
    ]),
    "not three"
  )
  