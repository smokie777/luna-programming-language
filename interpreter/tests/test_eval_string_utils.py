# test_eval_string_utils.py

from ..expressions import *
from .test_utils import assert_builtin_fn_call
import pytest

def test_eval_trim():
  assert_builtin_fn_call("trim", ["    trim_me!   "], "trim_me!")
