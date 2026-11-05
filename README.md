# INTRODUCTION

Luna is designed to be a fun, expressive, and Turing-complete programming language. Here are a few design philosophies that it follows:
1. Types are hierarchical.
2. Operations between different types are generally allowed.
3. Outside of Primitive Values, Lists are the core implementation structure, and are the building blocks for everything else: Functions, Switches, etc.
4. Since most things are ultimately Lists, they are allowed to be broken down into parts and composed together, just like lists can be sliced and concatenated.

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

Additionally, Luna does not feature a "null" type. Instead, Luna uses "false", as that is the lowest-most type in the hierarchy.

# 2. CROSS TYPE OPERATIONS

Cross-type operations, such as summing a list of items of different types, is generally allowed, and will respect the type hierarchy. 

Arithmetic operations will operate from left-to-right, and the output type will be the highest type in the List. Specifically, arithmetic operations such as "minus" are implemented using reduction, and the accumulator will be set to the first item converted to the highest type in the List.   

Example: true - 1 - 1 - 1 = -2
Explanation: the highest type in the items is number, so the output will be a number. True converted to a number is 1, so we have 1 - 1 - 1 - 1 = -2.

Example - what if in the above, we subtracted "ue"?: true - 1 - 1 - 1 - "ue" = "tr"
Explanation: the highest type is now a string. The accumulator in the reduction is boolean true converted into a string: "true". "true" does not end with "1", so the "minus ones" do nothing. But, "true" does end with "ue", so subtracting "ue" from "true" yields "tr". 
(note that subtraction between lists or strings is implemented as "inverse contatenation", that is, removing a matching sequence from the end of the item.)

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

