from interpreter.eval_ast import eval_ast
from lark import Lark
from libs.read_file import read_file


def compile_file(parser: Lark, file: str):
    src = read_file(file)
    ast = parser.parse(src)
    result = eval_ast(ast)

    print("output:", result)


def main():
    parser = Lark.open("grammar/expression-ambiguous.lark", start="exp")

    # example 1.3
    compile_file(parser, "examples/1-3.cq")


if __name__ == "__main__":
    main()
