# INTRODUCTION

Luna is an experiment into building a small programming language.

It is a tokenizer + parser + interpreter system implemented in Python. 

# HIERARCHICAL TYPES

Luna supports these Value types:
1. List
2. String
3. Number
4. Boolean

String, Number, and Boolean are Primitive Value types. List is a List of Primitives, or nested Lists.

Types in Luna are hierarchical, with List at the top and Boolean at the bottom. In operations between incompatible types, lower types will generally be coerced into higher types.

Luna does support converting higher types down to lower types, but this should be used sparingly, as it goes against the idea of hierarchical types.

Luna does not feature a `null` type; instead it uses `false`, as that is the falsey value of the lowest type in the hierarchy. Additionally, there is one falsey value for each type: `[]`, `""`, `0`, `false.`

# CROSS TYPE OPERATIONS

Cross-type operations across Values are generally allowed, and will respect the type hierarchy. However, each operation gets to define which operations are allowed, and when type coercion is appropriate. 

Operations evaluate from left-to-right, and short-circuit when possible.

Luna operations are designed with reversability in mind. For example, Plus can be reversed with Minus, and Times can be reversed with Divide.

While interesting cross-type operations is not the main focus of the language, some unconventional ones are allowed:
- Addition/Subtraction of strings and lists via concatenation and inverse concatenation (removing a matching sequence from the end)
- Multiplication/Division of strings and lists via sequence repetition

Examples:
`true + 1 + 1 + 1 + "ue" = "true111ue"`
`true - 1 - 1 - 1 - "ue" = "tr"`
Explanation: the highest type in the list is string, so each item is coerced into a string, then concatenation is performed.

`"ab" * 2 = "abab"`
`"abab" / 2 = "ab"`
`"abab" / "ab = 2`
`"abab" / 2 = "ab"`
Explanation: sequence repetition, then reversal of sequence repetition.

`"abab" * -2 = "baba"`
`"baba" / -2 = "ab"`
`"baba" / "ab" = -2`
Explanation: multiplying and dividing strings and lists by negative numbers creates their "inverse": a reversed sequence!
 
# COMPOSABLE PROGRAMS

The fundamental representation of a sequence of Expressions in Luna is a Program, represented by a sequence of Expressions separated by newlines. A Program will evaluate to the last expression in the sequence.

```
print(1)
print(2)
print(3)
```
Explanation: a .luna file in its entirety is a Program!

```
=>()(
  1
  2
  3
)
```
Explanation: a Function body is also a Program! This function will return `3`

One eventual goal of Luna is to implement composable Programs - for example, combining two Programs by concatenating their lists of Expressions.

# FROZEN EXPRESSIONS

In Luna, you can write `<>` before an Expression to Freeze it. A Frozen Expression will not be evaluated the next time it is evaluated. Then, you can freely re-assign the expression to other Variables, or delay its evaluation until later.

Every Expression in Luna can be frozen, including Switches! This should hopefully allow for some creative program designs.

Any Frozen expression can be forced to Evaluate if it is Invoked using `()` (see below).

At the AST level, Freezing an Expression means wrapping it in a Frozen class, which will then be handled by the Interpreter. Function definitions will automatically be frozen without the user needing to write `<>`.

```
-> a print(1)
-> b <>Print(2)
-> c print(3)
```
Explanation: `1, 3` is printed. The `b` variable contains a Frozen Print statement! It is not evaluated until it is invoked.

# INVOCATIONS

In Luna, Invocations, indicated with `()` serve two purposes:
1. Invoke Functions and other Invokables, causing them to Evaluate, with or without Arguments (currently, Function is the only supported Invokable.)
2. Evaluate any Frozen expression, such as a Frozen Print or Switch Expression.

```
-> a print(1)
-> b <>Print(2)
-> c print(3)
b()
```
Explanation: in the same example as before, now we can print `1, 3, 2` by Invoking the `Print(2)`.

# FUNCTIONS AND SCOPING

Luna supports dynamically scoped Functions with Arguments.

Each Function evaluation creates a new Scope, which holds Variable definitions and other scope-related information. If a Scope does not contain a Variable (for getting and setting), the interpreter will try to find that Variable in the next parent Scope.

Example of Function definition and Invocation:
```
-> my_func(a, b)(
  a + b
)
my_func(1, 2)
```

The `<<` keyword can be used to return from a function call, with or without a return expression after it.

Note: at the Interpreter level, a Function is Frozen when defined, but the action of evaluating it when assigning it to a Variable causes it to evaluate and become Un-Frozen. So, the environment will store the function as Un-Frozen. But, the Function body will only be evaluated when Invoked.

# SWITCHES

Luna handles logical branching using Switches. There are no "if statements" - only Switches.
- The Switch condition can be composed.
- Switch cases will be eagerly evaluated when a Switch is evaluated.
- Switch branches will NOT be evaluated until the matching branch was found during runtime.

Switch Evaluated immediately:
```
{4}(
  3 >> print("three")
  4 >> print("four")
  _ >> print("fallback")
)
# prints "four"
```

Frozen Switch with Composed Condition Evaluated at Invocation: 
```
-> my_frozen_switch <>{my_condition}(
  3 >> "three"
  4 >> "four
)
-> my_condition 3
-> my_switch_result my_frozen_switch()
print(my_switch_result) # prints "three"
```
Note: The switch was composed using a variable reference that did not exist at the time! This is allowed, as that variable got defined before the switch was invoked.

Switch shorthand to implement an "if statement":
```
{4=4}(print("I will be printed!"))
{3=4}(print("I will not be printed!"))
```
Explanation: if the switch body is exactly one Expression instead of a sequence of cases and branches, it is treated as a `true` branch.

Switch shorthand to implement "if-then-else" ternary:
```
{4=4}(
  print("I will be printed!")
  print("I will not be printed!")
)
```
Explanation: if the switch body is exactly two Expressions instead of a sequence of cases and branches, it is treated as a `true`/`false` ternary.

# INTERPRETER

Luna's Interpreter uses a recursive evaluation function that evaluates Expressions into Runtime Values.

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
-> fact (n)(
  {n<=2}(
    << n
    << n * fact(n - 1)
  )
)
print(fact(4))
```

# PARSER

TODO

# TOKENIZER

Luna's Tokenizer is implemented as a small finite state machine. It iterates through all charaters in a .luna file and breaks them down into a 1D array of Tokens, which can then be fed to the parser.

Examples of Tokens include:
- String, Number, True, False, Identifier, Equals, Minus

# BOOTSTRAPPING

To run tests: `pytest`
- This command runs all test files starting with "test_". All methods in test files starting with "test_" will be run.
