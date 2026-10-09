# Lab 2: AST Printer - pplus

## Expression Grammar
```
expression → literal | unary | binary | grouping ;
literal    → NUMBER | STRING | "true" | "false" | "none" ;
grouping   → "(" expression ")" ;
unary      → ( "-" | "!" ) expression ;
binary     → expression operator expression ;
operator   → "==" | "!=" | "<" | "<=" | ">" | ">=" | "+" | "-" | "*" | "/" | "%" ;
```

## Operators and Literals
- Unary: `-` (negative), `!` (not)
- Binary math: `+ - * / %`
- Binary comparison: `== != < <= > >=`
- Literals: numbers, strings, `true`, `false`, `none`

## Changes from Lox
From Lab 1:
- fun into def, nil into none, var into let
- Added % modulo
- Comments use # instead of //
- Only ASCII letters/digits, anything else is unexpected character

From Lab 2:
- Literals print as true/false/none instead of Python's True/False/None
- Strings print with quotes, so we can have "none" (string) and none (literal)
- Numbers always print as floats
- AST uses the visitor pattern so we can reuse the same classes later

## How to Run
- Python3, no extra packages. Run from repo root.
- Tests: `python test/lab2/test_astprinter.py`

## Tests

### Lab example, unary minus, multiply, grouping `-123 * (45.67)`
- AST: `Binary(Unary(minus, Literal(123.0)), star, Grouping(Literal(45.67)))`
- Expected: `(* (- 123.0) (group 45.67))`
- Actual: `(* (- 123.0) (group 45.67))`

### Addition, modulo, grouping `(1 + 2) % 3`
- AST: `Binary(Grouping(Binary(Literal(1.0), plus, Literal(2.0))), percent, Literal(3.0))`
- Expected: `(% (group (+ 1.0 2.0)) 3.0)`
- Actual: `(% (group (+ 1.0 2.0)) 3.0)`

### Division and subtraction, nested binary `10 / 5 - 1`
- AST: `Binary(Binary(Literal(10.0), slash, Literal(5.0)), minus, Literal(1.0))`
- Expected: `(- (/ 10.0 5.0) 1.0)`
- Actual: `(- (/ 10.0 5.0) 1.0)`

### Equality with grouped math on both sides `(1 + 2) == (4 - 1)`
- AST: `Binary(Grouping(Binary(Literal(1.0), plus, Literal(2.0))), equal_equal, Grouping(Binary(Literal(4.0), minus, Literal(1.0))))`
- Expected: `(== (group (+ 1.0 2.0)) (group (- 4.0 1.0)))`
- Actual: `(== (group (+ 1.0 2.0)) (group (- 4.0 1.0)))`

### Greater than, less than or equal, not equal `(4 > 5) != (6 <= 7)`
- AST: `Binary(Grouping(Binary(Literal(4.0), greater, Literal(5.0))), bang_equal, Grouping(Binary(Literal(6.0), less_equal, Literal(7.0))))`
- Expected: `(!= (group (> 4.0 5.0)) (group (<= 6.0 7.0)))`
- Actual: `(!= (group (> 4.0 5.0)) (group (<= 6.0 7.0)))`

### Less than, greater than or equal, not equal `(5 < 4) != (6 >= 6)`
- AST: `Binary(Grouping(Binary(Literal(5.0), less, Literal(4.0))), bang_equal, Grouping(Binary(Literal(6.0), greater_equal, Literal(6.0))))`
- Expected: `(!= (group (< 5.0 4.0)) (group (>= 6.0 6.0)))`
- Actual: `(!= (group (< 5.0 4.0)) (group (>= 6.0 6.0)))`

### Unary not, true, false `!true == false`
- AST: `Binary(Unary(bang, Literal(True)), equal_equal, Literal(False))`
- Expected: `(== (! true) false)`
- Actual: `(== (! true) false)`

### Modulo and subtraction, nested binary `10 % 2 - 1`
- AST: `Binary(Binary(Literal(10.0), percent, Literal(2.0)), minus, Literal(1.0))`
- Expected: `(- (% 10.0 2.0) 1.0)`
- Actual: `(- (% 10.0 2.0) 1.0)`

### Decimal number, multiply and add `3.14 * 2 + 1`
- AST: `Binary(Binary(Literal(3.14), star, Literal(2.0)), plus, Literal(1.0))`
- Expected: `(+ (* 3.14 2.0) 1.0)`
- Actual: `(+ (* 3.14 2.0) 1.0)`

### String and none literals `"test" != none`
- AST: `Binary(Literal("test"), bang_equal, Literal(None))`
- Expected: `(!= "test" none)`
- Actual: `(!= "test" none)`

### Edge case, four stacked unary minus `----6`
- AST: `Unary(minus, Unary(minus, Unary(minus, Unary(minus, Literal(6.0)))))`
- Expected: `(- (- (- (- 6.0))))`
- Actual: `(- (- (- (- 6.0))))`

### Edge case, string "none" vs literal none `"none" == none`
- AST: `Binary(Literal("none"), equal_equal, Literal(None))`
- Expected: `(== "none" none)`
- Actual: `(== "none" none)`

### Edge case, nested groupings `((1))`
- AST: `Grouping(Grouping(Literal(1.0)))`
- Expected: `(group (group 1.0))`
- Actual: `(group (group 1.0))`

All tests pass.

## Known limitations
- Trees built by hand, no parser yet
- Numbers always print as floats
- The AST doesn't check if an expression makes sense
- No failing tests