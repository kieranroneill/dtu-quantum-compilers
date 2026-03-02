from enum import Enum


class ExitCode(Enum):
    SUCCESS = 0
    COMPILE_ERROR = 1
    PARSE_ERROR = 2
    TYPE_CHECK_ERROR = 3
