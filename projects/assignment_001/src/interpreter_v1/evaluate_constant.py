from lark.lexer import Token
from libs.errors.compile_error import CompileError


def evaluate_constant(token: Token) -> int | float:
    match token.type:
        case "FLOAT":
            return float(token.value)
        case "INT":
            return int(token.value, 0)
        case _:
            raise CompileError(f"unknown token: {token.type}")
