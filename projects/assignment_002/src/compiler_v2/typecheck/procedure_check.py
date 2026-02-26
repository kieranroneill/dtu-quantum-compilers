from lark import Token, Tree
from libs import logging
from libs.utilities.exit_code import ExitCode

from .type_state import TypeState


def procedure_check(procedure: Tree[Token], state: TypeState) -> int:
    """
    Type-check a single procedure declaration.

    Args:
        procedure (Tree[Token]):
        state (TypeState): The state of the current compilation. This includes the symbol and type tables.

    Returns:
        int: The exit code indicating the success or failure of the type check.
    """
    if not isinstance(procedure, Tree) or str(procedure.data) != "procedure":
        logging.error(f"expected \"procedure\" node, got {getattr(procedure, 'data', type(procedure))}", procedure.meta)

        return ExitCode.TYPE_ERROR

    # grammar: ID "(" parameter_declarations ")" statement
    children = procedure.children

    if len(children) < 3:
        logging.error(
            f'invalid procedure shape, expected ["ID", "parameter_declarations", "statement"]', procedure.meta
        )

        return ExitCode.TYPE_ERROR

    id_token = children[0]

    if not isinstance(id_token, Token) or id_token.type != "ID":
        logging.error(f'procedure name must be an "ID"', id_token.meta)

        return ExitCode.TYPE_ERROR

    parameter_declarations_node = children[1]

    if (
        not isinstance(parameter_declarations_node, Tree)
        or str(parameter_declarations_node.data) != "parameter_declarations"
    ):
        logging.error('expected "parameter_declarations" node in procedure', parameter_declarations_node.meta)

        return ExitCode.TYPE_ERROR

    statement_node = children[2]

    return ExitCode.SUCCESS
