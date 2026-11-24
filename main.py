# main.py

import sys

from tokenizer.luna_tokenize import luna_tokenize
from parser.luna_parse import luna_parse
from interpreter.eval import luna_eval

def main():
  if len(sys.argv) != 2:
    print("Usage: luna <filename>")
    sys.exit(1)

  filename = sys.argv[1]

  with open(filename, "r", encoding="utf-8") as file:
    source = file.read()

  tokens = luna_tokenize(source)
  ast = luna_parse(tokens)
  luna_eval(ast)


if __name__ == "__main__":
  main()
