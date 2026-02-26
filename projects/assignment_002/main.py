import compiler_v2 as compiler
import libs


def main():
    source = libs.utilities.read_file("initialize.cq")
    result = compiler.run(source)

    print("output:", result)


if __name__ == "__main__":
    main()
