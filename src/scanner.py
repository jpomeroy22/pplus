from error_handler import ErrorHandler
from pplus_token import Token
from token_type import TokenType

class Scanner:
    keywords = {
        'and': TokenType.AND,
        'class': TokenType.CLASS,
        'def': TokenType.DEF,
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'for': TokenType.FOR,
        'if': TokenType.IF,
        'let': TokenType.LET,
        'none': TokenType.NONE,
        'or': TokenType.OR,
        'print': TokenType.PRINT,
        'return': TokenType.RETURN,
        'super': TokenType.SUPER,
        'this': TokenType.THIS,
        'true': TokenType.TRUE,
        'while': TokenType.WHILE,
    }
        
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        """Return a list of Token objects, ending with one EOF token.

        Report lexical errors through ErrorHandler.error(line, message).
        Scanning begins at line 1. Ignore whitespace and # comments.
        """
        while not self.at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()

        # Single character tokens
        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '*':
            self.add_token(TokenType.STAR)
        elif c == '/':
            self.add_token(TokenType.SLASH)
        elif c == '%':
            self.add_token(TokenType.PERCENT)

        # One/two character tokens
        elif c == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)

        # For comments, runs until the end of the line
        elif c == "#":
            while self.peek() != "\n" and not self.at_end():
                self.advance()

        # Whitespace
        elif c in [' ', '\r', '\t']:
            pass
        elif c == '\n':
            self.line += 1

        # Literals
        elif c == '"':
            self.string()
        elif self.is_digit(c):
            self.number()
        elif self.is_alpha(c) or c == '_':
            self.identifier()

        else:
            ErrorHandler.error(self.line, f"Unexpected character: {c}")

    def string(self):
        while self.peek() != '"' and not self.at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.at_end():
            ErrorHandler.error(self.line, "Unterminated string.")
            return

        # Closing "
        self.advance()
        value = self.source[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # Fractions
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def identifier(self):
        while self.is_alnum(self.peek()):
            self.advance()
        text = self.source[self.start:self.current]
        self.add_token(self.keywords.get(text, TokenType.IDENTIFIER))

    def at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def peek(self):
        if self.at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def match(self, expected):
        if self.at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def add_token(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    @staticmethod
    def is_digit(c):
        return '0' <= c <= '9'

    @staticmethod
    def is_alpha(c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'

    def is_alnum(self, c):
        return self.is_alpha(c) or self.is_digit(c)