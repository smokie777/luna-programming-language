# main.py

import sys

from tokenizer.luna_tokenize import luna_tokenize
from parser.luna_parse import luna_parse
from interpreter.luna_eval import luna_eval
import time

def main():
  should_show_time = "-t" in sys.argv

  args = [arg for arg in sys.argv[1:] if arg != "-t"]

  if len(args) != 1:
    print("Usage: python main.py [-t] <filename>")
    sys.exit(1)

  filename = args[0]

  with open(filename, "r", encoding="utf-8") as file:
    source = file.read()

  start_time = time.perf_counter() if should_show_time else 0
  tokens = luna_tokenize(source)
  ast = luna_parse(tokens)
  luna_eval(ast)
  
  if should_show_time:
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.6f} seconds")


if __name__ == "__main__":
  main()
