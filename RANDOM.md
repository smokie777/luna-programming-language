# RANDOM

This file is for writing down various informal thoughts










# LOGICAL SWITCHES

Syntax:
[condition](branches)

A condition must be a value.

A branch must be a branch object: value => expr
Branch expr will not be evaluated until that logical branch is reached in code execution.

This will evaluate to 3 because 'a'+'b' matches 'ab'.
['a'+'b'](
  'a' => 1,
  'b' => 2,
  'ab' => 3
)

Shorthand: if branches has exactly two non-branch value arguments, it is treated as if matching true and false.
Only when using this shorthand is the condition coerced to a boolean.
[7=4](1, 2)
Is the same as:
[7=4](
  true => 1,
  false => 2
)
Note that when explicitly matching true and false, the condition will not be coerced to a boolean.

If there is only one branch, it is treated as if matching true.
[7=4](1)
Is the same as:
[7=4](true => 1)

If there is no match, nothing will happen. The switch will evaluate to null.
['a'+'b'](
  'a' => 1
)

Default branches are optional, and are indicated with _.
['a'+'b'](
  'a' => 1
  _ => 2
)

If there are multiple matches, the topmost wins.
['a'+'b'](
  'a' => 'this branch is used',
  'b' => 2,
  'a' => 'unreachable code'
)

A branch may also be stored in a variable.
-> my_branch (
  'ab' => 3
)
['a'+'b'](
  'a' => 1,
  'b' => 2,
  my_branch
)

Multiple branches can be stored in a list.
-> my_branches (
  'a' => 1,
  'b' => 2,
  'ab' => 3
)
['a'+'b'](my_branches)

An entire logical switch can be stored in a variable. At runtime, variables will be looked up in whatever scope is active.
-> my_switch (
  ['a'+'b'](
    'a' => 1,
    'b' => 2,
    'ab' => 3
  )
)
