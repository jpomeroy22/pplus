# Lab 1: Scanning - pplus (pythonplus)

## Language
Name: pplus, files use .pp

## Regular Expression
- Numbers: `[0-9]+(\.[0-9]+)?` -- Digits, optional decimal part, stored as float
- String: `"[^"]*"` -- Anything between double quotes, can do multiple lines, no escapes
- Identifier: `[A-Za-z_][A-Za-z0-9_]*` -- Letters or underscores first, case sensitive

## Changes from Lox
- fun into def, nil into none, var into let
- Added % modulo
- Comments use # instead of //
- Only ASCII letters/digits, anything else is unexpected character

Everything else should work like Lox

## Errors
- Format: `[line N] Error: message`
- Unexpected characters
- Unterminated string

## How to Run
- Python3, no extra packages. Run from repo root.
- REPL: `python src/pplus.py`
- File: `python src/pplus.py test/lab1/comments.pp`
- Tests: `python test/lab1/run_tests.py` -- output saved to test/lab1/output

## Tests

### single_char.pp
- Purpose: All single char tokens
- Input: `() {} , . - + ; * / %`
- Expected: One token each
- All tests pass

### operators.pp
- Purpose: 1/2 char operators
- Input: `! != = == < <= > >=`
- Expected: != == <= >= are all single token
- All tests pass

### keywords.pp
- Purpose: All keywords
- Input: `and class def while`
- Expected: Each is its keyword token
- All tests pass

### identifiers.pp
- Purpose: Identifier rules
- Input: `x _x my_var var2 fun nil var Def LET`
- Expected: All identifier, old Lox keywords and wrong case arn't keywords
- All tests pass

### numbers.pp
- Purpose: Ints, decimals, edge cases
- Input: `0 12 3.14 5.0 5. .5`
- Expected: All floats, 5. is number dot, .5 is dot number
- All tests pass

### strings.pp
- Purpose: Normal, empty, and multi-line strings
- Input: `"testing" "" "# comment test"` and a string across 2 lines
- Expected: Each is a string token, # stays in the string
- All tests pass

### comments.pp
- Purpose: # comments
- Input: full line and end of line comments
- Expected: No tokens from comments
- All tests pass

### error_unterminated.pp
- Purpose: Unterminated string
- Input: `s = "never closed;`
- Expected: Error on line 1, exit code 65
- All tests pass

### error_unexpected.pp
- Purpose: Unexpected characters
- Input: @ $ & on lines 1-3
- Expected: Error for each with the right line, rest still scans
- All tests pass

### mixed.pp
- Purpose: Errors mixed with normal code
- Input: errors on lines 2 and 4
- Expected: Both errors show, normal lines still scan
- All tests pass

### repl_input.txt
- Purpose: REPL keeps working after errors
- Input: `x = 1;` then `"missing quote` then `@` then `print "does this work";`
- Expected: Both errors show, last line still works
- All tests pass

Actual output for every test is saved in test/lab1/output

Full output from one run:

```
=== comments.pp ===
IDENTIFIER x None
EQUAL = None
NUMBER 10 10.0
EOF  None
[exit code 0]

=== error_unexpected.pp ===
IDENTIFIER a None
EQUAL = None
NUMBER 1 1.0
NUMBER 2 2.0
SEMICOLON ; None
IDENTIFIER b None
EQUAL = None
SEMICOLON ; None
IDENTIFIER c None
EQUAL = None
NUMBER 3 3.0
NUMBER 4 4.0
SEMICOLON ; None
EOF  None
[line 1] Error: Unexpected character: @
[line 2] Error: Unexpected character: $
[line 3] Error: Unexpected character: &
[exit code 65]

=== error_unterminated.pp ===
IDENTIFIER s None
EQUAL = None
EOF  None
[line 1] Error: Unterminated string.
[exit code 65]

=== identifiers.pp ===
IDENTIFIER x None
IDENTIFIER _x None
IDENTIFIER my_var None
IDENTIFIER var2 None
IDENTIFIER fun None
IDENTIFIER nil None
IDENTIFIER var None
IDENTIFIER Def None
IDENTIFIER LET None
EOF  None
[exit code 0]

=== keywords.pp ===
AND and None
CLASS class None
DEF def None
ELSE else None
FALSE false None
FOR for None
IF if None
LET let None
NONE none None
OR or None
PRINT print None
RETURN return None
SUPER super None
THIS this None
TRUE true None
WHILE while None
EOF  None
[exit code 0]

=== mixed.pp ===
IDENTIFIER ok None
EQUAL = None
NUMBER 1 1.0
SEMICOLON ; None
IDENTIFIER bad None
EQUAL = None
SEMICOLON ; None
PRINT print None
STRING "fine" fine
SEMICOLON ; None
IDENTIFIER s None
EQUAL = None
EOF  None
[line 2] Error: Unexpected character: @
[line 4] Error: Unterminated string.
[exit code 65]

=== numbers.pp ===
NUMBER 0 0.0
NUMBER 12 12.0
NUMBER 3.14 3.14
NUMBER 123 123.0
NUMBER 1234567 1234567.0
NUMBER 5.0 5.0
NUMBER 5 5.0
DOT . None
DOT . None
NUMBER 5 5.0
NUMBER 0.5 0.5
EOF  None
[exit code 0]

=== operators.pp ===
BANG ! None
BANG_EQUAL != None
EQUAL = None
EQUAL_EQUAL == None
LESS < None
LESS_EQUAL <= None
GREATER > None
GREATER_EQUAL >= None
EOF  None
[exit code 0]

=== single_char.pp ===
LEFT_PAREN ( None
RIGHT_PAREN ) None
LEFT_BRACE { None
RIGHT_BRACE } None
COMMA , None
DOT . None
MINUS - None
PLUS + None
SEMICOLON ; None
STAR * None
SLASH / None
PERCENT % None
EOF  None
[exit code 0]

=== strings.pp ===
STRING "testing" testing
STRING "" 
STRING "# comment test" # comment test
STRING "test with
multiple lines" test with
multiple lines
EOF  None
[exit code 0]

=== repl ===
> IDENTIFIER x None
EQUAL = None
NUMBER 1 1.0
SEMICOLON ; None
EOF  None
> EOF  None
> EOF  None
> PRINT print None
STRING "does this work" does this work
SEMICOLON ; None
EOF  None
> 
[line 1] Error: Unterminated string.
[line 1] Error: Unexpected character: @
```

## Known limitations
- 5. and .5 arn't single numbers
- All numbers are floats
- No escape sequences in strings
- Multi line strings report the line they end on
- No failing tests