import logging

import lark

from .log import log


def warn(message: str, meta: lark.tree.Meta | None = None) -> None:
    log(message, logging.WARNING, meta)
