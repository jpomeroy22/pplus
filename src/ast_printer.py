from expression import Visitor


class AstPrinter(Visitor):
    def print(self, expression):
        return expression.accept(self)

    def visit_literal(self, expression):
        if expression.value is None:
            return "none"
        if expression.value is True:
            return "true"
        if expression.value is False:
            return "false"
        if isinstance(expression.value, str):
            return f'"{expression.value}"'
        return str(expression.value)

    def visit_grouping(self, expression):
        return self.parenthesize("group", expression.expression)

    def visit_unary(self, expression):
        return self.parenthesize(expression.operator.lexeme, expression.right)

    def visit_binary(self, expression):
        return self.parenthesize(expression.operator.lexeme, expression.left, expression.right)

    def parenthesize(self, name, *expressions):
        pieces = []
        pieces.append(name)
        for e in expressions:
            printer = e.accept(self)
            pieces.append(printer)
        return "(" + " ".join(pieces) + ")"