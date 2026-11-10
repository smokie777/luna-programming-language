# test_tokenizer.py

import pytest
from .luna_tokenize import luna_tokenize
from .Token import *

# helper for the newline at the end of every tokenize()
def nl(line_number):
  return Token(TokenType.NEWLINE, None, line_number)

def test_tokenize_empty_file():
  assert luna_tokenize("") == [nl(0)]

def test_tokenize_number():
  assert luna_tokenize("3") == [Token(TokenType.NUMBER, 3, 1), nl(2)]
  assert luna_tokenize("33") == [Token(TokenType.NUMBER, 33, 1), nl(2)]
  assert luna_tokenize("03") == [Token(TokenType.NUMBER, 3, 1), nl(2)]
  assert luna_tokenize("33.3") == [Token(TokenType.NUMBER, 33.3, 1), nl(2)]
  with pytest.raises(Exception):
    luna_tokenize("33.3.")
  with pytest.raises(Exception):
    luna_tokenize("3.")
  with pytest.raises(Exception):
    luna_tokenize(".3")
  with pytest.raises(Exception):
    luna_tokenize("3.3.3")
  with pytest.raises(Exception):
    luna_tokenize(".")
  with pytest.raises(Exception):
    luna_tokenize("33abc")

def test_tokenize_string():
  # for now, Luna does not allow single quotes in a string.
  # also, because there is a \n in the string, the line count will be incremented.
  all_valid_chars_string = "abcdefghijklmnopqrstuvwxyz1234567890`~!@#$%^&*()_+-=[]{}|;:\",<.>/? \n"
  assert luna_tokenize(f'\'{all_valid_chars_string}\'') == [
    Token(TokenType.STRING, all_valid_chars_string, 2),
    nl(3)
  ]
  assert luna_tokenize("''") == [Token(TokenType.STRING, "", 1), nl(2)]
  assert luna_tokenize("'a'") == [Token(TokenType.STRING, "a", 1), nl(2)]
  assert luna_tokenize("'='") == [Token(TokenType.STRING, "=", 1), nl(2)]
  assert luna_tokenize("'CaPs'") == [Token(TokenType.STRING, "CaPs", 1), nl(2)]
  assert luna_tokenize("'three\nline\nstring'") == [Token(TokenType.STRING, "three\nline\nstring", 3), nl(4)]
  with pytest.raises(Exception):
    luna_tokenize("'unclosedstring")
  with pytest.raises(Exception):
    luna_tokenize("unclosedstring'")

def test_tokenize_identifier():
  assert luna_tokenize("abc") == [Token(TokenType.IDENTIFIER, "abc", 1), nl(2)]

def test_tokenize_keyword():
  assert luna_tokenize("=") == [Token(TokenType.EQUALS, None, 1), nl(2)]
  assert luna_tokenize("true") == [Token(TokenType.TRUE, None, 1), nl(2)]
  assert luna_tokenize("false") == [Token(TokenType.FALSE, None, 1), nl(2)]
  assert luna_tokenize("==+") == [
    Token(TokenType.EQUALS, None, 1),
    Token(TokenType.EQUALS, None, 1),
    Token(TokenType.PLUS, None, 1),
    nl(2)
  ]
  with pytest.raises(Exception):
    luna_tokenize("@")

def test_tokenize_keyword_vs_identifier():
  assert luna_tokenize("trueabc") == [Token(TokenType.IDENTIFIER, "trueabc", 1), nl(2)]
  assert luna_tokenize("true1") == [Token(TokenType.IDENTIFIER, "true1", 1), nl(2)]
  assert luna_tokenize("CaPs") == [Token(TokenType.IDENTIFIER, "CaPs", 1), nl(2)]
s = "-> x -2 * (3 - 4.5)"
expected = [
  Token(TokenType.VARSET, None, 1),
  Token(TokenType.IDENTIFIER, "x", 1),
  Token(TokenType.MINUS, None, 1),
  Token(TokenType.NUMBER, 2, 1),
  Token(TokenType.TIMES, None, 1),
  Token(TokenType.PAREN_OPEN, None, 1),
  Token(TokenType.NUMBER, 3, 1),
  Token(TokenType.MINUS, None, 1),
  Token(TokenType.NUMBER, 4.5, 1),
  Token(TokenType.PAREN_CLOSE, None, 1),
  nl(2)
]
def test_tokenize_composite_one_line():
  print(luna_tokenize(s))
  assert luna_tokenize(s) == expected

def test_tokenize_composite_one_line_no_spaces():
  assert luna_tokenize(s.replace(" ", "")) == expected

def test_tokenize_multiline():
  assert luna_tokenize("3\n3") == [
    Token(TokenType.NUMBER, 3, 1),
    Token(TokenType.NEWLINE, None, 1),
    Token(TokenType.NUMBER, 3, 2),
    nl(3)
  ]

def test_tokenize_composite_more_cases():###
  assert luna_tokenize("abc+def") == [
    Token(TokenType.IDENTIFIER, "abc", 1),
    Token(TokenType.PLUS, None, 1),
    Token(TokenType.IDENTIFIER, "def", 1),
    nl(2)
  ]

def test_tokenize_comment_multiline():
  assert luna_tokenize("#comment\n3\n#comment\n3#comment") == [
    Token(TokenType.NEWLINE, None, 1),
    Token(TokenType.NUMBER, 3, 2),
    Token(TokenType.NEWLINE, None, 2),
    Token(TokenType.NEWLINE, None, 3),
    Token(TokenType.NUMBER, 3, 4),
    nl(5)
  ]
