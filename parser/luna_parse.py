# luna_parse.py

from interpreter.expressions import *
from tokenizer.Token import TokenType, Token
from .utils import luna_throw
from common.mappings import tt_to_equality_op, tt_to_addition_op, tt_to_multiplication_op
from common.constants import ReservedKeywords, RESERVED_KEYWORDS_SET

# A recursive descent parser which takes a 1-D list of tokens and returns an AST of Expressions.
# invariants:
# 1. a parse_ method should only be called if the token at idx could be the expected token. 
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
    while check(TokenType.NEWLINE):
      consume()

  # consume the current token, and all newlines after it
  def consume_current_and_newlines():
    consume()
    consume_newlines()

  def parse_file():
    nonlocal idx
    nodes = [parse_expr()]
    while check(TokenType.NEWLINE):
      consume_newlines()
      if idx < len(tokens): # check for EOF
        nodes.append(parse_expr())
      else:
        break
    return Program(nodes)

  def parse_expr():
    nonlocal idx
    # parse all operators, starting from the lowest prio
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
    while check(TokenType.OR):
      consume_current_and_newlines()
      nodes.append(parse_and())
    return nodes[0] if len(nodes) == 1 else Some(nodes)
  
  def parse_and():
    nonlocal idx
    nodes = [parse_equality()]
    while check(TokenType.AND):
      consume_current_and_newlines()
      nodes.append(parse_equality())
    return nodes[0] if len(nodes) == 1 else All(nodes)

  def parse_equality():
    nonlocal idx
    items = [parse_addition()]
    operators = []
    while check(list(tt_to_equality_op.keys())):
      operators.append(tt_to_equality_op[current().type])
      consume_current_and_newlines()
      items.append(parse_addition())
    return items[0] if len(items) == 1 else EqualityChain(items, operators)

  def parse_addition():
    nonlocal idx
    items = [parse_multiplication()]
    operators = []
    while check(list(tt_to_addition_op.keys())):
      operators.append(tt_to_addition_op[current().type])
      consume_current_and_newlines()
      items.append(parse_multiplication())
    return items[0] if len(items) == 1 else AdditionChain(items, operators)

  def parse_multiplication():
    nonlocal idx
    items = [parse_exponent()]
    operators = []
    while check(list(tt_to_multiplication_op.keys())):
      operators.append(tt_to_multiplication_op[current().type])
      consume_current_and_newlines()
      items.append(parse_exponent())
    return items[0] if len(items) == 1 else MultiplicationChain(items, operators)

  def parse_exponent():
    nonlocal idx
    nodes = [parse_inverse()]
    while check(TokenType.CARET):
      consume_current_and_newlines()
      nodes.append(parse_inverse())
    return nodes[0] if len(nodes) == 1 else Exponent(nodes)

  def parse_inverse():
    nonlocal idx
    if check(TokenType.MINUS):
      consume_current_and_newlines()
      return Inverse(parse_value())
    return parse_value()

  def parse_value():
    nonlocal idx
    t = current()
    match t.type:
      case TokenType.NUMBER | TokenType.STRING:
        consume()
        return t.value
      case TokenType.NAME:
        return parse_name()
      case TokenType.VARSET:
        return parse_varset()
      case TokenType.VARSET_GLOBAL:
        return parse_varset(True)
      case TokenType.FREEZE:
        consume()
        return Frozen(parse_expr())
      case TokenType.BRACE_OPEN:
        return parse_program()
      case TokenType.PAREN_OPEN:
        consume_current_and_newlines()
        node = parse_expr()
        consume_newlines()
        if check(TokenType.PAREN_CLOSE):
          consume()
          return node
        else:
          luna_throw(f'Found unclosed ")": {node}')
    luna_throw(f'Unexpected value token: {t}')  

  def parse_name():
    nonlocal idx
    t = current()
    match t.value:
      case ReservedKeywords.TRUE:
        consume()
        return True
      case ReservedKeywords.FALSE:
        consume()
        return False
      case ReservedKeywords.CONTINUE:
        consume()
        return Continue()
      case ReservedKeywords.BREAK:
        consume()
        return Break()
      case ReservedKeywords.RETURN:
        consume()
        if current().type != TokenType.PAREN_OPEN:
          return Return(False)
        return Return(parse_arguments(t.value)[0])
      case ReservedKeywords.BOOLEAN:
        consume()
        return ToBoolean(parse_arguments(t.value)[0])
      case ReservedKeywords.STRING:
        consume()
        return ToString(parse_arguments(t.value)[0])
      case ReservedKeywords.NUMBER:
        consume()
        return ToNumber(parse_arguments(t.value)[0])
      case ReservedKeywords.PRINT:
        consume()
        return Print(parse_arguments(t.value)[0])
      case ReservedKeywords.FUNCTION:
        consume()
        return Function(parse_params(t.value), parse_program())
      case ReservedKeywords.LOOP:
        consume()
        args = parse_arguments(t.value)
        if len(args) < 1 or len(args) > 3:
          luna_throw(f'Loop must be called as loop(iterable:number|boolean|list|string, iterator:identifier, index:identifier)Program. iterator and index are optional.') 
        body = parse_program()
        return Loop(
          args[0],
          # the loop iterator is an argument, but the loop item and idx are params.
          # args[x].varname is a hack to extract a string from VarGet without needing to write another parse_.
          # a custom parse_ should probably eventually be written to prevent the user
          # from passing in expressions that evaluate to strings.
          args[1].varname if len(args) >= 2 else None,
          args[2].varname if len(args) == 3 else None,
          body
        )

      case _:
        # there is no consume() here because VarGet has no token or syntax
        return VarGet(parse_identifier())

  def parse_identifier():
    if not check(TokenType.NAME):
      luna_throw(f'Expected identifer. Got: {current()}')
    if current().value in RESERVED_KEYWORDS_SET:
      luna_throw(f'Identifier name cannot be a reserved keyword: {current().value}')
    ret = current().value
    consume()
    return ret

  def parse_params(construct_name: str):
    nonlocal idx
    if check(TokenType.PAREN_OPEN):
      consume_current_and_newlines()
      if check(TokenType.PAREN_CLOSE):
        consume()
        return []
    else:
      luna_throw(f'Params for "{construct_name}" must be enclosed in ().')
    params = [parse_identifier()]
    consume_newlines()
    while check(TokenType.COMMA):
      consume_current_and_newlines()
      params.append(parse_identifier())
    if check(TokenType.PAREN_CLOSE):
      consume()
      return params
    luna_throw(f'Params for "{construct_name}" must be enclosed in ().')

  def parse_arguments(construct_name: str):
    nonlocal idx
    if check(TokenType.PAREN_OPEN):
      consume_current_and_newlines()
      if check(TokenType.PAREN_CLOSE):
        consume()
        return []
    else:
      luna_throw(f'Arguments for "{construct_name}" must be enclosed in ().')
    args = [parse_expr()]
    consume_newlines()
    while check(TokenType.COMMA):
      consume_current_and_newlines()
      args.append(parse_expr())
    if check(TokenType.PAREN_CLOSE):
      consume()
      return args
    luna_throw(f'Arguments for "{construct_name}" must be enclosed in ().')

  def parse_varset(is_varset_global = False):
    nonlocal idx
    consume()
    varname = parse_identifier()
    varvalue = parse_expr()
    if is_varset_global:
      return VarSetGlobal(varname, varvalue)
    else: 
      return VarSet(varname, varvalue)
      
  def parse_program():
    nonlocal idx
    if check(TokenType.BRACE_OPEN):
      consume_current_and_newlines()
      if check(TokenType.BRACE_CLOSE):
        consume()
        return Program([])
    else:
      luna_throw(f'Program must start with {"{"}. Got: {current()}')
    nodes = [parse_expr()]
    while check(TokenType.NEWLINE):
      consume_newlines()
      nodes.append(parse_expr())
    if check(TokenType.BRACE_CLOSE):
      consume()
      return Program(nodes)
    luna_throw(f'Program must end with {"}"}. Got: {current()}')


  return parse_file()
