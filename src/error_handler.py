import sys

class ErrorHandler:
    had_error = False

    @staticmethod
    def error(line, message):
        print(f'[line {line}] Error: {message}', file=sys.stderr)
        ErrorHandler.had_error = True