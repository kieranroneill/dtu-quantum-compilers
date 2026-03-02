from lark import Tree
from libs import logging
from libs.errors import TypeCheckError


def lval_check(lval_node: Tree) -> None:
    if not isinstance(lval_node, Tree) or str(lval_node.data) != "lval":
        logging.error("expected lval", lval_node)

        raise TypeCheckError()
