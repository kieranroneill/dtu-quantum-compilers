from lark import Lark

from .evaluate import evaluate


def run(src: str) -> int | float:
    """Parses the given source string and evaluates the resulting AST.

    Args:
        src (str): The source string to parse.

    Returns:
        int | float: The result of the parsed expression.
    """
    _lark = Lark.open("grammar_v1.lark", rel_to=__file__, start="exp")
    ast = _lark.parse(src)

    return evaluate(ast)
