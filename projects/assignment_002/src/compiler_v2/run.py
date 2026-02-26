from importlib import resources

from lark import Lark

from . import typecheck


def run(src: str) -> None:
    """
    Parses the given CQ program and type-checks it.

    Args:
        src (str): The source string to parse.
    """
    _lark = Lark.open(
        "grammar_v2.lark",
        import_paths=[str(resources.files("compiler_v1"))],  # get the grammar rules from the v1 compiler
        rel_to=__file__,
        start="program",
    )
    ast = _lark.parse(src)

    typecheck.program_check(ast)

    return None
