# luna_parse.py

from interpreter.expressions import *
from tokenizer.Token import TokenType, Token
from .utils import luna_throw
from common.mappings import tt_to_equality_op, tt_to_addition_op, tt_to_multiplication_op
from common.constants import ReservedKeywords, RESERVED_KEYWORDS_SET, BUILTIN_KEYWORDS_SET

# A recursive descent parser which takes a 1-D list of tokens and returns an AST of Expressions.
# invariants:
# 1. a parse_ method should only be called if the token at idx could be the expected token. 
def luna_parse(tokens:list[Token], should_suppress_warnings:bool=False) -> Expression:
  idx = 0

  # check if the current token is a given token(s)
  def check(token_type:str|list) -> bool:
    if idx >= len(tokens): # detect EOF
      return False
    if isinstance(token_type, str):
      return tokens[idx].type == token_type
    if isinstance(token_type, list):
      return tokens[idx].type in token_type
    luna_throw(f'Check input must be str or list. Got: {token_type}')

  # get the current token
  def current():
    if idx >= len(tokens):
      luna_throw(f'Unexpected end of file')
    return tokens[idx]

  # consume the current token
  def consume():
    nonlocal idx
    if idx >= len(tokens):
      luna_throw(f'Unexpected end of file')
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

  # parse_file is the entry point into the parsing of a file.
  def parse_file():
    nonlocal idx
    nodes = []
    while True:
      consume_newlines()
      if idx >= len(tokens): # check for EOF
        break
      nodes.append(parse_expr())
      if check(TokenType.NEWLINE):
        continue
      luna_throw(f'Unexpected token at end of expression in File: {current()}')
    return Program(nodes)

  # parse_expr initiates descent into the operator precedence chain.
  def parse_expr():
    return parse_ternary()

  def parse_ternary():
    nonlocal idx
    left = parse_or()
    mid = None
    right = None
    if check(TokenType.TERNARY_IF):
      consume_current_and_newlines()
      mid = parse_or()
      consume_newlines()
      if check(TokenType.TERNARY_ELSE):
        consume_current_and_newlines()
        right = parse_or()
    if mid is not None and right is not None:
      return IfThenElse(left, mid, right)
    if mid is None and right is None:
      return left
    luna_throw(f'Incomplete ternary - both a truthy case >> and a falsey case !> must be provided')

  def _parse_single_op_chain(next_parse_fn, op_token_type, ast_node_constructor):
    nonlocal idx
    nodes = [next_parse_fn()]
    while check(op_token_type):
      consume_current_and_newlines()
      nodes.append(next_parse_fn())
    return nodes[0] if len(nodes) == 1 else ast_node_constructor(nodes)

  def _parse_multi_op_chain(next_parse_fn, op_token_type_map, ast_node_constructor):
    nonlocal idx
    items = [next_parse_fn()]
    operators = []
    while check(list(op_token_type_map.keys())):
      operators.append(op_token_type_map[current().type])
      consume_current_and_newlines()
      items.append(next_parse_fn())
    return items[0] if len(items) == 1 else ast_node_constructor(items, operators)

  def parse_or():
    return _parse_single_op_chain(parse_and, TokenType.OR, Some)
  
  def parse_and():
    return _parse_single_op_chain(parse_equality, TokenType.AND, All)
  
  def parse_equality():
    return _parse_multi_op_chain(parse_addition, tt_to_equality_op, EqualityChain)

  def parse_addition():
    return _parse_multi_op_chain(parse_multiplication, tt_to_addition_op, AdditionChain)

  def parse_multiplication():
    return _parse_multi_op_chain(parse_exponent, tt_to_multiplication_op, MultiplicationChain)

  def parse_exponent():
    return _parse_single_op_chain(parse_inverse, TokenType.CARET, Exponent)

  def parse_inverse():
    nonlocal idx
    if check(TokenType.MINUS):
      consume()
      return Inverse(parse_inverse())
    return parse_invocation()

  def parse_invocation():
    nonlocal idx
    term = parse_value()
    while check(TokenType.PAREN_OPEN):
      term = Invoke(term, parse_arguments("invoke"))
    return term
  
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
        # this paren block is for "grouping", as opposed to parens for params/args.
        consume_current_and_newlines()
        node = parse_expr()
        consume_newlines()
        if check(TokenType.PAREN_CLOSE):
          consume()
          return node
        else:
          luna_throw(f'Found unclosed ")": {node}')
      case TokenType.BRACKET_OPEN:
        return parse_list()
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
        return Return(parse_arguments(t.value, [1])[0])
      case ReservedKeywords.MAP:
        consume()
        return Map(parse_map_body())
      case ReservedKeywords.IF:
        consume()
        condition = parse_arguments(t.value, [1])[0]
        if_branch = parse_program()
        else_branch = None
        if check(TokenType.NAME) and current().value == ReservedKeywords.ELSE:
          consume_current_and_newlines()
          else_branch = parse_program()
        return IfThenElse(condition, if_branch, else_branch)
      case ReservedKeywords.FUNCTION | ReservedKeywords.F:
        consume()
        return Function(parse_params(t.value), parse_program())
      case ReservedKeywords.LOOP:
        consume()
        args = parse_arguments(t.value, [1, 2, 3])
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
      case ReservedKeywords.SWITCH:
        consume()
        condition = parse_arguments(t.value, [1])[0]
        cases, branches = parse_switch_body()
        return Switch(condition, cases, branches)
      case _:
        # there is no consume() here because VarGet has no token or syntax
        return VarGet(parse_identifier())

  def parse_identifier():
    if not check(TokenType.NAME):
      luna_throw(f'Expected identifer. Got: {current()}')
    ret = current().value
    consume()
    return ret

  def parse_params(construct_name:str):
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
      consume_newlines()
    if check(TokenType.PAREN_CLOSE):
      consume()
      return params
    luna_throw(f'Params for "{construct_name}" must be enclosed in ().')

  def parse_arguments(construct_name:str, exact_num_args:list|None = None):
    nonlocal idx
    if check(TokenType.PAREN_OPEN):
      consume_current_and_newlines()
      if check(TokenType.PAREN_CLOSE):
        consume()
        if not exact_num_args:
          return []
        luna_throw(f'"{construct_name}" must have {exact_num_args} args, got: 0')
    else:
      luna_throw(f'Arguments for "{construct_name}" must be enclosed in ().')
    args = [parse_expr()]
    consume_newlines()
    while check(TokenType.COMMA):
      consume_current_and_newlines()
      args.append(parse_expr())
      consume_newlines()
    if check(TokenType.PAREN_CLOSE):
      consume()
      if exact_num_args is None or len(args) in exact_num_args:
        return args
      luna_throw(f'"{construct_name}" must have {exact_num_args} args, got: {len(args)}')
    luna_throw(f'Arguments for "{construct_name}" must be enclosed in ().')

  def parse_map_body():
    nonlocal idx
    if check(TokenType.BACKTICK):
      consume_current_and_newlines()
      if check(TokenType.BACKTICK):
        consume()
        return []
    else:
      luna_throw(f'map body must start with backtick. Got: {current()}')
    aa = []
    while True:
      key = parse_expr()
      consume_newlines()
      if check(TokenType.COLON):
        consume_current_and_newlines()
        aa.append([key, parse_expr()])
        consume_newlines()
        if check(TokenType.COMMA):
          consume_current_and_newlines()
          continue
        if check(TokenType.BACKTICK):
          consume()
          return aa
        luna_throw(f'Expected comma or backtick after map value. Got: {current()}')
      luna_throw(f'Expected colon after map key. Got: {current()}')

  def parse_switch_body():
    nonlocal idx
    if check(TokenType.BACKTICK):
      consume_current_and_newlines()
      if check(TokenType.BACKTICK):
        consume()
        return [], []
    else:
      luna_throw(f'Switch body must start with backtick. Got: {current()}')
    cases = []
    branches = []
    while True:
      case = parse_expr()
      if isinstance(case, VarGet) and case.varname == "_":
        # this is a good workaround to prevent "_" from being tokenized as a standalone token,
        # rather than as a valid start-of-name token
        case = SwitchCatchAllCase()
      cases.append(case)
      consume_newlines()
      if check(TokenType.COLON):
        consume_current_and_newlines()
        branches.append(parse_expr())
        consume_newlines()
        if check(TokenType.COMMA):
          consume_current_and_newlines()
          continue
        if check(TokenType.BACKTICK):
          consume()
          return cases, branches
        luna_throw(f'Expected comma or backtick after switch branch. Got: {current()}')
      luna_throw(f'Expected colon after switch case. Got: {current()}')

  def parse_varset(is_varset_global = False):
    nonlocal idx
    consume()
    varname = parse_identifier()
    varvalue = parse_expr()
    if varname in RESERVED_KEYWORDS_SET:
      luna_throw(f'Variable name cannot be a reserved keyword: {varname}')
    if varname in BUILTIN_KEYWORDS_SET and not should_suppress_warnings:
      print(f'[WARNING]: {varname} was used as a variable name, shadowing a built-in function.')
    if is_varset_global:
      return VarSetGlobal(varname, varvalue)
    else: 
      return VarSet(varname, varvalue)
      
  def parse_program():
    nonlocal idx
    if check(TokenType.BRACE_OPEN):
      consume_current_and_newlines()
    else:
      luna_throw(f'Program must start with {"{"}. Got: {current()}')
    nodes = []
    while not check(TokenType.BRACE_CLOSE):
      if check(TokenType.NEWLINE):
        consume_current_and_newlines()
        continue
      nodes.append(parse_expr())
      if not check(TokenType.BRACE_CLOSE) and not check(TokenType.NEWLINE):
        luna_throw(f'Invalid token found at end of Expr in Program: {current()}')

    consume()
    return Program(nodes)

  def parse_list():
    nonlocal idx
    if check(TokenType.BRACKET_OPEN):
      consume_current_and_newlines()
      if check(TokenType.BRACKET_CLOSE):
        consume()
        return []
    else:
      luna_throw(f'List must start with [. Got: {current()}')
    nodes = [parse_expr()]
    consume_newlines()
    while check(TokenType.COMMA):
      consume_current_and_newlines()
      nodes.append(parse_expr())
      consume_newlines()
    if check(TokenType.BRACKET_CLOSE):
      consume()
      return nodes
    luna_throw(f'List must end with ]. Got: {current()}')

  return parse_file()
