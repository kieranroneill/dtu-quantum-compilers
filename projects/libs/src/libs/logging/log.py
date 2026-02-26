import logging

import lark


def log(message: str, level: int = int, meta: lark.tree.Meta | None = None) -> None:
    _message = f"{message}{meta.line}:{meta.column}" if isinstance(meta, lark.tree.Meta) else message

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
