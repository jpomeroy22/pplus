

class UndefinedVariableError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message

class Environment:
    def __init__(self, outer=None):
        self.outer = outer
        self.variables = {}

    def define(self, name, value):
        self.variables[name] = value

    def get(self, token):
        name = token.lexeme
        if name in self.variables:
            return self.variables[name]
        if self.outer is not None:
            return self.outer.get(token)
        raise UndefinedVariableError(token, f"Undefined variable '{name}'.")

    def assign(self, token, value):
        name = token.lexeme
        if name in self.variables:
            self.variables[name] = value
            return
        if self.outer is not None:
            self.outer.assign(token, value)
            return
        raise UndefinedVariableError(token, f"Undefined variable '{name}'.")