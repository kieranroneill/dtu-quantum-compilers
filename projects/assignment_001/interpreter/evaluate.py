from errors.compile_error import CompileError
from interpreter.evaluate_binary_operation import evaluate_binary_operation
from interpreter.evaluate_constant import evaluate_constant
from lark.lexer import Token
from lark.tree import Tree


def evaluate(node: Tree | Token) -> int | float:
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
        return evaluate_constant(node)

    if not isinstance(node, Tree):
        raise TypeError(f"unexpected node type: {type(node)}")

    if str(node.data) != "exp":
        raise CompileError(f"unexpected rule: {node.data}")

    children = node.children

    # for single child trees, run recursively
    if len(children) == 1:
        return evaluate(children[0])

    # binary operations should have three children: "exp binop exp"
    if len(children) == 3:
        left, center, right = children

        # when there is a binary operator in the middle
        if isinstance(center, Token) and center.type == "BINOP":
            operator = center.value
            a = evaluate(left)
            b = evaluate(right)

            return evaluate_binary_operation(operator, a, b)

        # handle when there is a parenthesized expression
        if isinstance(left, Token) and left.value == "(" and isinstance(right, Token) and right.value == ")":
            return evaluate(center)

    raise CompileError("unsupported expression shape")
