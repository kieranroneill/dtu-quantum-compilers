import interpreter_v2 as interpreter
import libs


def main():
    source = libs.utilities.read_file("initialize.cq")
    result = interpreter.run(source)

    print("output:", result)


if __name__ == "__main__":
    main()
