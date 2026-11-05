# INTRODUCTION

Luna is designed to be a fun, expressive, and Turing-complete programming language. Here are a few design philosophies that Luna follows:
1. Operations between different types are generally allowed, and should produce intuitive results.
- However, nonsensical operations like "List divide List" should still be disallowed.
2. Other than primitive values, Lists are the core implementation structure, and are the building blocks for more advanced functionality such as Functions, Switches, Loops, Dictionaries.
- As a result, Functions, Switches, etc. should be able to be broken down into variables and composed together, in the same way that a List can be sliced and concatenated.

# HIERARCHICAL TYPES

Luna supports these data types:
1. List
2. String
3. Number
4. Boolean

String, Number, and Boolean are primitive Value types. They are referred to in the code using the letter "v" or "V".

List is a list of primitives, or nested lists. They are referred to in the code using the letter "l" or "L".

Types in Luna are hierarchical, with List at the top and Boolean at the bottom. This means that when performing operations or type coercion between two different types, the lower-priority type will be converted into the higher-priority type.

However, any type can still be converted into any other type using explicit type-conversion functions.

# SCOPING

Luna implements one scope per function call. The main purpose of a scope is to hold variable defintions. If code execution cannot find a Variable defined in the current scope, it will attempt to find it in the next parent scope.

# INTERPRETER

Luna's interpreter uses a recursive evaluation function that evaluates Expressions into Runtime Values.

An Expression can be a Value (String/Number/Boolean), a List, or some other operation that takes Expressions as arguments.

A Runtime Value is simply the output of the Python code that the interpreter is written in. For example, a Runtime Value may be a Python string "foo".
