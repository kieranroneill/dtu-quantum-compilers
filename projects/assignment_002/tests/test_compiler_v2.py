from pathlib import Path

import compiler_v2 as compiler
import libs


def test_success():
    source = libs.utilities.read_file(Path(__file__).with_name("success.cq"))

    compiler.run(source)


if __name__ == "__main__":
    test_success()

    print("✅ passed")
