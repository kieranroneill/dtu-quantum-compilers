import logging

from lark import Token, Tree
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
        logging.error(f"expected \"procedure\" node, got {getattr(procedure, 'data', type(procedure))}")

        return ExitCode.TYPE_ERROR

    # Expected shape (based on your grammar_v2): ID "(" parameter_declarations ")" statement
    # After parsing, punctuation usually doesn't show up in the tree, so children are commonly:
    #   [ID, parameter_declarations, statement]
    children = procedure.children
    if len(children) < 3:
        logging.error(f"unexpected procedure shape (children={len(children)}), expected at least 3")

        return ExitCode.TYPE_ERROR

    name_token = children[0]
    params_node = children[1]
    body_stmt = children[2]

    if not isinstance(name_token, Token) or name_token.type != "ID":
        logging.error("procedure name must be an ID token")

        return ExitCode.TYPE_ERROR

    if not isinstance(params_node, Tree) or str(params_node.data) != "parameter_declarations":
        logging.error('expected "parameter_declarations" node in procedure')

        return ExitCode.TYPE_ERROR

    # Hook: later you will iterate params_node.children and populate state.env/state.tenv
    # Hook: later you will typecheck body_stmt
    # For now, just succeed if it parses.
    return ExitCode.SUCCESS
