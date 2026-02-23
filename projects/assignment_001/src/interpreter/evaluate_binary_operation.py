from libs.errors.compile_error import CompileError


def evaluate_binary_operation(operator: str, a, b):
    operations = {
        "+": lambda _a, _b: _a + _b,
        "-": lambda _a, _b: _a - _b,
        "*": lambda _a, _b: _a * _b,
        "/": lambda _a, _b: _a // _b if type(_a) == int and type(_b) == int else _a / _b,
        "%": lambda _a, _b: _a % _b,
        "&": lambda _a, _b: _a & _b,
        "|": lambda _a, _b: _a | _b,
        "^": lambda _a, _b: _a ^ _b,
        "<": lambda _a, _b: _a < _b,
        "==": lambda _a, _b: _a == _b,
        "xor": lambda _a, _b: _a ^ _b,
        "**": lambda _a, _b: _a**_b,
    }

    try:
        return operations[operator](a, b)
    except KeyError:
        raise CompileError(f"unsupported operator: {operator}")
