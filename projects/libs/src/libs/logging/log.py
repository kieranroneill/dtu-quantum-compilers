import logging

import lark


def log(message: str, level: int = int, leaf: lark.Tree | lark.Token | None = None) -> None:
    _message = message

    if isinstance(leaf, lark.Token):
        _message = f"{message}:{leaf.end_line}:{leaf.end_column}"

    if isinstance(leaf, lark.Tree):
        _message = f"{message}{leaf.meta.line}:{leaf.meta.column}"

    match level:
        case logging.CRITICAL:
            logging.critical(_message)
        case logging.DEBUG:
            logging.debug(_message)
        case logging.ERROR:
            logging.error(_message)
        case logging.FATAL:
            logging.fatal(_message)
        case logging.INFO:
            logging.info(_message)
        case logging.WARNING:
            logging.warning(_message)
