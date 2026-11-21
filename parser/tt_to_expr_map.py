from tokenizer.Token import TokenType
from interpreter.expressions import *

tt_to_expr_map = {
  TokenType.EQUALS: Equals,
  TokenType.LT: Lt,
  TokenType.LTE: Lte,
  TokenType.GT: Gt,
  TokenType.GTE: Gte,
  TokenType.PLUS: Sum,
  TokenType.MINUS: Difference,
  TokenType.TIMES: Product,
  TokenType.DIVIDE: Quotient,
  TokenType.PERCENT: Remainder,
  TokenType.CARET: Exponent
}
