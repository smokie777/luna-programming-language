# test_tokenizer.py

import pytest
from tokenizer.luna_tokenize import luna_tokenize
from tokenizer.Token import *

def test_tokenize_number():
  s = "3"
  assert luna_tokenize(s) == [Token(TokenType.NUMBER, 3, 1)]
