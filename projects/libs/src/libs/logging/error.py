import logging

import lark

from .log import log


def error(message: str, meta: lark.tree.Meta | None = None) -> None:
    log(message, logging.ERROR, meta)
