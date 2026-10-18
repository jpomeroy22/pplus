from token_type import TokenType
from expression import *
from error_handler import ErrorHandler

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def at_end(self):
        return self.peek().type == TokenType.EOF

    def step(self):
        if not self.at_end():
            self.current += 1
        return self.previous()

    def check(self, type):
        if self.at_end():
            return False
        return self.peek().type == type

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.step()
                return True
        return False

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NONE):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def factor(self):
        expression = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR, TokenType.PERCENT):
            operator = self.previous()
            right = self.unary()
            expression = Binary(expression, operator, right)
        return expression

    def term(self):
        expression = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.factor()
            expression = Binary(expression, operator, right)
        return expression

    def comparison(self):
        expression = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expression = Binary(expression, operator, right)
        return expression

    def equality(self):
        expression = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expression = Binary(expression, operator, right)
        return expression

    def expression(self):
        return self.equality()

    def consume(self, type, message):
        if self.check(type):
            return self.step()
        raise self.error(self.peek(), message)

    def error(self, token, message):
        ErrorHandler.error(token.line, message)
        return ParseError()

    def parse(self):
        try:
            expression = self.expression()
            if not self.at_end():
                raise self.error(self.peek(), "Unexpected token after expression.")
            return expression
        except ParseError:
            return None