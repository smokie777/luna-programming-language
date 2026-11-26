# test_parse_list_utils.py

import pytest
from .luna_parse import luna_parse
from interpreter.expressions import *
from interpreter.operators import *
from tokenizer.luna_tokenize import luna_tokenize
from .test_parse import assert_parse_expr_tokens

def test_parse_lmap():
  assert_parse_expr_tokens(
    "lmap([1,2], f(i){i*2})",
    Lmap(
      [1,2],
      Function(["i"], Program([Product([VarGet("i"),2])]))
    )
  )

def test_parse_filter():
  assert_parse_expr_tokens(
    "filter([1,2], f(i){i=2})",
    Filter(
      [1,2],
      Function(["i"], Program([Equals([VarGet("i"),2])]))
    )
  )

def test_parse_insert():
  assert_parse_expr_tokens(
    "insert([1,2], 3)",
    Insert([1,2], 3, None)
  )
  assert_parse_expr_tokens(
    "insert([1,2], 3, 1)",
    Insert([1,2], 3, 1)
  )

def test_parse_insert():
  assert_parse_expr_tokens(
    "insert([1,2], 3)",
    Insert([1,2], 3, None)
  )
  assert_parse_expr_tokens(
    "insert([1,2], 3, 1)",
    Insert([1,2], 3, 1)
  )

def test_parse_get():
  assert_parse_expr_tokens(
    "get([1,2], 1)",
    Get([1,2], 1)
  )

def test_parse_find():
  assert_parse_expr_tokens(
    "find([1,2], f(i){i=2})",
    Find([1,2], Function(["i"], Program([Equals([VarGet("i"),2])])))
  )

def test_parse_findindex():
  assert_parse_expr_tokens(
    "findindex([1,2], 2)",
    FindIndex([1,2], 2)
  )

def test_parse_slice():
  assert_parse_expr_tokens(
    "slice([1,2], 1)",
    Slice([1,2], 1, None)
  )
  assert_parse_expr_tokens(
    "slice([1,2], 1, 2)",
    Slice([1,2], 1, 2)
  )
