# INTRODUCTION

Luna is an experiment into building a small programming language.

- Luna is a tokenizer + parser + interpreter system implemented in Python
- This is a hobby project with the goal of building a programming language that can be used to write and run real code in .luna files!
- I am just beginning to study Programming Languages and Compilers as part of my MSCS, so please forgive any scuff!

# HIERARCHICAL TYPES

Luna supports these Value types:
1. List
2. String
3. Number
4. Boolean

String, Number, and Boolean are Primitive Value types. List is a List of Primitives, or nested Lists.

Types in Luna are hierarchical, with List at the top and Boolean at the bottom. In operations between incompatible types, lower types will generally be coerced into higher types.

Luna does support converting higher types down to lower types, but this should be used sparingly, as it goes against the idea of hierarchical types.

Luna does not feature a `null` type. Instead, Luna uses `false`, as that is the lowest-most falsey type in the hierarchy. Additionally, Luna supports one falsey value for each type: `[]`, `""`, `0`, `false.`

# CROSS TYPE OPERATIONS

Cross-type operations, such as summing a list of items of different types, is generally allowed, and will respect the type hierarchy. However, each operation gets to define which operations are allowed, and when type coercion is appropriate. 

Operations evaluate from left-to-right, and short-circuit when possible.

Luna operations are designed with reversability in mind. For example, plus can be reversed with minus, and times can be reversed with divide.

Luna allows to add and subtract strings and lists via concatenation and inverse concatenation (removing a matching sequence from the end).

Luna allows to multiply and divide strings and lists via sequence repetition.

Examples:
`true + 1 + 1 + 1 + "ue" = "true111ue"`
`true - 1 - 1 - 1 - "ue" = "tr"`
Explanation: in addition and subtraction, the return type is the highest type in the list (string). so, each item is coerced into a string, then concatenation is performed.

`"ab" * 2 = "abab"`
`"abab" / 2 = "ab"`
`"abab" / "ab = 2`
`"abab" / 2 = "ab"`

Luna also supports multiplying and dividing strings and lists by negative counts!
`"abab" * -2 = "baba"`
`"baba" / -2 = "ab"`
`"baba" / "ab" = -2`

Note that cross-type operations are generally only permitted across Value types, as opposed to across all keywords. After all, multiplying a function by a list makes no sense. However, Blocks are able to be added together, and multiplied by numbers to repeat them (more on this later).
 
# BLOCKS

The fundamental representation of a sequence of Expressions in Luna is called a Block, represented by `()`. By default, a Block will be evaluated to its last Expression.

A Block as part of another Expression:
```
print(
  (3, 4, 5)
) # 5
```

A .luna program in its entirety is considered to be a Block!

```
3
4
5
```

# FROZEN EXPRESSIONS

In Luna, you can write `<>` before an Expression to Freeze it. A Frozen Expression will not be evaluated the next time it is evaluated. This is especially useful for defining Expressions like Functions, as Functions should be evaluated when Invoked, not when defined. In fact, Functions in Luna will be automatically Frozen by the parser, so that you do not need to write `<>`.

Say we write `<>(print(3))`. The Block containing the Print Expression is Frozen, and the next time this is Evaluated, the Freeze will be consumed, and `(print(3))` will be returned. Note that this does not actually Print anything. 

Any Frozen expression can be forced to Evaluate if it is Invoked (see below).

At the AST level, Freezing an Expression means wrapping it in a Frozen class, which will then be handled by the Interpreter.

Example: Freezing a block and then Invoking it later (see next section)
```
-> a 1
-> my_block = <>(
  -> a 2
)
print(a) # 1
my_block()
print(a) # 2
<>(
  -> a 2
)()
print(a) # 3
```

# INVOCATIONS

In Luna, Invocations, indicated with `()` serve two purposes:
1. Invoke, Functions, Switches, and Loops, causing them to Evaluate, with or without Arguments
2. Evaluate a Frozen expression, such as a Frozen Block.

Invoking this Frozen Block will Print "3": `<>(print(3))()`

# FUNCTIONS AND SCOPING

Luna supports Functions with Arguments.

Each Function evaluation creates a new Scope, which holds Variable definitions. If a Scope does not contain a Variable, the interpreter will try to find that Variable in the next parent Scope. However, Variables can only be set and modified in the current Scope.

Example of Function definition and Invocation:
```
=> my_func (a, b)(
  a + b
)
my_func(1, 2)
```

Note: at the Interpreter level, a Function is Frozen when defined, but the action of evaluating it when assigning it to a Variable causes it to become Un-Frozen. Then, Invoke will run directly on the Un-Frozen Function.

# SWITCHES

Luna handles logical branching using Switches. There are no "if statements" - only Switches. A Switch can be Evaluated immediately, or composed using a Condition, Cases, Branches, and Default Branch, and Evaluated later.

Switch Evaluated immediately:
```
-> x {4}(
  3 >> "three"
  4 >> "four
)
print(x) # "four"
```

Frozen Switch Evaluated at Invocation: 
```
-> x <>{4}(
  3 >> "three"
  4 >> "four
)
-> y x()
print(y) # "four"
```

# INTERPRETER

Luna's Interpreter uses a recursive evaluation function that evaluates Expressions into Runtime Values.

An Expression can be a Python int/bool/str/list, or an Expression class.

A Runtime Value is simply the output of the Python code that the interpreter is written in. For example, a Runtime Value may be a Python string "foo".

# PARSER

TODO

# TOKENIZER

Luna's Tokenizer is implemented as a small finite state machine. It iterates through all charaters in a .luna file and breaks them down into a 1D array of Tokens, which can then be fed to the parser.

Examples of Tokens include:
- String, Number, True, False, Identifier, Equals, Minus

# BOOTSTRAPPING

To run tests: `pytest`
- This command runs all test files starting with "test_". All methods in test files starting with "test_" will be run.
