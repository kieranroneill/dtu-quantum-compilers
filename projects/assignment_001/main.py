from lark import Lark


def main():
    parser = Lark.open("grammar/expression-ambiguous.lark", start="exp")
    tree1 = parser.parse("1 + 2")

    print(tree1)
    print(tree1.pretty())


if __name__ == "__main__":
    main()
