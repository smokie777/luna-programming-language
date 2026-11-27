# equals.py

from .luna_types import Lv, LvMap

# Returns whether two values are equal.
# Different types are never equal.
# Collection data structure equality is implemented as deep equality.
def luna_equals(a:Lv, b:Lv) -> bool:
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
          return all([luna_equals(a[i], b[i]) for i in range(len(a))])
        case _:
          return False
    case LvMap():
      match b:
        case LvMap():
          if len(a.aa) != len(b.aa):
            return False
          matched_indices = []
          for k1, v1 in a.aa:
            for idx in range(len(b.aa)):
              k2, v2 = b.aa[idx]
              if (
                idx not in matched_indices
                and luna_equals(k1, k2) and luna_equals(v1, v2)
              ):
                matched_indices.append(idx)
          return len(matched_indices) == len(a.aa)
        case _:
          return False
    case _:
      return False
