# INTRODUCTION

Luna is designed to be a fun, expressive, and Turing-complete programming language. Here are a few design philosophies:
1. Types are hierarchical.
2. Operations between different types are generally allowed.
3. Outside of Primitive Values, Lists are the core implementation structure, and are the building blocks for everything else: Functions, Switches, etc.
4. Since most things are ultimately Lists, they can be broken down into parts and composed together, just like lists can be sliced and concatenated.

# 1. HIERARCHICAL TYPES

Luna supports these data types:
1. List
2. String
3. Number
4. Boolean

String, Number, and Boolean are primitive Value types.

List is a list of primitives, or nested lists.

Types in Luna are hierarchical, with List at the top and Boolean at the bottom. In operations between incompatible types, lower types will generally be coerced into higher types.

Luna does support converting higher types down to lower types, but this should be used sparingly, as it goes against the idea of hierarchical types.

Luna does not feature a `null` type. Instead, Luna uses `false`, as that is the lowest-most type in the hierarchy. Additionally, Luna supports one Falsey Value for each type: `[]`, `""`, `0`, `false.`

# 2. CROSS TYPE OPERATIONS

Cross-type operations, such as summing a list of items of different types, is generally allowed, and will respect the type hierarchy. However, each operation gets to define which operations are strictly not allowed. 

Most operations operate from left-to-right. When possible, short-circuiting is implemented.

Luna operations are also designed with reversability in mind. For example, plus can be reversed with minus, and times can be reversed with divide.

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

# 3. LISTS AS THE CORE STRURCTURE

Luna sees all advanced functionality as a List. For example, a Function is seen as a List of Expressions.

# 4. EXTREME COMPOSITION!!!

If everything is a List, then everything should be able to be broken apart and composed together.

# SCOPING

Luna implements one scope per function call. The main purpose of a scope is to hold variable defintions. If code execution cannot find a Variable defined in the current scope, it will attempt to find it in the next parent scope. Scoping is implemented at the interpreter level using Environents.

# INTERPRETER

Luna's interpreter uses a recursive evaluation function that evaluates Expressions into Runtime Values.

An Expression can be a Value (String/Number/Boolean), a List, or an Operation that takes Expressions as arguments. Variables are implemented as Operations - both Variable getting and setting. 

A Runtime Value is simply the output of the Python code that the interpreter is written in. For example, a Runtime Value may be a Python string "foo".

All Luna operations are implemented using Runtime Values.

# PARSER

TODO

# TOKENIZER

TODO

# BOOTSTRAPPING

To run tests: `pytest`
- This command runs all test files starting with "test_". All methods in test files starting with "test_" will be run.
