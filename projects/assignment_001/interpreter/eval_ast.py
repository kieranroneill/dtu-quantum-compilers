from errors.compile_error import CompileError
from lark.lexer import Token
from lark.tree import Tree


def eval_ast(node: Tree | Token) -> int | float:
    """
    Recursively evaluates the AST and interprets the code.

    Parameters
    ----------
    node : lark.tree.Tree | lark.lexer.Token
        The AST which is recursively evaluated until it reaches a leaf node (token).

    Returns
    -------
    result : int | float
        The evaluated value of the expression.
    """

    # if we have a token, we evaluate it and return the result
    if isinstance(node, Token):
        if node.type == "INT":
            return int(node.value, 0)
        if node.type == "FLOAT":
            return float(node.value)
        raise CompileError(f"unknown token: {node.type}")

    # if we have a tree structure, we need to further evaluate
    if isinstance(node, Tree):
        if str(node.data) != "exp":
            raise CompileError(f"expected rule: {node.data}")

        # exp: INT | FLOAT | NAMED_CONSTANT
        if len(node.children) == 1:
            return eval_ast(node.children[0])

        # exp: exp BINOP exp
        if len(node.children) == 3:
            left, op, right = node.children
            if not isinstance(op, Token) or op.type != "BINOP":
                raise CompileError("Expected BINOP in the middle of a binary expression")

            a = eval_ast(left)
            b = eval_ast(right)

            if op.value == "+":
                return a + b

            raise CompileError(f"unsupported operator: {op.value}")

        raise CompileError("unsupported expression shape")

    raise TypeError(f"unexpected node type: {type(node)}")
