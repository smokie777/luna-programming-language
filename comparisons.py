# comparisons.py

# Concerning cross-type equality: different types are never equal.
# List equality is defined as: both lists have the same length,
# and the value at each index of both lists are equal.

def equals(a, b):
  match a:
    case str():
      match b:
        case str():
          return a == b
        case _:
          return False
    case bool():
      match b:
        case bool():
          return a == b
        case _:
          return False
    case int() | float():
      match b:
        case bool():
          return False
        case int() | float():
          return float(a) == float(b)
        case _:
          return False
    case list():
      match b:
        case list():
          if len(a) != len(b):
            return False
          return all([equals(a[i], b[i]) for i in range(len(a))])
        case _:
          return False
    case _:
      return False
    