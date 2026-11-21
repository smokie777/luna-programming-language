# luna_parse.py

from interpreter.expressions import *
from tokenizer.Token import TokenType, Token
from tokenizer.luna_tokenize import luna_tokenize
from .utils import luna_throw
from .tt_to_expr_map import tt_to_expr_map

# A recursive descent parser which takes a 1-D list of tokens and returns an AST of Expressions.
def luna_parse(tokens: list[Token]) -> Expression:
  idx = 0

  def check(token_type: str | list) -> bool:
    if isinstance(token_type, str):
      return tokens[idx].type == token_type
    if isinstance(token_type, list):
      return tokens[idx].type in token_type
    luna_throw(f'Check input must be str or list. Got: {token_type}')

  def consume():
    nonlocal idx
    idx += 1

  def current():
    return tokens[idx]

  # TODO: handle multiline programs
  def parse_program():
    # TODO: gather nodes of expressions separated by newline similarly to how parse_or gathers nodes separated by |
    pass

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
      consume()
      mid = parse_or()
    if check(TokenType.ELSE):
      consume()
      right = parse_or()
    if mid is not None or right is not None:
      return IfThenElse(left, mid, right)
    return left

  def parse_or():
    nonlocal idx
    nodes = [parse_and()]
    while idx < len(tokens) and check(TokenType.OR):
      consume()
      nodes.append(parse_and())
    return nodes[0] if len(nodes) == 1 else Some(nodes)
  
  def parse_and():
    nonlocal idx
    nodes = [parse_equality()]
    while idx < len(tokens) and check(TokenType.AND):
      consume()
      nodes.append(parse_equality())
    return nodes[0] if len(nodes) == 1 else All(nodes)

  def parse_equality():
    nonlocal idx
    nodes = [parse_addition()]
    expr = tt_to_expr_map[current().type] if current().type in tt_to_expr_map else None
    while idx < len(tokens) and check([
      TokenType.LTE, TokenType.LT, TokenType.GTE, TokenType.GT, TokenType.EQUALS
    ]):
      consume()
      nodes.append(parse_addition())
    return nodes[0] if len(nodes) == 1 else expr(nodes)

  def parse_addition():
    nonlocal idx
    nodes = [parse_multiplication()]
    expr = tt_to_expr_map[current().type] if current().type in tt_to_expr_map else None
    while idx < len(tokens) and check([TokenType.PLUS, TokenType.MINUS]):
      consume()
      nodes.append(parse_multiplication())
    return nodes[0] if len(nodes) == 1 else expr(nodes)

  def parse_multiplication():
    nonlocal idx
    nodes = [parse_exponent()]
    expr = tt_to_expr_map[current().type] if current().type in tt_to_expr_map else None
    while idx < len(tokens) and check([TokenType.TIMES, TokenType.DIVIDE, TokenType.PERCENT]):
      consume()
      nodes.append(parse_exponent())
    return nodes[0] if len(nodes) == 1 else expr(nodes)

  def parse_exponent():
    nonlocal idx
    nodes = [parse_inverse()]
    while idx < len(tokens) and check(TokenType.CARET):
      consume()
      nodes.append(parse_inverse())
    return nodes[0] if len(nodes) == 1 else Exponent(nodes)

  def parse_inverse():
    nonlocal idx
    if check(TokenType.INVERSE):
      consume()
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

  # TODO: implement handling for lists, maps
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
        consume()
        node = parse_expr()
        if tokens[idx].type == TokenType.PAREN_CLOSE:
          consume()
          return node
        else:
          luna_throw(f'Found unclosed ")": {node}')
    luna_throw(f'Unexpected value token: {t}')  

  
  return parse_expr()
