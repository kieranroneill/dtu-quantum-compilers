import logging
from pathlib import Path

import compiler_v2 as compiler
import pytest
from libs.utilities.exit_code import ExitCode
from libs.utilities.read_file import read_file


def test_fail_duplicate_procedure_parameters(caplog):
    caplog.set_level(logging.ERROR)
    source = read_file(Path(__file__).with_name("fail_duplicate_procedure_parameters.cq"))
    exit_code = compiler.run(src=source)

    assert exit_code == ExitCode.TYPE_CHECK_ERROR
    assert "duplicate parameter name" in caplog.text


def test_success_multiple_procedure_parameter_types(caplog):
    caplog.set_level(logging.NOTSET)
    source = read_file(Path(__file__).with_name("success_multiple_procedure_parameter_types.cq"))
    exit_code = compiler.run(source)

    assert exit_code == ExitCode.SUCCESS


def test_success_procedure_parameters_array_fixed_size(caplog):
    caplog.set_level(logging.NOTSET)
    source = read_file(Path(__file__).with_name("success_procedure_parameters_array_fixed_size.cq"))
    exit_code = compiler.run(source)

    assert exit_code == ExitCode.SUCCESS


def test_success_procedure_parameters_array_reference(caplog):
    caplog.set_level(logging.NOTSET)
    source = read_file(Path(__file__).with_name("success_procedure_parameters_array_reference.cq"))
    exit_code = compiler.run(source)

    assert exit_code == ExitCode.SUCCESS
