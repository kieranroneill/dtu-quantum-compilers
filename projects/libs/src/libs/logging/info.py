import logging

import lark

from .log import log


def info(message: str, meta: lark.tree.Meta | None = None) -> None:
    log(message, logging.INFO, meta)
