# INTRODUCTION

Luna is designed to be a fun, expressive, and Turing-complete programming language. Here are a few design philosophies that it follows:
1. Operations between different types are generally allowed, and should produce intuitive results.
2. Other than primitive values, Lists are the core implementation structure, and are the building blocks for more advanced functionality such as Functions, Switches, Loops, Dictionaries.
3. As a result of #2, Functions, Switches, etc. should be able to be broken down into variables and composed together, in the same way that a List can be sliced and concatenated.

# HIERARCHICAL TYPES

Luna supports these data types:
1. List
2. String
3. Number
4. Boolean

String, Number, and Boolean are primitive Value types, referred to in the code using "v" or "V".

List is a list of primitives, or nested lists, referred to in the code using "l" or "L".

Types in Luna are hierarchical, with List at the top and Boolean at the bottom. In operations between incompatible types, lower types will generally be converted into higher types.

Luna does support converting higher types down to lower types, but this should be used sparingly, as it goes against the idea of hierarchical types.

# SCOPING

Luna implements one scope per function call. The main purpose of a scope is to hold variable defintions. If code execution cannot find a Variable defined in the current scope, it will attempt to find it in the next parent scope.

# INTERPRETER

Luna's interpreter uses a recursive evaluation function evl() that evaluates Expressions into Runtime Values.

An Expression can be a Value (String/Number/Boolean), a List, or some other operation that takes Expressions as arguments.

A Runtime Value is simply the output of the Python code that the interpreter is written in. For example, a Runtime Value may be a Python string "foo".

All Luna operations are implemented using Runtime Values. Expressions are only to be used in evl().
