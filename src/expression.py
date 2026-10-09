

class Visitor:
    def visit_literal(self, expression):
        raise NotImplementedError

    def visit_grouping(self, expression):
        raise NotImplementedError

    def visit_unary(self, expression):
        raise NotImplementedError

    def visit_binary(self, expression):
        raise NotImplementedError


class Expression:
    def accept(self, visitor):
        raise NotImplementedError


class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)


class Grouping(Expression):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping(self)


class Unary(Expression):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary(self)


class Binary(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary(self)