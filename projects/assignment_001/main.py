import sys

import interpreter
import libs


def main():
    if len(sys.argv) != 2:
        print("usage: python3 main.py <path>")
        sys.exit(1)

    path = sys.argv[1]
    source = libs.utilities.read_file(path)
    result = interpreter.run(source)

    print("output:", result)


if __name__ == "__main__":
    main()
