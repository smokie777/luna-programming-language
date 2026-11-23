# mappings.py

from tokenizer.Token import TokenType
from interpreter.expressions import *
from interpreter.operators import EqualityOp, AdditionOp, MultiplicationOp
from interpreter.equals import luna_equals
from interpreter.inequality import luna_lt, luna_gt, luna_lte, luna_gte
from interpreter.arithmetic import luna_plus, luna_minus, luna_divide, luna_times, luna_remainder

tt_to_equality_op = {
  TokenType.EQUALS: EqualityOp.EQ,
  TokenType.LT: EqualityOp.LT,
  TokenType.LTE: EqualityOp.LTE,
  TokenType.GT: EqualityOp.GT,
  TokenType.GTE: EqualityOp.GTE,
}

tt_to_addition_op = {
  TokenType.PLUS: AdditionOp.PLUS,
  TokenType.MINUS: AdditionOp.MINUS
}

tt_to_multiplication_op = {
  TokenType.TIMES: MultiplicationOp.TIMES,
  TokenType.DIVIDE: MultiplicationOp.DIVIDE,
  TokenType.PERCENT: MultiplicationOp.PERCENT
}

equality_op_to_eval_fn = {
  EqualityOp.EQ: luna_equals,
  EqualityOp.LT: luna_lt,
  EqualityOp.GT: luna_gt,
  EqualityOp.LTE: luna_lte,
  EqualityOp.GTE: luna_gte,
}

addition_op_to_eval_fn = {
  AdditionOp.PLUS: luna_plus,
  AdditionOp.MINUS: luna_minus,
}

multiplication_op_to_eval_fn = {
  MultiplicationOp.TIMES: luna_times,
  MultiplicationOp.DIVIDE: luna_divide,
  MultiplicationOp.PERCENT: luna_remainder
}
