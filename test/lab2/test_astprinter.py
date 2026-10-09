import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from expression import Literal, Grouping, Unary, Binary
from ast_printer import AstPrinter
from pplus_token import Token
from token_type import TokenType

printer = AstPrinter()


# Saved token list
plus = Token(TokenType.PLUS, "+", None, 1)
minus = Token(TokenType.MINUS, "-", None, 1)
star = Token(TokenType.STAR, "*", None, 1)
slash = Token(TokenType.SLASH, "/", None, 1)
percent = Token(TokenType.PERCENT, "%", None, 1)
bang = Token(TokenType.BANG, "!", None, 1)
equal_equal = Token(TokenType.EQUAL_EQUAL, "==", None, 1)
bang_equal = Token(TokenType.BANG_EQUAL, "!=", None, 1)
less = Token(TokenType.LESS, "<", None, 1)
less_equal = Token(TokenType.LESS_EQUAL, "<=", None, 1)
greater = Token(TokenType.GREATER, ">", None, 1)
greater_equal = Token(TokenType.GREATER_EQUAL, ">=", None, 1)


# -123 * (45.67) - example from the lab
# Should print: (* (- 123.0) (group 45.67))
tree = Binary(Unary(minus, Literal(123.0)), star, Grouping(Literal(45.67)))
print(printer.print(tree))

# (1 + 2) % 3
# Should print: (% (group (+ 1.0 2.0)) 3.0)
tree = Binary(Grouping(Binary(Literal(1.0), plus, Literal(2.0))), percent, Literal(3.0))
print(printer.print(tree))

# 10 / 5 - 1
# Should print: (- (/ 10.0 5.0) 1.0)
tree = Binary(Binary(Literal(10.0), slash, Literal(5.0)), minus, Literal(1.0))
print(printer.print(tree))

# (1 + 2) == (4 - 1)
# Should print: (== (group (+ 1.0 2.0)) (group (- 4.0 1.0)))
tree = Binary(Grouping(Binary(Literal(1.0), plus, Literal(2.0))), equal_equal, Grouping(Binary(Literal(4.0), minus, Literal(1.0))))
print(printer.print(tree))

# (4 > 5) != (6 <= 7)
# Should print: (!= (group (> 4.0 5.0)) (group (<= 6.0 7.0)))
tree = Binary(Grouping(Binary(Literal(4.0), greater, Literal(5.0))), bang_equal, Grouping(Binary(Literal(6.0), less_equal, Literal(7.0))))
print(printer.print(tree))

# (5 < 4) != (6 >= 6)
# Should print: (!= (group (< 5.0 4.0)) (group (>= 6.0 6.0)))
tree = Binary(Grouping(Binary(Literal(5.0), less, Literal(4.0))), bang_equal, Grouping(Binary(Literal(6.0), greater_equal, Literal(6.0))))
print(printer.print(tree))

# !true == false
# Should print: (== (! true) false)
tree = Binary(Unary(bang, Literal(True)), equal_equal, Literal(False))
print(printer.print(tree))

# 10 % 2 - 1
# Should print: (- (% 10.0 2.0) 1.0)
tree = Binary(Binary(Literal(10.0), percent, Literal(2.0)), minus, Literal(1.0))
print(printer.print(tree))

# 3.14 * 2 + 1
# Should print: (+ (* 3.14 2.0) 1.0)
tree = Binary(Binary(Literal(3.14), star, Literal(2.0)), plus, Literal(1.0))
print(printer.print(tree))

# "test" != none
# Should print: (!= "test" none)
tree = Binary(Literal("test"), bang_equal, Literal(None))
print(printer.print(tree))

# ----6
# Should print: (- (- (- (- 6.0))))
tree = Unary(minus, Unary(minus, Unary(minus, Unary(minus, Literal(6.0)))))
print(printer.print(tree))

# "none" == none
# Should print: (== "none" none)
tree = Binary(Literal("none"), equal_equal, Literal(None))
print(printer.print(tree))

# ((1))
# Should print: (group (group 1.0))
tree = Grouping(Grouping(Literal(1.0)))
print(printer.print(tree))