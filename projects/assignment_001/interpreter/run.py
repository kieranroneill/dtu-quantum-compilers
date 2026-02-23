from interpreter.evaluate import evaluate
from lark import Lark


def run(src: str) -> int | float:
    """Parses the given source string and evaluates the resulting AST.

    Args:
        src (str): The source string to parse.

    Returns:
        int | float: The result of the parsed expression.
    """
    parser = Lark.open("expression.lark", start="exp")
    ast = parser.parse(src)

    return evaluate(ast)
