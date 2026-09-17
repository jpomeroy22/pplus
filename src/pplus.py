import sys

if len(sys.argv) == 1:
    while True:
        try:
            line = input('> ')
            print(line)
            print('Error: Scanner Not Implemented')
        except KeyboardInterrupt:
            break

elif len(sys.argv) == 2:
    filename = sys.argv[1]
    with open(filename) as file:
        contents = file.read()
    print(contents)
    print('Error: Scanner Not Implemented')

else:
    print('Usage: pplus.py [script]')