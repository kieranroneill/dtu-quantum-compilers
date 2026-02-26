from enum import Enum


class ExitCode(Enum):
    SUCCESS = 0
    COMPILE_ERROR = 1
    TYPE_ERROR = 2
