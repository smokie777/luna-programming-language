# RANDOM

This file is for writing down various informal thoughts

TODO:
- combining programs
- multiplying programs
- loops


how do you compute the factorial of 4?

# using a function:
```
-> fact =>(n)(
  {n<=2}(
    2,
    n*fact(n-1)
  )
)
print(fact(4))
```

# using a loop:
```
-> n 4                           # assign n 4
-> result 1                      # assign result 1
<>(                              # create a new block with "(" then freeze it with "<>"! freeze means it wont be evaluated until invoked
  {n<=2}(                        # create a new switch with the condition "n less than or equal to 2"
    return print(result*2),      # if the condition is true, print "result multiplied by 2", then return (this will return for the whole program, as we are not in a function scope!)
    (result*=n, n-=1)            # if the condition is false, assign result "result multiplied by n", then assign n "nminus one"
  )                              # end the switch
)*3()                            # end the frozen block, then repeat the block 3 times, then invoke it. note that "3" could be any higher number, as the block is exited once "n<=2".
```

# different types of loops
Luna provides a `loop` keyword: `loop(iterable:number|boolean|list, iterator)(block)`

A loop will not create a new scope; its contents will be evaluated as if in the current scope.

The iterator is a variable name that will keep track of the value of the current iterator. It will be assigned to the current scope. 

If iterable is a number, repeats the loop number times
```loop(3, i)(print(i))```          prints 0 1 2 
If iterable is a boolean True, that is an infinite loop!
```loop(True, i)(print(i))```       prints 0 1 2 ... inf
If iterable is a list, iterates over each item in the list
```loop([1,2,3], i)(print(i))```    prints 1 2 3

A few loop keywords are supported as well:
`break` breaks out of the current loop iteration
`continue` continues to the next loop iteration

A loop can also be expressed more primitively by multiplying frozen blocks with numbers, then invoking the resulting block. Note that this type of loop, which does not use the `loop` keyword, will neither create a loop scope nor be able to use loop keywords.
```(3*<>(print(1)))()```              prints 1 1 1

By default, a loop will be evaluated on the spot, similar to a Block. However, you can freeze a loop and run it later.
```
-> my_loop <>loop(3, i)(print(i))
print('start')
my_loop()
```
prints 'start' 1 2 3
