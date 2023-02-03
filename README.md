# Basic Interpreter written in python
### It's a mix of python and c-based languages in one interpreted language with strong typization.

## Example
```python
def factorial |n int| -> int {
    if n <= 1 ! 1;
    ! [factorial n - 1] * n;
}

res int = [factorial 10];
[shown [int_to_str res]]; # 3628800 
```

## All features
```python
# types/vars
a int; a = 3;
b float = 2.0 + (-2.0) * 1.0 / 100.0;
c bool = true or false;
d str = "hello, world!";
# conditions
if a >= 3 or not b 
    a = 4;
else if a < 3 {
    a = 5;
    b = 2.8;
}
else { c = false; }
# loops
loop {  # infinite loop
    a = a + 1;
    if a > 42
        stop; # break
    else next; # continue
}
even_sum int = 0; 
loop i int, 0..10, 2 {
    even_sum = even_sum + i;
}
# functions
def no_args_func || -> float {
    ! 3.14; # return
}
def args_func |arg1 int, msg str| -> bool {
    ! false;
} 
[args_func 2, "hello"]; # func call
# builtins
[shown "new line message"]; # print with new line
[show "one line msg"]; # casual print
[str_to_int "228"]; # one of the type cast functions
[read "read value: "]; # read str from console
# ... (check builtins/intrinsics.py)
```
Made for studying and demonstration only, so there are no more complex features like arrays, user types, libs imports and mutiple files interpretation.

## Install
After clonning go to the clonned directory and run
```bash
    chmod +x ./run.sh
    ./run.sh file.txt # your filepath here
    # tests
    python3 -m pytest
```
