# reductions.py

from luna_types import LvList, Lv
from typeutils import luna_to_boolean, luna_to_list, luna_to_number, luna_to_string
from equals import luna_equals
from arithmetic import luna_plus, luna_minus
from collections.abc import Callable

# Reduces a list into a single item by calling fn on each sequential
# pair of items in the list, accumulating the result each time.
def luna_reduce(
  acc: Lv,
  l: LvList,
  fn: Callable[[Lv, Lv], Lv]
) -> Lv:
  for i in l:
    acc = fn(acc, i)
  return acc

# Returns whether all values in a list are truthy.
def luna_and(l: LvList) -> bool:
  for i in l:
    if luna_equals(luna_to_boolean(i), False):
      return False
  return True

# Returns whether at least one value in a list is truthy.
def luna_or(l: LvList) -> bool:
  for i in l:
    if luna_equals(luna_to_boolean(i), True):
      return True
  return False

# Luna reductions respect type hierarchy based coercion.
# So, the accumulator is chosen as the first item converted to the highest type in the list.
def gen_luna_reduce_acc(l: LvList) -> Lv:
  if len(l) == 0:
    return False
  is_acc_string = False
  is_acc_number = False
  for i in l:
    if isinstance(i, list):
      return luna_to_list(l[0])
    elif isinstance(i, str):
      is_acc_string = True
    elif isinstance(i, int | float):
      is_acc_number = True
  if is_acc_string:
    return luna_to_string(l[0])
  elif is_acc_number:
    return luna_to_number(l[0])
  return False

# Returns the sum of all values in a list.
def luna_sum(l: LvList) -> Lv:
  if len(l) == 0:
    return False
  elif len(l) == 1:
    return l[0]
  return luna_reduce(gen_luna_reduce_acc(l), l[1:], luna_plus)

# Returns the difference of all values in a list.
# In subtraction, the first item is the most important, so
# the accumulator is chosen to be the first item in the list.
def luna_difference(l: LvList) -> Lv:
  if len(l) == 0:
    return False
  elif len(l) == 1:
    return l[0]
  return luna_reduce(gen_luna_reduce_acc(l), l[1:], luna_minus)
