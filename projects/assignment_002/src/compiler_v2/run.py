from importlib import resources

from lark import Lark
from libs import logging
from libs.errors import CompileError, TypeCheckError
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
    symbol_table = [{}]

    try:
        symbol_table = typecheck.program_check(ast, symbol_table)
    except Exception as e:
        if isinstance(e, CompileError):
            return ExitCode.COMPILE_ERROR

        if isinstance(e, TypeCheckError):
            return ExitCode.TYPE_CHECK_ERROR

        logging.error(e)

        return ExitCode.PARSE_ERROR

    logging.info("✅ successfully compiled program")

    return ExitCode.SUCCESS
