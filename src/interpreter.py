from expression import Visitor
from token_type import TokenType
from error_handler import ErrorHandler
from statement import StatementVisitor
from environment import Environment, UndefinedVariableError

class InterpretError(Exception):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token
        self.message = message

class Interpreter(Visitor, StatementVisitor):
    def __init__(self):
        self.environment = Environment()
        
    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except (InterpretError, UndefinedVariableError) as error:
            ErrorHandler.error(error.token.line, error.message)

    def execute(self, statement):
        statement.accept(self)

    def execute_block(self, statements, environment):
        previous_environment = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous_environment

    def visit_let_statement(self, statement):
        value = None
        if statement.initializer is not None:
            value = self.evaluate(statement.initializer)
        self.environment.define(statement.name.lexeme, value)

    def visit_block_statement(self, statement):
        new_environment = Environment(self.environment)
        self.execute_block(statement.statements, new_environment)

    def visit_variable(self, expression):
        return self.environment.get(expression.name)

    def visit_assign(self, expression):
        value = self.evaluate(expression.value)
        self.environment.assign(expression.name, value)
        return value

    def visit_expression_statement(self, statement):
        self.evaluate(statement.expression)

    def visit_print_statement(self, statement):
        value = self.evaluate(statement.expression)
        if isinstance(value, str):
            print(value)
        else:
            print(self.make_text(value))

    def evaluate(self, expression):
        return expression.accept(self)

    def bool_to_num(self, value):
        if value is True:
            return 1
        if value is False:
            return 0
        return value

    def num_to_bool(self, value):
        if value is True or value is False:
            return value
        return value !=0

    def is_number(self, value):
        return isinstance(value, (int, float))

    def check_numbers(self, operator, *values):
        for value in values:
            if not self.is_number(value):
                raise InterpretError(operator, f"Operand must be a number for '{operator.lexeme}'.")

    def visit_literal(self, expression):
        return expression.value

    def visit_grouping(self, expression):
        return self.evaluate(expression.expression)

    def visit_unary(self, expression):
        right = self.evaluate(expression.right)
        operator = expression.operator
        if operator.type == TokenType.MINUS:
            right = self.bool_to_num(right)
            self.check_numbers(operator, right)
            return -right
        if operator.type == TokenType.BANG:
            if right is None or isinstance(right, str):
                raise InterpretError(operator, "Operand must be a number or boolean for '!'.")
            return not self.num_to_bool(right)

    def visit_binary(self, expression):
        left = self.evaluate(expression.left)
        right = self.evaluate(expression.right)
        operator = expression.operator

        if operator.type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)
        if operator.type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)

        left = self.bool_to_num(left)
        right = self.bool_to_num(right)
        self.check_numbers(operator, left, right)

        if operator.type == TokenType.PLUS:
            return left + right
        if operator.type == TokenType.MINUS:
            return left - right
        if operator.type == TokenType.STAR:
            return left * right
        if operator.type == TokenType.SLASH:
            if right == 0:
                raise InterpretError(operator, "Division by zero.")
            return left / right
        if operator.type == TokenType.PERCENT:
            if right == 0:
                raise InterpretError(operator, "Modulo by zero.")
            return left % right
        if operator.type == TokenType.GREATER:
            return left > right
        if operator.type == TokenType.GREATER_EQUAL:
            return left >= right
        if operator.type == TokenType.LESS:
            return left < right
        if operator.type == TokenType.LESS_EQUAL:
            return left <= right

    def is_equal(self, left, right):
        left_num = self.bool_to_num(left)
        right_num = self.bool_to_num(right)
        if self.is_number(left_num) and self.is_number(right_num):
            return left_num == right_num
        return left == right

    def make_text(self, value):
        if value is None:
            return "none"
        if value is True:
            return "true"
        if value is False:
            return "false"
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        if isinstance(value, str):
            return f'"{value}"'
        return str(value)