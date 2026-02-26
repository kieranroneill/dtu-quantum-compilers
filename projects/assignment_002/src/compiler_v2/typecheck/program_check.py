import logging

from lark import Token, Tree
from libs.utilities.exit_code import ExitCode

from .procedure_check import procedure_check
from .type_state import TypeState


def program_check(ast: Tree[Token]) -> int:
    """
    Type-checks a CQ program.

    Args:
        ast (Tree[Token]): The parsed AST.

    Returns:
        int: The exit code indicating the success or failure of the type check.
    """
    if not isinstance(ast, Tree):
        logging.error(f'expected parse "Tree", but got "{type(ast)}"')

        return ExitCode.COMPILE_ERROR

    if str(ast.data) != "program":
        logging.error(f'expected start rule "program", got "{ast.data}"')

        return ExitCode.TYPE_ERROR

    procedures = ast.children

    if len(procedures) > 1:
        logging.error(f'expected one "procedure", got "{len(procedures)}" procedures')

        return ExitCode.COMPILE_ERROR

    state = TypeState(symbol_table=[{}], type_table=[{}])

    procedure = procedures[0]

    return procedure_check(procedure, state)
