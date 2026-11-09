# RANDOM

This file is for writing down various informal thoughts

TODO:
- combining programs
- multiplying programs

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
