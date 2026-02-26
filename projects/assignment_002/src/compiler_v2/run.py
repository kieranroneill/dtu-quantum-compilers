from importlib import resources

from lark import Lark
from libs import logging
from libs.utilities.exit_code import ExitCode

from . import typecheck


def run(src: str) -> int:
    """
    Parses the given CQ program and type-checks it.

    Args:
        src (str): The source string to parse.

    Returns:
        int: The exit code indicating the success or failure of the compilation process.
    """
    _lark = Lark.open(
        "grammar_v2.lark",
        import_paths=[str(resources.files("compiler_v1"))],  # get the grammar rules from the v1 compiler
        rel_to=__file__,
        start="program",
    )
    ast = _lark.parse(src)

    exit_code = typecheck.program_check(ast)

    if exit_code == ExitCode.SUCCESS:
        logging.info("✅ successfully compiled program")

    return exit_code
