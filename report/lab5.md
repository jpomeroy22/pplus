# Lab 5: Variables - pplus

## Grammar
```
program     → declaration* EOF ;
declaration → letDecl | statement ;
letDecl     → "let" IDENTIFIER ( "=" expression )? ";" ;
statement   → exprStmt | printStmt | block ;
block       → "{" declaration* "}" ;
exprStmt    → expression ";" ;
printStmt   → "print" expression ";" ;

expression  → assignment ;
assignment  → IDENTIFIER "=" assignment | equality ;
primary     → NUMBER | STRING | "true" | "false" | "none"
            | "(" expression ")" | IDENTIFIER ;
```
Rest of the expression grammar is the same as Lab 3.

## Changes from Lox
From Lab 1:
- fun into def, nil into none, var into let
- Added % modulo
- Comments use # instead of //
- Only ASCII letters/digits, anything else is unexpected character

From Lab 2:
- Literals print as true/false/none instead of Python's True/False/None
- Numbers always print as floats
- AST uses the visitor pattern so we can reuse the same classes later

From Lab 3:
- `%` is in factor
- `none` is a primary literal instead of `nil`

From Lab 4:
- `true`/`false` turn into `1`/`0` in math, and `0` is false, anything else is true
- `print` shows strings without quotes, so `print "one";` shows `one`

From Lab 5:
- Variables use `let` instead of `var`

## Variables
- `let a = 1;` makes a variable
- `print a;` uses it
- `a = 2;` changes it
- `print a = 1;` prints `1`
- `a = b = 5;` sets both to `5`

## Design Choices
- Using a variable before it's declared: error
- `let a;` with no value: `a` is `none`
- Declaring the same variable twice: allowed, it just replaces the old value
- These are the same as Lox

## Scope
- `{ }` makes a new block
- Variables made in a block are gone after the `}`
- A block can use variables from outside it
- If a block makes a variable with the same name as one outside, it uses its own

## Errors
- Format: `[line N] Error: message`
- Missing `}`: `Expect '}' after block.`
- Bad assignment: `Invalid assignment target.`
- Variable doesn't exist: `Undefined variable 'a'.`

## How to Run
- Python3, no extra packages. Run from repo root.
- REPL: `python src/pplus.py`
- File: `python src/pplus.py test/lab5/scope.pp`
- Tests: `python test/lab5/run_tests.py` -- output saved to test/lab5/output

## Tests

### Test 1, declaring, using, and assigning variables
Input:
```
let a = 1;
print a;
a = 2;
print a;
let b;
print b;
let a = "test";
print a;
print a = 1;
let a = 1;
let b = 2;
print a + b;
a = b = 5;
print a;
print b;
```
Expected: each print shows the current value

Actual:
```
1
2
none
test
1
3
5
5
```

### Test 2, changing an outer variable inside a block
Input:
```
let a = 1;
{
  a = 2;
}
print a;
```
Expected: `2`

Actual:
```
2
```

### Test 3, textbook scope example
Input:
```
let a = "global a";
let b = "global b";
let c = "global c";
{
  let a = "outer a";
  let b = "outer b";
  {
    let a = "inner a";
    print a;
    print b;
    print c;
  }
  print a;
  print b;
  print c;
}
print a;
print b;
print c;
```
Expected: each block uses its own variables first

Actual:
```
inner a
outer b
global c
outer a
outer b
global c
global a
global b
global c
```
- Inner block has its own `a`, uses the outer `b`, and the global `c`
- Outer block has its own `a` and `b`, and uses the global `c`
- After both blocks end, it's back to the global values

### Test 4, missing `}`
Input:
```
{
  print 1;
```
Expected: error

Actual:
```
[line 2] Error: Expect '}' after block.
```

### Test 5, bad assignment
Input:
```
1 + 2 = 3;
```
Expected: error

Actual:
```
[line 1] Error: Invalid assignment target.
```

### Test 6, using a variable that doesn't exist
Input:
```
print z;
```
Expected: error

Actual:
```
[line 1] Error: Undefined variable 'z'.
```

### Test 7, assigning a variable that doesn't exist
Input:
```
z = 1;
```
Expected: error

Actual:
```
[line 1] Error: Undefined variable 'z'.
```

### Test 8, using a variable outside its block
Input:
```
{
  let a = 1;
}
print a;
```
Expected: error

Actual:
```
[line 4] Error: Undefined variable 'a'.
```

### Test 9, REPL
Input:
```
let a = 4;
print a * 2;
a = a + 1;
print a;
```
Expected: `8` then `5`

Actual:
```
> > 8
> > 5
>
```

All tests pass.

## Known limitations
- In the REPL, a block has to be on one line
- Errors give the line number but not which token caused it
- No failing tests