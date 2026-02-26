from lark import Token, Tree
from libs.errors.compile_error import CompileError

from .type_state import TypeState


def procedure_check(proc: Tree[Token], state: TypeState) -> None:
    """
    Type-check a single procedure declaration.

    For now we only validate the shape and set up the hook for later work.
    """
    if not isinstance(proc, Tree) or str(proc.data) != "procedure":
        raise CompileError(f"Expected 'procedure' node, got {getattr(proc, 'data', type(proc))}")

    # Expected shape (based on your grammar_v2): ID "(" parameter_declarations ")" statement
    # After parsing, punctuation usually doesn't show up in the tree, so children are commonly:
    #   [ID, parameter_declarations, statement]
    children = proc.children
    if len(children) < 3:
        raise CompileError(f"Unexpected procedure shape (children={len(children)}). Expected at least 3.")

    name_token = children[0]
    params_node = children[1]
    body_stmt = children[2]

    if not isinstance(name_token, Token) or name_token.type != "ID":
        raise CompileError("Procedure name must be an ID token")

    if not isinstance(params_node, Tree) or str(params_node.data) != "parameter_declarations":
        raise CompileError("Expected 'parameter_declarations' node in procedure")

    # Hook: later you will iterate params_node.children and populate state.env/state.tenv
    # Hook: later you will typecheck body_stmt
    # For now, just succeed if it parses.
    return None
