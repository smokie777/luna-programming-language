# luna_parse.py

from interpreter.expressions import *
from tokenizer.Token import TokenType, Token
from tokenizer.luna_tokenize import luna_tokenize
from .utils import luna_throw

# Luna's parser is a Recursive Descent Parser which takes a 1-D list of tokens and outputs an AST of Expressions.
# Rules of the implementation:
# 1. Each parse() should only be called when idx could point to the first token of its expression. Thus, each parse() should move idx forward appropriately.
# 2. A lower precedence operation's parse() should be higher up in the file than a higher precedence operation's parse().
# 3. The entry point to the recursion is parse_expr(). Recursive calls to parse_expr() are not allowed until the entire descent is completed.
def luna_parse(tokens: list[Token]):
  idx = 0

  # TODO: handle multiline programs
  def parse_program():
    # TODO: gather nodes of expressions separated by newline similarly to how parse_or gathers nodes separated by |
    pass

  def parse_expr():
    nonlocal idx
    node = parse_varset()
        
    return node

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

  def parse_or():
    nonlocal idx
    nodes = [parse_value()]
    while idx < len(tokens) and tokens[idx].type == TokenType.OR:
      idx += 1
      nodes.append(parse_value())
    return nodes[0] if len(nodes) == 1 else Some(nodes)

  # ALL OPERATORS TO EVENTUALLY BE IMPLEMENTED HERE

  # do not handle lists for now, just terminals
  def parse_value():
    nonlocal idx
    t = tokens[idx]
    match t.type:
      case TokenType.NUMBER | TokenType.STRING:
        idx += 1
        return t.value
      case TokenType.TRUE:
        idx += 1
        return True
      case TokenType.FALSE:
        idx += 1
        return False
      case TokenType.PAREN_OPEN:
        # recursive parse_expr() only allowed after full descent
        idx += 1
        node = parse_expr()
        if tokens[idx].type != TokenType.PAREN_CLOSE:
          luna_throw(f'Found unclosed ")": {node}')
        return node
    luna_throw(f'Unexpected token: {t}')  
  
  return parse_expr()

if __name__ == "__main__":
# print(luna_parse(luna_tokenize("-> x 3")))
  print(luna_parse(luna_tokenize("-> x 3 3")))