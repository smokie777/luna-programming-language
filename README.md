# INTRODUCTION

Luna is an experiment into building a small programming language!

It is a tokenizer + parser + interpreter system implemented in Python.

# OPERATOR PRECEDENCE, KEYWORDS, AND SYNTAX

Operator Precedence (all operators have left-to-right associativity):

```
HIGHEST PRECEDENCE
()                 grouping
()                 invocation (distinguished from grouping during parsing)
!                  inverse
^                  exponent
*, /, %            multiplication, division
+, -               addition, subtraction
>, <, >=, <=, =    equality comparison
&                  and
|                  or
>>, !>             if, else
LOWEST PRECEDENCE
```

Reserved keywords:

```
true               boolean true
false              boolean false
->, =>             local/global variable assignment
<>                 freeze
loop               define a loop
continue           loop continue
break              loop break
function           define a function
return             function return
switch             define a switch
print              print to console
map                create a map
boolean, b         convert to boolean
string, s          convert to string
number, n          convert to number
```

Commonly used syntax:

```
{}                 defines a Program
()                 defines construct arguments
[]                 create a list
\n                 a newline indicates the end of an expression (unless in a string)
```

# HIERARCHICAL TYPES

Value types:

1. List
2. String
3. Number
4. Boolean

Types are hierarchical, with List at the top and Boolean at the bottom. In operations between incompatible types, lower types will generally be coerced into higher types.

Higher types may be converted to lower types, but this should be used sparingly, as it goes against the idea of hierarchical types.

There is no `null` type; instead `false` is used, as that is the falsey value of the lowest type in the hierarchy. There is one falsey value for each type: `[]`, `""`, `0`, `false`.

# CROSS TYPE OPERATIONS

Cross-type operations across Values are generally allowed, and will respect the type hierarchy. Each operation decides which cross-type interactions are allowed, and when type coercion is appropriate.

Operations evaluate from left-to-right, are left-associative, and short-circuit when possible.

Operations are designed with reversability in mind. For example, Plus can be reversed with Minus, and Times can be reversed with Divide.

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

The fundamental representation of a sequence of Expressions is a Program, represented by a sequence of expressions inside curly braces `{}` separated by newlines `\n`. A Program will evaluate to the last expression in the sequence. A `.luna` file in its entirety counts as a Program, even if `{}` is not written. Examples of Programs:

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

One eventual goal is to implement composable Programs - for example, combining two Programs by concatenating their lists of expressions.

# FROZEN EXPRESSIONS

`<>` can be written before an expression to Freeze it. A Frozen expression will not be evaluated until invoked using `()`. Frozen expressions can be freely assigned to other variables. Variable references will be set at frozen expression invocation, rather than at creation.

Every Expression can be frozen! This should (hopefully) allow for some creative program designs.

At the AST level, Freezing an expression means wrapping it in a Frozen node. When the Interpreter evaluates a Frozen expression, it will strip away the Frozen node and return the un-evaluated node inside.

Certain constructs will be automatically Frozen without requiring the `<>` syntax, such as function bodies.

```
-> a print(1)
-> b <>Print(2)
-> c print(3)
# prints 1, 3
```

# INVOCATIONS

Invocations, indicated with `()`, serve two purposes:

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

Functions are defined using the `function` keyword. 

Each Function invocation creates a new Scope, which holds local variable definitions and other scope-related information. Variable scoping rules include:

- Variable getting will search in the current scope first, then in parent scopes.
- Variable setting using `->` will only set the variable inside the current scope.
- Variable setting using `=>` will search the current scope and all parent scopes for the variable, and set the variable in all scopes in which it was defined! If no definitions were found, it will behave the same as `->`.
- A variable name must start with a letter, and only contain letters, numbers, and underscores.

```
-> my_func function(a, b){
  a + b
}
print(my_func(1, 2)) # prints 3
```

The `return` keyword is used to return from a function invocation, with or without a return expression. If `return` is not provided, the evaluation of the last expression in the function body will be returned.

# SWITCHES AND CONDITIONALS

A Switch can be written with the following syntax:

`switch(condition, Map, default)`

At runtime, `condition` will be evaluated, and compared via equality to the evaluation of each `Map` key in order of top to bottom. If a match is found, then the matching key's value will be evaluated and returned, and the switch will exit. Only keys up until the matching key will be evaluated, and only the matching key's value will be evaluated. If a match is not found, the switch will return the optional `default` expression's evaluation, and if `default` is not provided, the switch will return `false`. A `Frozen Map` assigned to a variable may also be provided to a switch. 

```
-> result switch(3+4, map(
  6: "six",
  7: "seven"
))
print(result) # "seven"
```

```
-> result switch(3+4, map(
  6: "six"
), "default_value")
print(result) # "default_value"
```

```
-> result switch(3+4, map(
  6: "six"
))
print(result) # false
```

```
-> my_switch_branches <>map(
  6: { # this is a program with two expressions!
    print("i am")
    print("six")
  },
  7: {
    print("i am")
    print("seven")
  },
)
switch(3+4, my_switch_branches) # prints "i am", "seven"
```

Conditionals may also be implemented using `if-then-else` syntax, using `>>` to represent `if` and `!>` to represent `else`.

If condition is truthy, then evaluate if_branch
`condition >> if_branch`

If condition is truthy, then evaluate if_branch, else evaluate else_branch
`condition >> if_branch !> else_branch`

If condition is falsey, then evaluate else_branch
`condition !> else_branch`

# LOOPS

A loop can be created as follows:

`loop(iterable:number|boolean|list|string, iterator, index)(Program)`

A loop will not create a new scope; its contents will be evaluated in the current scope.

`iterator` and `index` are optional. If provided, new temporary variables will be created in the current scope corresponding to the given identifier names. These temporary variables will be reverted after the loop finishes (or is broken out of).

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
`break` breaks out of the current loop iteration  
`continue` continues to the next loop iteration

```
loop("abc", item, idx)(
  print(item + idx)
  break
)
# prints "a0"
```

A few noteworthy function-loop interactions:

- `return` from a loop inside a function will immediately return from that function.
- `break` or `continue` inside a function but not inside a loop is invalid
- `break`, `continue`, or `return` from not inside a loop or function is invalid

# INTERPRETER

Luna's interpreter is a recursive tree-walking interpreter that evaluates Expressions into Runtime Values.

An Expression can be a Python int/bool/str/list, or an Expression class.

A Runtime Value is simply the output of the Python code that the interpreter is written in. For example, a Runtime Value may be a Python string "foo".

Example of (Python) Interpreter code which produces and executes a recursive Factorial function with `n=4` that will yield `24`:

```
fact = Function(
  ["n"],
  Program([
    IfThenElse(
      Lte([VarGet("n"), 2]),
      VarGet("n"),
      Product([
        VarGet("n"),
        Invoke(VarGet("fact"), [Difference([VarGet("n"), 1])])
      ])
    )
  ])
)
p = Program([
  VarSet("fact", fact),
  Invoke(VarGet("fact"), [4])
])
luna_eval(p) == 24 # True

```

The actual Luna code to generate this interpreter code would be:

```
-> fact function(n){
  n <= 2
    >> n
    !> n * fact(n - 1)
}
fact(4)
```

# PARSER

Luna's Parser is a recursive descent parser that takes a list of tokens and converts it into an AST of Expression nodes. The operator precedence section earlier is fully implemented here.

# TOKENIZER

Luna's Tokenizer is implemented as a finite state machine. It iterates through all charaters in a `.luna` file and breaks them down into a 1D array of Tokens, which can then be fed to the parser.

Examples of Tokens include:

- `String`, `Number`, `True`, `False`, `Identifier`, `Equals`, `Minus`

# BOOTSTRAPPING

To run tests:

`python -m pytest` to run all test files and methods starting with `test_`

`python -m pytest parser/test_parse.py` to run one specific test file

`python -m parser.luna_parse` to run one specific file
