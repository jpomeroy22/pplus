# Lab 3: Parser - pplus

## Expression Grammar
```
expression → equality ;
equality   → comparison ( ( "!=" | "==" ) comparison )* ;
comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term       → factor ( ( "-" | "+" ) factor )* ;
factor     → unary ( ( "/" | "*" | "%" ) unary )* ;
unary      → ( "!" | "-" ) unary | primary ;
primary    → NUMBER | STRING | "true" | "false" | "none" | "(" expression ")" ;
```

## Precedence and Associativity
Lowest to highest:
- Equality: `== !=` -- left
- Comparison: `> >= < <=` -- left
- Term: `+ -` -- left
- Factor: `* / %` -- left
- Unary: `! -` -- right
- Primary: literals and `( )`

Each rule only calls the one below it, so higher precedence ends up deeper in the tree. The `( ... )*` loops build left to right, so `5 - 2 - 1` is `(5 - 2) - 1`. Parentheses go back to the top, so they override precedence.

## Grammar Changes Since Lab 2
- Lab 2 had `binary → expression operator expression`, which didn't say which operator goes first
- Lab 3 splits it into one rule per precedence level so `*` binds tighter than `+`

## Changes from Lox
From Lab 1:
- fun into def, nil into none, var into let
- Added % modulo
- Comments use # instead of //
- Only ASCII letters/digits, anything else is unexpected character

From Lab 2:
- Literals print as true/false/none instead of Python's True/False/None
- Strings print with quotes, so "none" (string) looks different from none (literal)
- Numbers always print as floats
- AST uses the visitor pattern so we can reuse the same classes later

From Lab 3:
- `%` is in factor
- `none` is a primary literal instead of `nil`
- Leftover tokens after an expression are an error instead of being ignored

## Errors
- Format: `[line N] Error: message`
- Unclosed parenthesis: `Expect ')' after expression.`
- Missing operand or token that can't start an expression: `Expect expression.`
- Leftover tokens: `Unexpected token after expression.`
- Scanner errors from Lab 1 still work, and no tree is printed if there's an error

## How to Run
- Python3, no extra packages. Run from repo root.
- REPL: `python src/pplus.py`
- File: `python src/pplus.py test/lab3/precedence.pp`
- Tests: `python test/lab3/run_tests.py` -- output saved to test/lab3/output

## Tests

### Lab example `-123 * (45.67)`
- Expected: `(* (- 123.0) (group 45.67))`
- Actual: `(* (- 123.0) (group 45.67))`

### Modulo with grouping `(1 + 2) % 3`
- Expected: `(% (group (+ 1.0 2.0)) 3.0)`
- Actual: `(% (group (+ 1.0 2.0)) 3.0)`

### Division before subtraction `10 / 5 - 1`
- Expected: `(- (/ 10.0 5.0) 1.0)`
- Actual: `(- (/ 10.0 5.0) 1.0)`

### Equality with groups on both sides `(1 + 2) == (4 - 1)`
- Expected: `(== (group (+ 1.0 2.0)) (group (- 4.0 1.0)))`
- Actual: `(== (group (+ 1.0 2.0)) (group (- 4.0 1.0)))`

### Greater than, less than or equal, not equal `(4 > 5) != (6 <= 7)`
- Expected: `(!= (group (> 4.0 5.0)) (group (<= 6.0 7.0)))`
- Actual: `(!= (group (> 4.0 5.0)) (group (<= 6.0 7.0)))`

### Less than, greater than or equal, not equal `(5 < 4) != (6 >= 6)`
- Expected: `(!= (group (< 5.0 4.0)) (group (>= 6.0 6.0)))`
- Actual: `(!= (group (< 5.0 4.0)) (group (>= 6.0 6.0)))`

### Unary not, true, false `!true == false`
- Expected: `(== (! true) false)`
- Actual: `(== (! true) false)`

### Modulo before subtraction `10 % 2 - 1`
- Expected: `(- (% 10.0 2.0) 1.0)`
- Actual: `(- (% 10.0 2.0) 1.0)`

### Decimal, multiply before subtract `3.14 * 2 - 1`
- Expected: `(- (* 3.14 2.0) 1.0)`
- Actual: `(- (* 3.14 2.0) 1.0)`

### String and none `"test" != none`
- Expected: `(!= "test" none)`
- Actual: `(!= "test" none)`

### Stacked unary minus `----6`
- Expected: `(- (- (- (- 6.0))))`
- Actual: `(- (- (- (- 6.0))))`

### String "none" vs literal none `"none" == none`
- Expected: `(== "none" none)`
- Actual: `(== "none" none)`

### Nested groupings `((1))`
- Expected: `(group (group 1.0))`
- Actual: `(group (group 1.0))`

### Precedence, no parentheses `1 + 2 * 3 - 4 / 2`
- Expected: `(- (+ 1.0 (* 2.0 3.0)) (/ 4.0 2.0))`
- Actual: `(- (+ 1.0 (* 2.0 3.0)) (/ 4.0 2.0))`

### Left associativity `5 - 2 - 1`
- Expected: `(- (- 5.0 2.0) 1.0)`
- Actual: `(- (- 5.0 2.0) 1.0)`

### Error, unclosed parenthesis `(1 + 2`
- Expected: `[line 1] Error: Expect ')' after expression.`
- Actual: `[line 1] Error: Expect ')' after expression.`
- Cause: parses `1 + 2` inside the group, then needs a `)` but hits the end

### Error, extra parenthesis `1 + 2)`
- Expected: `[line 1] Error: Unexpected token after expression.`
- Actual: `[line 1] Error: Unexpected token after expression.`
- Cause: `1 + 2` is a full expression, so the extra `)` is leftover

### Error, missing right side `1 +`
- Expected: `[line 1] Error: Expect expression.`
- Actual: `[line 1] Error: Expect expression.`
- Cause: after `+` it needs another number or expression, but hits the end

### Error, missing left side `* 5`
- Expected: `[line 1] Error: Expect expression.`
- Actual: `[line 1] Error: Expect expression.`
- Cause: `*` can't start an expression

### Error, extra token `1 2`
- Expected: `[line 1] Error: Unexpected token after expression.`
- Actual: `[line 1] Error: Unexpected token after expression.`
- Cause: `1` is a full expression and nothing joins it to `2`, so `2` is leftover

### Error, empty group `()`
- Expected: `[line 1] Error: Expect expression.`
- Actual: `[line 1] Error: Expect expression.`
- Cause: `(` needs an expression inside but gets `)`

### Error, bad character `1 + @`
- Expected: `[line 1] Error: Unexpected character: @`
- Actual: `[line 1] Error: Unexpected character: @`
- Cause: scanner doesn't know `@`, so the parser never runs and no tree prints

All error tests exit with code 65 and don't print a tree.

### repl_input.txt
- Purpose: REPL keeps working after errors
- Input: `1 + 2 * 3` then `(1 + 2` then `@` then `1 2` then `-(1 + 2) * 3`
- Expected: first and last lines print trees, the 3 in the middle print errors

Actual:
```
> (+ 1.0 (* 2.0 3.0))
> > > > (* (- (group (+ 1.0 2.0))) 3.0)
> 
[line 1] Error: Expect ')' after expression.
[line 1] Error: Unexpected character: @
[line 1] Error: Unexpected token after expression.
```
The extra `>` are the error lines that didn't print a tree. Errors show at the bottom because they go to stderr.

All tests pass.

## Syntax Tree
Expression: `1 + 2 * 3`

Syntax tree following the grammar:
```
expression
└── equality
    └── comparison
        └── term
            ├── factor
            │   └── unary
            │       └── primary
            │           └── NUMBER 1
            ├── "+"
            └── factor
                ├── unary
                │   └── primary
                │       └── NUMBER 2
                ├── "*"
                └── unary
                    └── primary
                        └── NUMBER 3
```

Printed AST:
```
(+ 1.0 (* 2.0 3.0))
```

How they match:
- The syntax tree shows every grammar rule, even the ones that do nothing here
- The AST skips those and only keeps the operators and numbers
- `+` is at the top of both trees, so it happens last
- `*` is lower in both trees, so `2 * 3` happens first
- Each number at the bottom becomes a literal like `1.0`

## Known limitations
- Errors give the line number but not which token caused it
- Errors stop at first syntax errors
- One expression per file or REPL line
- No failing tests