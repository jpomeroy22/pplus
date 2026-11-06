

class StatementVisitor:
    def visit_expression_statement(self, statement):
        raise NotImplementedError

    def visit_print_statement(self, statement):
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