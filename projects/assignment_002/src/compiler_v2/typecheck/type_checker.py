from unittest import case

from lark import Token, Tree
from libs import logging
from libs.errors import CompileError, TypeCheckError

from .symbols import (
    ArrayReferenceSymbol,
    ArraySymbol,
    BaseSymbol,
    CBitSymbol,
    FloatSymbol,
    IntSymbol,
    QBitSymbol,
)


class TypeChecker:
    def __init__(self, symbol_table: list[dict[str, BaseSymbol]] | None = None) -> None:
        self.symbol_table = [{}] if symbol_table is None else symbol_table

    ###
    # private functions
    ###

    def _check_node(self, node: Tree, data: str) -> None:
        if not isinstance(node, Tree) or str(node.data) != data:
            logging.error(f'expected "{data}" node', node)

            raise TypeCheckError()

    def _lookup_symbol_by_name(self, name: str) -> BaseSymbol | None:
        """
        Gets the first symbol with the given name from the symbol table. As the symbol is in the form of a scope stack, it iterates backs through the stack returning the first symbol found with the given name.

        Args:
            name (str): The name of the symbol to lookup.

        Returns:
            BaseSymbol | None: The symbol with the given name, or None if not found.
        """
        for scope in reversed(self.symbol_table):
            if name in scope:
                return scope[name]

        return None

    def _symbol_by_type(self, _type: str) -> BaseSymbol | None:
        match _type:
            case "cbit":
                return CBitSymbol()
            case "float":
                return FloatSymbol()
            case "int":
                return IntSymbol()
            case "qbit":
                return QBitSymbol()
            case _:
                return None

    def _symbol_of(self, item: Token | Tree) -> BaseSymbol | None:
        """
        Gets the symbol for the provided node/token.

        Args:
            item (Token | Tree): The node/token to parse the symbol for.

        Returns:
            (BaseSymbol | None): Returns the symbol for the provided node/token, or None if the symbol cannot be parsed.
        """
        _type = None

        if isinstance(item, Tree):
            # if the node is a variable, return the symbol for the variable
            if item.data == "grammar_v1__variable":
                return self._lookup_symbol_by_name(item.children[0].value)

            _type = str(item.children[0].value)

            # if there is a third child, it is an array declaration, i.e. [TYPE, ID, -> (ID | INT)]
            if len(item.children) > 2:
                array_ref_token = item.children[2]

                if isinstance(array_ref_token, Token):
                    if array_ref_token.type == "INT":
                        return ArraySymbol(_type, int(array_ref_token.value))

                    if array_ref_token.type == "ID":
                        return ArrayReferenceSymbol(_type, str(array_ref_token.value))

                    logging.warn('array reference must be an "ID" or "INT" token', item)

                    return None

                logging.warn(f'unsupported type "{_type}"', item)

                return None

        if isinstance(item, Token):
            _type = str(item.type)

        if _type is not None:
            match _type:
                case "FLOAT":
                    return FloatSymbol()
                case "INT":
                    return IntSymbol()
                case "NAMED_CONSTANT":  # i.e. "pi"
                    return FloatSymbol()
                case _:
                    logging.warn(f'unsupported type "{_type}"', item)

                    return None

        logging.warn(f"unable to parse symbol", item)

        return None

    ###
    # public functions
    ###

    def block_check(self, node: Tree) -> None:
        self._check_node(node, "block")

        if len(node.children) != 2:
            logging.error(f"unexpected block shape", node)

            raise TypeCheckError()

        # add a new scope
        self.symbol_table.append({})

        self.declarations_check(node.children[0])
        self.statements_check(node.children[1])

        # remove the scope
        self.symbol_table.pop()

        return None

    def declaration_check(self, node: Tree) -> None:
        """
        Type-checks the "declaration" node.

        Lark grammar: TYPE lval ";"
            | TYPE ID "=" exp ";"
            | TYPE ID "[" INT "]" "=" "{" exps "}" ";"

        Args:
            node (Tree): The "declaration" node to type-check.

        Raises:
            TypeCheckError: If the "declaration" node fails the type check.
        """
        self._check_node(node, "declaration")

        # grammar: TYPE lval ";"
        if len(node.children) >= 2 and isinstance(node.children[0], Token) and node.children[0].type == "TYPE":

            lval_node = node.children[1]

            self.lval_check(lval_node)

            name = str(lval_node.children[0].value)

            if name in self.symbol_table[-1]:
                logging.error(f'duplicate declaration name "{name}" in the same scope', lval_node)

                raise TypeCheckError()

            type_token = node.children[0]
            symbol = self._symbol_by_type(type_token)

            if symbol is None:
                logging.error(f'unsupported parameter type "{str(type_token.value)}"', type_token)

                raise TypeCheckError()

            self.symbol_table[-1][name] = symbol

            return None

        # TODO: implement other grammar forms for declaration here

        logging.error("invalid declaration form", node)

        raise TypeCheckError()

    def declarations_check(self, node: Tree) -> None:
        self._check_node(node, "declarations")

        for node in node.children:
            self.declaration_check(node)

        return None

    def exp_binary_check(self, node: Tree) -> None:
        """
        Type-checks an "exp_binary" node.

        Note: The grammar rules are stated in grammar_v1.lark, which is a subset of the grammar_v2.lark.

        Lark grammar: exp OP exp

        Args:
            node (Tree): The "exp_binary" node to type-check.

        Raises:
            TypeCheckError: If the "exp_binary" node fails the type check.
        """
        if not isinstance(node, Tree):
            logging.error("unexpected grammar form", node)

            raise TypeCheckError()

        operator_token = node.children[1]

        if not isinstance(operator_token, Token) or operator_token.type not in {"PE", "MD", "AS", "CMP"}:
            logging.error("expected binary operator token in expression", operator_token)

            raise TypeCheckError()

        left_value_token = node.children[0]
        right_value_token = node.children[2]

        # check the left and right expressions
        self.exp_check(left_value_token)
        self.exp_check(right_value_token)

        operator_type = str(operator_token.type)
        operator_value = str(operator_token.value)
        left_value_symbol = self._symbol_of(left_value_token)
        right_value_symbol = self._symbol_of(right_value_token)

        # PM: base ** exponent
        if operator_type == "PE" and operator_value == "**":
            if operator_value == "**":
                if left_value_symbol.symbol() != "int" and left_value_symbol.symbol() != "float":
                    logging.error("exponentiation base must be numeric", node)

                    raise TypeCheckError()

                if right_value_symbol.symbol() != "int" and right_value_symbol.symbol() != "float":
                    logging.error("exponent must be numeric", node)

                    raise TypeCheckError()

            return None

        # MD: * / % &
        if operator_type == "MD":
            if operator_value in {"*", "/"}:
                if left_value_symbol.symbol() != "int" and left_value_symbol.symbol() != "float":
                    logging.error("left operand of * / must be numeric", node)

                    raise TypeCheckError()

                if right_value_symbol.symbol() != "int" and right_value_symbol.symbol() != "float":
                    logging.error("right operand of * / must be numeric", node)

                    raise TypeCheckError()

            if operator_value == "%":
                if left_value_symbol.symbol() != "int" and right_value_symbol.symbol() != "int":
                    logging.error("modulo requires integer operands", node)

                    raise TypeCheckError()

            if operator_value == "&":
                if left_value_symbol.symbol() != "int" and right_value_symbol.symbol() != "int":
                    logging.error("bitwise and requires integer operands", node)
                    raise TypeCheckError()

            return None

        # AS: + - | xor ^
        if operator_type == "AS":
            if operator_value in {"+", "-", "|", "^"}:
                if left_value_symbol.symbol() != "int" and left_value_symbol.symbol() != "float":
                    logging.error(f'"AS" operator "{operator_value}" requires numeric type', node)

                    raise TypeCheckError()

                if right_value_symbol.symbol() != "int" and right_value_symbol.symbol() != "float":
                    logging.error(f'"AS" operator "{operator_value}" requires numeric type', node)

                    raise TypeCheckError()

                return None

            if operator_value == "xor":
                if left_value_symbol.symbol() != "int" and right_value_symbol.symbol() != "int":
                    logging.error("xor requires integer operands", node)

                    raise TypeCheckError()

        # CMP: == <
        if operator_type == "CMP":
            if left_value_symbol.symbol() != "int" and left_value_symbol.symbol() != "float":
                logging.error("comparison left operand must be numeric type", node)

                raise TypeCheckError()

            if right_value_symbol.symbol() != "int" and right_value_symbol.symbol() != "float":
                logging.error("comparison right operand must be numeric type", node)

                raise TypeCheckError()

            return None

        logging.error(f'unsupported binary operator "{operator_value}" with type "{operator_type}"', node)

        raise TypeCheckError()

    def exp_check(self, item: Token | Tree) -> None:
        """
        Type-checks an "exp" node.

        Lark grammar:

        Args:
            item (Token | Tree): The "exp" node to type-check.

        Raises:
            TypeCheckError: If the "exp" node fails the type check.
        """
        # grammar form: INT | FLOAT | NAMED_CONSTANT
        if isinstance(item, Token):
            if item.type in {"INT", "FLOAT", "NAMED_CONSTANT"}:
                return None

            logging.error(f'unexpected token "{item.type}"', item)

            raise TypeCheckError()

        # grammar form: variable
        if str(item.data) == "grammar_v1__variable":
            return self.variable_check(item)

        children = item.children

        match len(children):
            # grammar form: "(" exp ")"
            case 1:
                return self.exp_check(children[0])
            # grammar form: UNOP exp
            case 2:
                return self.exp_unary_check(item)
            # grammar form: exp BINOP exp
            case 3:
                return self.exp_binary_check(item)

        logging.error("invalid expression form", item)

        raise TypeCheckError()

    def exp_unary_check(self, node: Tree) -> None:
        """
        Type-checks an "exp_unary" node.

        Note: The grammar rules are stated in grammar_v1.lark, which is a subset of the grammar_v2.lark.

        Lark grammar: UNOP exp_unary

        Args:
            node (Tree): The "exp_unary" node to type-check.

        Raises:
            TypeCheckError: If the "exp_unary" node fails the type check.
        """
        if not isinstance(node, Tree):
            logging.error("unexpected grammar form", node)

            raise TypeCheckError()

        operator_token = node.children[0]
        operator = str(operator_token.value)

        if (
            not isinstance(operator_token, Token)
            or operator_token.type != "UNOP"
            or operator not in {"!", "not", "~", "-"}
        ):
            logging.error(f'unexpected unary operator "{operator}"', operator_token)

            raise TypeCheckError()

        operand_token = node.children[1]
        operand_symbol = self._symbol_of(operand_token)

        if operand_symbol is None:
            logging.error(f'unsupported operand type "{str(operand_token.value)}"', operand_token)

            raise TypeCheckError()

        # bitwise negation must be "int"
        if operator == "~":
            if operand_symbol.symbol() != "int":
                logging.error("bitwise negation requires integer operand", operand_token)

                raise TypeCheckError()

        # unary minus must be numeric (float or int)
        if operator == "-":
            if operand_symbol.symbol() != "int" or operand_symbol.symbol() != "float":
                logging.error("unary minus requires numeric operand", operand_token)

                raise TypeCheckError()

        return self.exp_check(operand_token)

    def lval_check(self, node: Tree) -> None:
        self._check_node(node, "lval")

    def parameter_declaration_check(self, node: Tree) -> None:
        """
        Type-check the parameter of a procedure.

        Lark grammar: TYPE ID | TYPE ID "[" (ID | INT) "]"

        Args:
            node (Tree): The parameter node to type-check.

        Raises:
            TypeCheckError: If the "parameter_declaration" and its corresponding elements failed the type check.
        """
        self._check_node(node, "parameter_declaration")

        children = node.children

        if len(children) > 3:
            logging.error(f'unexpected "parameter_declaration" shape', node)

            raise TypeCheckError()

        type_token = children[0]

        if not isinstance(type_token, Token) or type_token.type != "TYPE":
            logging.error('parameter type must be a "TYPE" token', type_token)

            raise TypeCheckError()

        name_token = children[1]

        if not isinstance(name_token, Token) or name_token.type != "ID":
            logging.error('parameter name must be an "ID" token', name_token)

            raise TypeCheckError()

        _type = str(type_token.value)
        name = str(name_token.value)

        if name in self.symbol_table[-1]:
            logging.error(f'duplicate parameter name "{name}" in the same scope', name_token)

            raise TypeCheckError()

        # if there is a third child, it is an array declaration, i.e. [TYPE, ID, -> (ID | INT)]
        if len(children) > 2:
            array_ref_token = children[2]

            if isinstance(array_ref_token, Token):
                if array_ref_token.type == "INT":
                    self.symbol_table[-1][name] = ArraySymbol(_type, int(array_ref_token.value))

                    return None

                if array_ref_token.type == "ID":
                    self.symbol_table[-1][name] = ArrayReferenceSymbol(_type, str(array_ref_token.value))

                    return None

            logging.error(f'unsupported array type "{_type}"', array_ref_token)

            raise TypeCheckError()

        symbol = self._symbol_by_type(_type)

        if symbol is None:
            logging.error(f'unsupported parameter type "{_type}"', type_token)

            raise TypeCheckError()

        self.symbol_table[-1][name] = symbol

        return None

    def parameter_declarations_check(self, node: Tree) -> None:
        self._check_node(node, "parameter_declarations")

        for parameter in node.children:
            self.parameter_declaration_check(parameter)

        return None

    def procedure_check(self, node: Tree) -> None:
        """
        Type-check a single procedure.

        Lark grammar: ID "(" parameter_declarations ")" statement

        Args:
            node (Tree): The procedure node to type-check.

        Raises:
            TypeCheckError: If the "procedure" fails the type check.
        """
        self._check_node(node, "procedure")

        children = node.children

        if len(children) < 3:
            logging.error(f'invalid procedure shape, expected ["ID", "parameter_declarations", "statement"]', node)

            raise TypeCheckError()

        # <---------- "ID" check ---------->

        id_token = node.children[0]

        if not isinstance(id_token, Token) or id_token.type != "ID":
            logging.error(f'procedure name must be an "ID"', id_token)

            raise TypeCheckError()

        # <---------- "parameter_declarations" check ---------->

        self.parameter_declarations_check(children[1])

        # <---------- "statement" check ---------->

        return self.statement_check(children[2])

    def program_check(self, node: Tree) -> None:
        """
        Type-checks a CQ program.

        Args:
            node (Tree): The parsed AST.

        Raises:
            CompileError: If the AST is not a Tree or if there are multiple procedures.
            TypeCheckError: If the "program" and its corresponding elements failed the type check.
        """
        self._check_node(node, "program")

        procedures = node.children

        if len(procedures) <= 0:
            logging.error(f"expected at least one procedure")

            raise CompileError()

        for procedure in procedures:
            self.procedure_check(procedure)

        return None

    def statement_check(self, node: Tree) -> None:
        """
        Type-checks a "statement" node.

        Lark grammar: lval EQ exp ";"
            | qupdate ";"
            | qupdate IF lval ";"
            | procedure_call ";"
            | MEASURE lval "->" lval ";"
            | IF "(" exp ")" statement "else" statement
            | WHILE "(" exp ")" statement
            | block

        Args:
            node (Tree): The "statement" node to type-check.

        Raises:
            TypeCheckError: If the "statement" and its corresponding elements failed the type check.
        """
        self._check_node(node, "statement")

        match len(node.children):
            # grammar form: block
            case 1:
                return self.block_check(node.children[0])
            # grammar form: lval EQ exp ";"
            case 3:
                lval_node = node.children[0]

                self.lval_check(lval_node)

                lval_name = lval_node.children[0].value
                lval_symbol = self._lookup_symbol_by_name(lval_name)

                if lval_symbol is None:
                    logging.error(f'undefined variable "{lval_name}"', lval_node)

                    raise TypeCheckError()

                if lval_symbol.symbol() == "qbit":
                    logging.error('"qbit" type is not allowed to be assignment target', lval_node)

                    raise TypeCheckError()

                exp_node = node.children[2]

                self.exp_check(exp_node)

                return None

        # TODO: implement other grammar forms for "statement" here

        logging.error("invalid statement form", node)

        raise TypeCheckError()

    def statements_check(self, node: Tree) -> None:
        self._check_node(node, "statements")

        for node in node.children:
            self.statement_check(node)

        return None

    def variable_check(self, node: Tree) -> None:
        """
        Type-checks a "variable" node.

        Note: The grammar rules are stated in grammar_v1.lark, which is a subset of the grammar_v2.lark.

        Lark grammar: ID
            | ID "[" exp "]"

        Args:
            node (Tree): The "statement" node to type-check.

        Raises:
            TypeCheckError: If the "variable" node fails the type check.
        """
        self._check_node(node, "grammar_v1__variable")

        children = node.children

        # grammar form: ID
        if len(children) == 1 and isinstance(children[0], Token) and children[0].type == "ID":
            name = str(children[0].value)
            symbol = self._lookup_symbol_by_name(name)

            # if the symbol exists so we are successful
            if symbol is not None:
                return None

            logging.error(f'undefined variable "{name}"', node)

            raise TypeCheckError()

        # grammar form: ID "[" exp "]"
        if (
            len(children) == 2
            and isinstance(children[0], Token)
            and children[0].type == "ID"
            and isinstance(children[1], Tree)
        ):
            name = str(children[0].value)

            # check the symbol exists
            symbol = self._lookup_symbol_by_name(name)

            if symbol is None:
                logging.error(f'undefined variable "{name}"', node)

                raise TypeCheckError()

            return self.exp_check(children[1])

        logging.error("invalid variable form", node)

        raise TypeCheckError()
