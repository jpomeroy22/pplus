import sys
from error_handler import ErrorHandler
from scanner import Scanner

class PPlus:
    def run(self, source):
        ErrorHandler.had_error = False
        for token in Scanner(source).scan_tokens():
            print(token)

    def run_file(self, filename):
        try:
            with open(filename, encoding='utf-8') as file:
                contents = file.read()
        except FileNotFoundError:
            print(f'Error: file not found: {filename}', file=sys.stderr)
            return 66
        self.run(contents)
        return 65 if ErrorHandler.had_error else 0

    def run_prompt(self):
        while True:
            try:
                line = input('> ')
            except (EOFError, KeyboardInterrupt):
                print()
                return 0
            self.run(line)

def main():
    pplus = PPlus()
    if len(sys.argv) == 1:
        return pplus.run_prompt()
    elif len(sys.argv) == 2:
        return pplus.run_file(sys.argv[1])
    else:
        print('Usage: pplus.py [script]', file=sys.stderr)
        return 64

if __name__ == '__main__':
    sys.exit(main())