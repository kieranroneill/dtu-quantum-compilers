import logging
from pathlib import Path

import compiler_v2 as compiler
import pytest
from libs.utilities.exit_code import ExitCode
from libs.utilities.read_file import read_file


def test_success_procedure_complex_statement(caplog):
    caplog.set_level(logging.NOTSET)
    source = read_file(Path(__file__).with_name("success_procedure_complex_statement.cq"))
    exit_code = compiler.run(source)

    assert exit_code == ExitCode.SUCCESS


def test_success_procedure_simple_statement(caplog):
    caplog.set_level(logging.NOTSET)
    source = read_file(Path(__file__).with_name("success_procedure_simple_statement.cq"))
    exit_code = compiler.run(source)

    assert exit_code == ExitCode.SUCCESS
