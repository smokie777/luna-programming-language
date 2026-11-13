# INTRODUCTION

Luna is an experiment into building a small programming language!

It is a tokenizer + parser + interpreter system implemented in Python.

# OPERATOR PRECEDENCE, KEYWORDS, AND SYNTAX

This table describes Operator Precedence in Luna. All operators have left-to-right associativity.

```
HIGHEST PRECEDENCE
()                 grouping
()                 invocation (distinguished from grouping during parsing)
!                  inverse
^                  exponent
*, /, %            multiplication, division
+, -               addition, substraction
>, <, >=, <=, =    equality comparison
&                  and
|                  or
>>>                switch
LOWEST PRECEDENCE
```

Here are all pre-made keywords in Luna.

```
true               boolean true
false              boolean false
->, =>             variable assignment
<>                 freeze
loop               defines a loop
>>                 loop continue
<<                 loop break
function           defines a function
<<<                function return
switch             defines a switch
print              prints something to the console
boolean            converts an expression's type to boolean
string             converts an expression's type to string
number             converts an expression's type to number
```

Finally, here are the syntactical constructs in Luna:

```
{}                 defines a Program
(...)              defines function/loop arguments and body. arguments are separated by commas
backticks          defines switch branches
\n                 a newline defines the end of an expression (unless in a string)
```

# HIERARCHICAL TYPES

Luna supports these Value types:

1. List
2. String
3. Number
4. Boolean

Types in Luna are hierarchical, with List at the top and Boolean at the bottom. In operations between incompatible types, lower types will generally be coerced into higher types.

Luna does support converting higher types down to lower types, but this should be used sparingly, as it goes against the idea of hierarchical types.

Luna does not feature a `null` type; instead it uses `false`, as that is the falsey value of the lowest type in the hierarchy. There is one falsey value for each type: `[]`, `""`, `0`, `false`.

# CROSS TYPE OPERATIONS

Cross-type operations across Values are generally allowed, and will respect the type hierarchy. Each operation decides which cross-type interactions are allowed, and when type coercion is appropriate.

Operations evaluate from left-to-right, are left-associative, and short-circuit when possible.

Luna operations are designed with reversability in mind. For example, Plus can be reversed with Minus, and Times can be reversed with Divide.

While interesting cross-type operations is not the main focus of the language, some unconventional ones are allowed:

- Addition/Subtraction of strings and lists via concatenation and inverse concatenation (removing a matching sequence from the end)
- Multiplication/Division of strings and lists via sequence repetition

The highest type in the sequence is String, so each item is coerced into a string, then concatenation is performed.  
`true + 1 + 1 + 1 + "ue" = "true111ue"`  
`true - 1 - 1 - 1 - "ue" = "tr"`

List/String multiplication and division is sequence repetition and reversal of sequence repetition
`"ab" * 2 = "abab"`  
`"abab" / 2 = "ab"`  
`"abab" / "ab = 2`  
`"abab" / 2 = "ab"`

Multiplying and dividing strings and lists by negative numbers creates their "inverse": a reversed sequence!  
`"abab" * -2 = "baba"`  
`"baba" / -2 = "ab"`  
`"baba" / "ab" = -2`

# COMPOSABLE PROGRAMS

The fundamental representation of a sequence of Expressions in Luna is a Program, represented by a sequence of expressions inside curly braces `{}` separated by newlines `\n`. A Program will evaluate to the last expression in the sequence. A `.luna` file in its entirety counts as a Program, even if `{}` is not written. Examples of Programs:

```
print(1)
print(2)
print(3) # a .luna file is a Program.
```

```
-> x { # Programs can be evaluated and assigned to variables.
  1
  2
  3
}
print(x) # prints 3
```

```
function(){ # a Function body is a Program. Function bodies will not be evaluated until invoked.
  1
  2
  3
}
```

One eventual goal of Luna is to implement composable Programs - for example, combining two Programs by concatenating their lists of expressions.

# FROZEN EXPRESSIONS

In Luna, you can write `<>` before an expression to Freeze it. A Frozen expression will not be evaluated until invoked using `()`. Frozen expressions can be freely assigned to other variables.

Every Expression in Luna can be frozen! This should (hopefully) allow for some creative program designs.

At the AST level, Freezing an expression means wrapping it in a Frozen class, which will then be handled by the Interpreter. Function definitions will automatically be Frozen without requiring the `<>` syntax.

```
-> a print(1)
-> b <>Print(2)
-> c print(3)
# prints 1, 3
```

# INVOCATIONS

In Luna, invocations, indicated with `()`, serve two purposes:

1. Invoke Functions and other invokables, causing them to evaluate, with or without arguments.
2. Evaluate any Frozen expression

```
-> a print(1)
-> b <>Print(2)
-> c print(3)
b()
# prints 1, 3, 2
```

# FUNCTIONS, SCOPES, AND VARIABLES

Luna supports dynamically scoped Functions using the `function` keyword.

Each Function invocation creates a new Scope, which holds local variable definitions and other scope-related information. Variable scoping rules include:

- Variable lookup will search in the current scope first, then in parent scopes.
- Variable setting using `->` will only set the variable inside the current scope.
- Variable setting using `=>` will search the current scope and all parent scopes for the variable, and set the variable in all scopes in which it was defined! If no definitions were found, it will behave the same as `->`.
- A variable name must start with a letter, and only contain letters, numbers, and underscores.

```
-> my_func function(a, b){
  a + b
}
print(my_func(1, 2)) # prints 3
```

The `<<<` keyword can be used to return from a Function call, with or without a return expression after it. If `<<<` is not provided, the evaluation of the last expression in the Function body will be returned.

# SWITCHES

Luna handles logical branching using Switches using the `switch` keyword. Switch branches are enclosed in backticks, newline `\n` separated, and are written as `expr1 >>> expr2`. If the Switch condition matches `expr1` in any branch, the Switch will evaluate to `expr2`.

- The Switch condition can be composed.
- Switch cases will be eagerly evaluated when a Switch is evaluated. (need to refactor to only evaluate when checked)
- Switch branches will NOT be evaluated until the matching branch was found during runtime.

Switch evaluated immediately:

```
switch(2+2)`
  3 >>> print("three")
  4 >>> print("four")
  _ >>> print("fallback")
`
# prints "four"
```

Frozen Switch with composed condition evaluated at invocation:

```
-> my_frozen_switch <>switch(my_condition)`
  3 >> "three"
  4 >> "four
`
-> my_condition 3
-> result my_frozen_switch()
print(result) # prints "three"
```

Note: The switch was composed using a variable reference that did not exist at the time! This is allowed, as that variable got defined before the switch was invoked.

A Switch branch can also be written outside of a Switch construct, where it takes on a different meaning: `expr1 >>> expr2` will evaluate to `expr2` if `expr1` is truthy, and `false` if `expr1` is falsey.

# LOOPS

Luna provides a `loop` keyword: `loop(iterable:number|boolean|list|string, iterator, index)(Program)`

A loop will not create a new scope; its contents will be evaluated in the current scope.

`iterator` and `index` are optional. If provided, new variables will be created in the current scope corresponding to the given identifier names. If this would overwrite a pre-existing variable's value in the current scope, those values would be reverted after the loop finishes (or is broken out of).

If iterable is a Number, repeats the loop number times

```
loop(3)(print(0))
# prints 0 0 0
```

If iterable is a boolean True, that is an infinite loop! If iterable is boolean False, nothing will happen.

```
loop(True, item, idx)(print(idx))
# prints 0 1 2...inf
```

If iterable is a List or String, iterates over each item

```
loop(["a", "b", "c"], item, idx)(print(item + idx))
# prints "a0" "b1" "c2"
```

```
loop("abc", item, idx)(print(item + idx))
# prints "a0" "b1" "c2"
```

A few loop keywords are supported as well:  
`<<` breaks out of the current loop iteration  
`>>` continues to the next loop iteration

```
loop("abc", item, idx)(
  print(item + idx)
  <<
)
# prints "a0"
```

A few noteworthy function-loop interactions:

- Returning `<<<` from a loop inside a function is valid and will immediately return from that function.
- Breaking `<<` or continuing `>>` inside a function but not inside a loop running in that function is invalid.
- Breaking `<<`, continuing `>>`, or returning `<<<` from not inside a loop or function at all is invalid.

# INTERPRETER

Luna's interpreter is a recursive tree walking interpreter that evaluates Expressions into Runtime Values.

An Expression can be a Python int/bool/str/list, or an Expression class.

A Runtime Value is simply the output of the Python code that the interpreter is written in. For example, a Runtime Value may be a Python string "foo".

Example of (Python) Interpreter code which produces and executes a recursive Factorial function with `n=4` that will print `24`:

```
fact = Function(
  ["n"],
  Program([
    Switch(
      Lte([VarGet("n"), 2]),
      [True, False],
      [
        Return(VarGet("n")),
        Return(Product([
          VarGet("n"),
          Invoke(VarGet("fact"), [Difference([VarGet("n"), 1])])
        ]))
      ],
    )
  ])
)
p = Program([
  VarSet("fact", fact),
  Print(Invoke(VarGet("fact"), [4]))
])
```

The actual Luna code to generate this interpreter code would be:

```
-> fact function(n){
  switch(n<=2)`
    true >>> <<< n
    false >>> <<< n * fact(n - 1)
  `
}
print(fact(4))
```

# PARSER

TODO

# TOKENIZER

Luna's Tokenizer is implemented as a small finite state machine. It iterates through all charaters in a `.luna` file and breaks them down into a 1D array of Tokens, which can then be fed to the parser.

Examples of Tokens include:

- `String`, `Number`, `True`, `False`, `Identifier`, `Equals`, `Minus`

# BOOTSTRAPPING

To run tests: `python -m pytest` (runs all test files and methods starting with `test_`)
