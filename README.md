# INTRODUCTION

Luna is an experiment into building a small programming language!

It is a tokenizer + parser + interpreter system implemented in Python.

The purpose for Luna's existence is to be a fun, lightweight programming language with cool behaviors that can be used to write real scripts!

# THE LUNA MANIFESTO (WIP)

1. Intuitive is good.
2. Clarity is good.

# OPERATOR PRECEDENCE, KEYWORDS, AND SYNTAX

Operator Precedence (all operators have left-to-right associativity):

```
HIGHEST PRECEDENCE
()                 grouping
()                 invocation
-                  inverse
^                  exponent
*, /, %            multiplication, division, remainder
+, -               addition, subtraction
>, <, >=, <=, =    equality, inequality
&                  and
|                  or
>>, !>             ternary
LOWEST PRECEDENCE
```

Reserved keywords:

```
true               boolean true
false              boolean false
->, =>             local/global variable assignment
<>                 freeze
if, else           if/else statement
loop               loop definition
continue           loop continue
break              loop break
function           function definition
return             function return
switch             switch definition
map                map definition (key-value pair collection)
```

Commonly used syntax:

```
{}                 program definition
()                 grouping or invocation
[]                 list definition
``                 switch body definition
\n                 a newline indicates the end of a complete expression.
                   newlines in an incomplete expression are ignored.
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

# MAPS

A Map, or a mapping of keys to values, is implemented as an associative array where each element is a list of size 2. The first element is the key, and the second element is the value. A Map can be written as follows:

```
map(
  [key1, value1],
  [key2, value2],
)
```

Composition is allowed when creating a Map - imagine that `map()` is a function, and each argument is an expression that evaluates to a list of size 2. The list of size 2 invariant is enforced at evaluation time. Note that since Maps are associative arrays, keys and values can be any valid expression, and duplicate keys are allowed. This is an intentional design choice to promote flexibility. 

A Map is considered to be a special construct rather than a Value type, so operations that can normally be performed using Value types do not apply to Maps. Instead, Map helper functions will be provided.

# POLYMORPHISM

Cross-type operations across Values are generally allowed, and will respect the type hierarchy. Each operation decides which cross-type interactions are allowed, and when type coercion is appropriate.

Operations evaluate from left-to-right, are left-associative, and short-circuit when possible.

Operations are designed with reversability in mind. For example, Plus can be reversed with Minus, and Times can be reversed with Divide.

While interesting cross-type operations is not the main focus of the language, some unconventional ones are allowed:

Addition/Subtraction of strings and lists is concatenation and inverse concatenation (removing a matching sequence from the end):
`true + 1 + 1 + 'ue' = '3ue'`  
`true - 'ue' = 'tr'`

Multiplication/Division of strings and lists is sequence repetition:
`'ab' * 2 = 'abab'`  
`'abab' / 2 = 'ab'`  
`'abab' / 'ab = 2`  
`'abab' / 2 = 'ab'`

Multiplying and dividing strings and lists by negative numbers creates their 'inverse': a reversed sequence!  
`'abab' * -2 = 'baba'`  
`'baba' / -2 = 'ab'`  
`'baba' / 'ab' = -2`

# COMPOSABLE PROGRAMS

The fundamental representation of a sequence of Expressions is a Program, represented by a sequence of expressions inside curly braces `{}` separated by newlines `\n`. A Program will evaluate to the last expression in the sequence, unless the Program is a Function Body and `return` is used. A `.luna` file in its entirety is a Program, even if `{}` are not explicitly written. Examples of Programs:

```
# A .luna file in its entirety is a Program.
1
2
3
```

```
# Programs can be evaluated and assigned to variables.
-> x {
  1
  2
  3
}
print(x) # prints 3
```

```
# a Function body is a Program. Function bodies will not be evaluated until invoked.
function(){
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

Certain constructs that do not evaluate by default do not need to be explicitly frozen, such as Function Bodies.

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

Invoking a non-invokable, non-frozen expression is allowed - the expression will simply be evaluated normally.

# FUNCTIONS, SCOPES, AND VARIABLES

Functions are defined using the `function` keyword, a comma-separated sequence of params, and a Program.

`function(params)Program`

Each Function invocation creates a new Scope, which holds local variable definitions and other scope-related information. Variable scoping rules include:

- Variable getting will search in the current scope first, then in parent scopes.
- Variable setting using `->` will only set the variable inside the current scope.
- Variable setting using `=>` will search the current scope and all parent scopes for the variable, and set the variable in all scopes in which it was defined! If no definitions were found, it will behave the same as `->`.
- A variable name must start with a letter or underscore, and only contain letters, numbers, and underscores.

```
-> my_func function(a, b){
  a + b
}
print(my_func(1, 2)) # prints 3
```

The `return` keyword is used to return from a function invocation, with or without a return expression. If `return` is not provided, the evaluation of the last expression in the function body will be returned.

# CONDITIONALS: IF-THEN-ELSE, TERNARY

An If-Then-Else construct can be created using the `if` and `else` keywords:

`if(condition)Program else Program`

Examples:
```
if (1+1=2) {
  print(true)
}
```
```
if (1+1=3) {
  print(true)
} else {
  print(false)
}
```

An If-Then-Else can also be constructed using ternary operators `>>` and `!>`. The expression after `>>` is the true branch, and the expression after `!>` is the false branch. These ternary operators are not usable as standalones - they can only be used in a ternary expression.

Examples:
```
-> x 3 = 3 >> "equal" !> "not equal"
print(x) # "equal"
```
```
-> x 3 = 4 >> "equal" !> "not equal"
print(x) # "not equal"
```

# CONDITIONALS: SWITCH

A Switch can be written using the `switch` keyword, and backticks to define the switch body:

```
switch(condition)`
  case1: branch1,
  case2: branch2,
  _: defaultbranch
  ...
`
```

At runtime, `condition` will be evaluated, then the cases will be evaluated from top to bottom until a match is found. Then, the matching case's branch will be evaluated. Unreached cases and branches will not be evaluated. A default case `_` may optionally be provided; as soon as it is reached, the default branch executes. If no matching case is found, the switch returns `false`. Individual switch cases and branches can be composed using expressions.

Note that the switch body is indicated with backticks, rather than any other grouping syntax, as a switch body has unique syntax and behavior. Switch cases are separated from branches by colons `:`, and different case-branch pairs are separated by commas `,`. 

```
-> result switch(3+4)`
  6: 'six',
  7: 'seven'
`
print(result) # 'seven'
```

```
-> result switch(3+4)`
  6: 'six',
  _: 'default_value'
`
print(result) # 'default_value'
```

```
-> result switch(3+4)`
  6: 'six'
`
print(result) # false
```

# LOOPS

A loop can be created using the `loop` keyword:

`loop(iterable:number|boolean|list|string, iterator, index)Program`

A loop will not create a new scope; its contents will be evaluated in the current scope.

Identifier names for `iterator` and `index` are optional. If provided, new temporary variables will be created in the current scope corresponding to the given identifier names. These temporary variables will be reverted after the loop terminates.

If iterable is a Number, repeats the loop number times

```
loop(3){print(0)}
# prints 0 0 0
```

If iterable is a boolean True, that is an infinite loop! If iterable is boolean False, nothing will happen.

```
loop(True, item, idx){print(idx)}
# prints 0 1 2...inf
```

If iterable is a List or String, iterates over each item

```
loop(['a', 'b', 'c'], item, idx){print(item + idx)}
# prints 'a0' 'b1' 'c2'
```

```
loop('abc', item, idx){print(item + idx)}
# prints 'a0' 'b1' 'c2'
```

A few loop keywords are supported as well:  
`break` breaks out of the current loop iteration  
`continue` continues to the next loop iteration

```
loop('abc', item, idx){
  print(item + idx)
  break
}
# prints 'a0'
```

A few noteworthy function-loop interactions:

- `return` from a loop inside a function will immediately return from that function.
- `break` or `continue` inside a function but not inside a loop is invalid
- `break`, `continue`, or `return` from not inside a loop or function is invalid

# BUILT-IN FUNCTIONS

Built-in functions are implemented as Python methods keyed to variables in the interpreter's global scope (environment). They may be invoked by simply invoking their identifier name, similar to a normal function invocation. Built-ins may be shadowed if the user assigns a different value to the built-in name, but then a warning will be printed to the console.

A list of all built-in functions:
```
  # Generic built-ins:
  print(expr) -> False:              print to console
  boolean(expr) -> boolean:          convert to boolean
  string(expr) -> string:            convert to string
  number(expr) -> number:            convert to number
  list(expr) -> list:                convert to list

  # List built-ins:
  lmap(list, function) -> list:      list map
  filter(list, function) -> list:    list filter
  insert(list, item, idx) -> item:   inserts item into list at idx.
                                     inserts at end of list if
                                     idx not provided
  pop(list, idx) -> item:            removes and returns item at idx
                                     returns last item if idx not provided
  get(list, idx) -> number:          get item from list by index
  getindex(list, item) -> number:    get item index from list by value
  find(list, fn) -> ite:             get item from list by callback
  findindex(list) -> number:         get item index from list by callback
  slice(list, idx1, idx2) -> list:   slice list by range [idx1, idx2)
  sum(list) -> value:                sum of all items in a list
  difference(list) -> value:         difference of all items in a list
  product(list) -> value:            product of all items in a list
  quotient(list) -> value:           quotient of all items in a list
  remainder(list) -> value:          remainder of all items in a list
  lt(list) -> boolean:               < inequality chain 
  lte(list) -> boolean:              <= inequality chain
  gt(list) -> boolean:               > inequality chain
  gte(list) -> boolean:              >= inequality chain
  equals(list) -> boolean:           equality chain
  all(list) -> boolean:              whether all items in a list are truthy
  some(list) -> boolean:             whether at least one item in a list is truthy
```


# INTERPRETER

Luna's interpreter is a recursive tree-walking interpreter that evaluates Expressions into Runtime Values.

An Expression can be a Python int/bool/str/list, or an Expression class.

A Runtime Value is simply the output of the Python code that the interpreter is written in. For example, a Runtime Value may be a Python string "foo".

Example of Python Interpreter code which produces and executes a recursive Factorial function with `n=4` that will yield `24`:

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

The actual Luna code to generate this interpreter code could be:

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

- `String`, `Number`, `True`, `False`, `Name`, `Equals`, `Minus`

# BOOTSTRAPPING

This project requires Python 3.13.

Note: the language is still in development and many key features are missing, I don't recommend using the language seriously for now.

All bootstrapping commands should be run from the root directory:

To install dependencies:

`pip install -r requirements.txt`

To install the Luna programming language from a clone of this repo:

`python -m pip install -e .`

To install the Luna programming language from GitHub:

`python -m pip install git+https://github.com/smokie777/luna-programming-language.git`

To run a .luna file:

`luna filename.luna`

# TESTING

All testing commands should be run from the root directory:

`python -m pytest` to run all test files and methods starting with `test_`

`python -m pytest -s` to run all tests, and also see print() statements

`python -m pytest parser/test_parse.py` to run one specific test file

`python -m pytest parser/test_parse.py::test_method_name` to run one specific test method

`python -m parser.luna_parse` to run one specific file
