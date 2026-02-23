from lark import Lark

from .evaluate import evaluate


def run(src: str) -> int | float:
    """Parses the given source string and evaluates the resulting AST.

    Args:
        src (str): The source string to parse.

    Returns:
        int | float: The result of the parsed expression.
    """
    parser = Lark.open("expression.lark", rel_to=__file__, start="exp")
    ast = parser.parse(src)

    return evaluate(ast)
