from lark import Token, Tree
from libs.errors.compile_error import CompileError

from .procedure_check import procedure_check
from .type_state import TypeState


def program_check(ast: Tree[Token]) -> None:
    """
    Type-checks a CQ program.

    Args:
        ast (Tree[Token]): The parsed AST.

    Raises:
        CompileError: on any type error or unsupported construct.
    """
    if not isinstance(ast, Tree):
        raise CompileError(f"expected parse tree, got {type(ast)}")

    if str(ast.data) != "program":
        raise CompileError(f"expected start rule 'program', got '{ast.data}'")

    procedures = ast.children

    if len(procedures) != 1:
        raise CompileError(f"Expected exactly 1 procedure, got {len(procedures)}")

    state = TypeState(symbol_table=[{}], type_table=[{}])

    procedure = procedures[0]
    procedure_check(procedure, state)

    return None
