from importlib import resources

from interpreter_v1.evaluate import evaluate
from lark import Lark


def run(src: str) -> int | float:
    """Parses the given source string and evaluates the resulting AST.

    Args:
        src (str): The source string to parse.

    Returns:
        int | float: The result of the parsed expression.
    """
    parser = Lark.open(
        "cq.lark",
        import_paths=[str(resources.files("interpreter_v1"))],  # get the grammar rules from the v1 interpreter
        rel_to=__file__,
        start="exp",
    )
    ast = parser.parse(src)

    result = evaluate(ast)

    print(result)

    return 0
