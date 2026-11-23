# luna_parse.py

from interpreter.expressions import *
from tokenizer.Token import TokenType, Token
from .utils import luna_throw
from common.mappings import tt_to_equality_op, tt_to_addition_op, tt_to_multiplication_op

# A recursive descent parser which takes a 1-D list of tokens and returns an AST of Expressions.
def luna_parse(tokens: list[Token]) -> Expression:
  idx = 0

  # check if the current token is a given token(s)
  def check(token_type: str | list) -> bool:
    if idx >= len(tokens):
      return False
    if isinstance(token_type, str):
      return tokens[idx].type == token_type
    if isinstance(token_type, list):
      return tokens[idx].type in token_type
    luna_throw(f'Check input must be str or list. Got: {token_type}')

  # get the current token
  def current():
    return tokens[idx]

  # consume the current token
  def consume():
    nonlocal idx
    idx += 1

  # consume all newlines starting at the current token
  def consume_newlines():
    nonlocal idx
    while idx < len(tokens) and check(TokenType.NEWLINE):
      consume()

  # consume the current token, and all newlines after it
  def consume_current_and_newlines():
    consume()
    consume_newlines()

  def parse_program():
    nonlocal idx
    nodes = [parse_expr()]
    while idx < len(tokens) and check(TokenType.NEWLINE):
      consume_newlines()
      if idx < len(tokens):
        nodes.append(parse_expr())
    return Program(nodes)

  def parse_expr():
    nonlocal idx

    # 1. parse the "start of expression keywords"
    # node = parse_varset()

    # 2. parse all operators, starting from the lowest prio
    return parse_ifthenelse()

  def parse_ifthenelse():
    nonlocal idx
    left = parse_or()
    mid = None
    right = None
    if check(TokenType.IF):
      consume_current_and_newlines()
      mid = parse_or()
    if check(TokenType.ELSE):
      consume_current_and_newlines()
      right = parse_or()
    if mid is not None or right is not None:
      return IfThenElse(left, mid, right)
    return left

  def parse_or():
    nonlocal idx
    nodes = [parse_and()]
    while idx < len(tokens) and check(TokenType.OR):
      consume_current_and_newlines()
      nodes.append(parse_and())
    return nodes[0] if len(nodes) == 1 else Some(nodes)
  
  def parse_and():
    nonlocal idx
    nodes = [parse_equality()]
    while idx < len(tokens) and check(TokenType.AND):
      consume_current_and_newlines()
      nodes.append(parse_equality())
    return nodes[0] if len(nodes) == 1 else All(nodes)

  def parse_equality():
    nonlocal idx
    items = [parse_addition()]
    operators = []
    while idx < len(tokens) and check(list(tt_to_equality_op.keys())):
      operators.append(tt_to_equality_op[current().type])
      consume_current_and_newlines()
      items.append(parse_addition())
    return items[0] if len(items) == 1 else EqualityChain(items, operators)

  def parse_addition():
    nonlocal idx
    items = [parse_multiplication()]
    operators = []
    while idx < len(tokens) and check(list(tt_to_addition_op.keys())):
      operators.append(tt_to_addition_op[current().type])
      consume_current_and_newlines()
      items.append(parse_multiplication())
    return items[0] if len(items) == 1 else AdditionChain(items, operators)

  def parse_multiplication():
    nonlocal idx
    items = [parse_exponent()]
    operators = []
    while idx < len(tokens) and check(list(tt_to_multiplication_op.keys())):
      operators.append(tt_to_multiplication_op[current().type])
      consume_current_and_newlines()
      items.append(parse_exponent())
    return items[0] if len(items) == 1 else MultiplicationChain(items, operators)

  def parse_exponent():
    nonlocal idx
    nodes = [parse_inverse()]
    while idx < len(tokens) and check(TokenType.CARET):
      consume_current_and_newlines()
      nodes.append(parse_inverse())
    return nodes[0] if len(nodes) == 1 else Exponent(nodes)

  def parse_inverse():
    nonlocal idx
    if check(TokenType.MINUS):
      consume_current_and_newlines()
      return Inverse(parse_value())
    return parse_value()

  def parse_varset():
    nonlocal idx
    if tokens[idx].type in (TokenType.VARSET, TokenType.VARSET_GLOBAL):
      is_global_varset = tokens[idx].type == TokenType.VARSET_GLOBAL
      idx += 1
      varname_token = tokens[idx]
      if not varname_token.type == TokenType.IDENTIFIER:
        luna_throw(f'Variable name must be Identifier. Got: {varname_token.type}')
      idx += 1
      varvalue = parse_or()
      if is_global_varset:
        return VarSetGlobal(varname_token.value, varvalue)
      else: 
        return VarSet(varname_token.value, varvalue)
    return parse_or()


  # ALL OPERATORS TO EVENTUALLY BE IMPLEMENTED HERE

  # TODO: implement handling for identifiers, lists, maps
  def parse_value():
    nonlocal idx
    t = tokens[idx]
    match t.type:
      case TokenType.NUMBER | TokenType.STRING:
        consume()
        return t.value
      case TokenType.TRUE:
        consume()
        return True
      case TokenType.FALSE:
        consume()
        return False
      case TokenType.PAREN_OPEN:
        consume_current_and_newlines()
        node = parse_expr()
        consume_newlines()
        if tokens[idx].type == TokenType.PAREN_CLOSE:
          consume()
          return node
        else:
          luna_throw(f'Found unclosed ")": {node}')
    luna_throw(f'Unexpected value token: {t}')  

  
  return parse_program()
