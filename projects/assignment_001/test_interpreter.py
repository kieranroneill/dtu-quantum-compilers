import interpreter


def test_simple_expressions():
    assert interpreter.run("2 + 2") == 4, "should be 4"
    assert interpreter.run("2+2") == 4, "should be 4"
    assert interpreter.run("2 - 2") == 0, "should be 0"
    assert interpreter.run("5 * 3") == 15, "should be 15"
    assert interpreter.run("3 / 2") == 1, "should be 1"
    assert interpreter.run("3.0 / 2.0") == 1.5, "should be 1"
    assert interpreter.run("(3 + 3)") == 6, "should be 6"
    assert interpreter.run("(5) + (5)") == 10, "should be 10"


def test_complex_expressions():
    assert interpreter.run("(1 + 2) * 3") == 9, "should be 9"
    assert interpreter.run("((1 + 1) * 2) * 3") == 12, "should be 12"
    assert interpreter.run("((8 * 2.0) / 4) - 9") == -5.0, "should be -0.5"


if __name__ == "__main__":
    test_simple_expressions()

    print("✅ passed")
