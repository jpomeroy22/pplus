# Lab 4: Statements - pplus

## Grammar
```
program    → statement* EOF ;
statement  → exprStmt | printStmt ;
exprStmt   → expression ";" ;
printStmt  → "print" expression ";" ;
```
Expression grammar is the same as Lab 3.

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
- Leftover tokens after an expression are an error instead of being ignored

From Lab 4:
- `true`/`false` turn into `1`/`0` in math, and `0` is false, anything else is true
- `print` shows strings without quotes, so `print "one";` shows `one`

## Statements
- `1 + 2;` runs the expression and doesn't print anything
- `print 1 + 2;` runs the expression and prints it
- Every statement needs a `;` at the end
- Statements run top to bottom

## Errors
- Format: `[line N] Error: message`
- Missing `;`: `Expect ';' after expression.` or `Expect ';' after value.`
- Panic mode: after an error, `skip_to_next_statement()` skips ahead to after a `;` or to the next keyword like `print`, then keeps parsing, so it can find more than one error
- If there's any syntax error, nothing runs

## How to Run
- Python3, no extra packages. Run from repo root.
- REPL: `python src/pplus.py` (needs a `;` at the end of each line)
- Test 1: `python src/pplus.py test/lab4/test1.pp`
- Test 2: `python src/pplus.py test/lab4/test2.pp`

## Tests

### Test 1, syntax errors and panic mode
Input:
```
"one"
true;
print 2 +
```
Expected: two errors, nothing runs

Actual:
```
[line 2] Error: Expect ';' after expression.
[line 3] Error: Expect expression.
```

### Test 2, expression and print statements
Input:
```
4 + 2;
print "one";
print true;
print 1 + 2;
print none;
```
Expected: `4 + 2;` prints nothing, the 4 prints show their values

Actual:
```
one
true
3
none
```

All tests pass.

## Known limitations
- Only expression and print statements, no variables yet
- Errors give the line number but not which token caused it
- REPL needs a `;` at the end of each line
- No failing tests