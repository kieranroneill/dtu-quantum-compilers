from importlib import resources

from lark import Lark
from libs import logging
from libs.errors import CompileError, TypeCheckError
from libs.utilities.exit_code import ExitCode

from .typecheck import TypeChecker


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
        propagate_positions=True,
        rel_to=__file__,
        start="program",
    )
    ast = _lark.parse(src)
    type_checker = TypeChecker()

    try:
        logging.debug(ast)
        type_checker.program_check(ast)
    except Exception as e:
        if isinstance(e, CompileError):
            return ExitCode.COMPILE_ERROR

        if isinstance(e, TypeCheckError):
            return ExitCode.TYPE_CHECK_ERROR

        logging.error(e)
        print(ast.pretty())

        return ExitCode.PARSE_ERROR

    logging.info("✅ successfully compiled program")

    return ExitCode.SUCCESS
