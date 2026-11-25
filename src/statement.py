

class StatementVisitor:
    def visit_expression_statement(self, statement):
        raise NotImplementedError

    def visit_print_statement(self, statement):
        raise NotImplementedError

    def visit_let_statement(self, statement):
        raise NotImplementedError

    def visit_block_statement(self, statement):
        raise NotImplementedError

class Statement:
    def accept(self, visitor):
        raise NotImplementedError

class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_statement(self)

class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_statement(self)

class LetStatement(Statement):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_let_statement(self)

class BlockStatement(Statement):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_statement(self)