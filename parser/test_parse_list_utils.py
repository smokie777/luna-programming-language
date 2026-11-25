# test_parse_list_utils.py

import pytest
from .luna_parse import luna_parse
from interpreter.expressions import *
from interpreter.operators import *
from tokenizer.luna_tokenize import luna_tokenize
from .test_parse import assert_parse_expr_tokens

def test_parse_or():
  assert_parse_expr_tokens(
    "lmap([1,2], f(i){i*2})",
    Lmap(
      [1,2],
      Function(["i"], Program([Product([VarGet("i"),2])]))
    )
  )
