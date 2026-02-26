import logging
from pathlib import Path

import compiler_v2 as compiler
import pytest
from libs.utilities.exit_code import ExitCode
from libs.utilities.read_file import read_file


def test_fail_too_many_procedures(caplog):
    caplog.set_level(logging.ERROR)
    source = read_file(Path(__file__).with_name("fail_too_many_procedures.cq"))
    exit_code = compiler.run(src=source)

    assert exit_code == ExitCode.COMPILE_ERROR
    assert 'expected one "procedure"' in caplog.text


def test_success(caplog):
    caplog.set_level(logging.NOTSET)
    source = read_file(Path(__file__).with_name("success.cq"))
    exit_code = compiler.run(source)

    assert exit_code == ExitCode.SUCCESS
