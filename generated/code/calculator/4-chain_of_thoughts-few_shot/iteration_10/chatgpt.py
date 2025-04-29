class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses. It correctly handles the order
    of operations and supports integers, decimals, and negative numbers.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result as a float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid, contains unbalanced parentheses,
                        or has invalid characters.
            ZeroDivisionError: If division by zero is attempted.
        """
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("Unbalanced parentheses in expression.")

        tokens = self._tokenize(normalized_expr)
        postfix = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression by removing spaces and validating allowed characters.

        Args:
            expression (str): The arithmetic expression to normalize.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/(). ")
        for char in expression:
            if char not in allowed_chars:
                raise ValueError(f"Expression contains invalid character: {char}")

        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether a mathematical expression has properly paired parentheses.

        Args:
            expression (str): The arithmetic expression as a string.

        Returns:
            bool: True if parentheses are correctly paired, otherwise False.
        """
        stack = []
        for char in expression:
            if char == "(":
                stack.append(char)
            elif char == ")":
                if not stack:
                    return False
                stack.pop()
        return not stack

    def _tokenize(self, expression: str) -> list:
        """
        Converts the normalized expression string into a list of tokens (numbers, operators, and parentheses).
        Handles unary plus/minus for negative numbers.

        Args:
            expression (str): The normalized arithmetic expression.

        Returns:
            list: A list of tokens.

        Raises:
            ValueError: If invalid characters or number formats are encountered.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isdigit() or char == ".":
                # Token is a number.
                number_token, i = self._read_number(expression, i)
                tokens.append(number_token)
            elif char in "+-":
                # Determine if the operator is unary (part of a number) or binary.
                if (i == 0) or (expression[i - 1] in "(+-*/"):
                    # Unary plus or minus: read it as part of a number.
                    number_token, i = self._read_number(expression, i)
                    tokens.append(number_token)
                else:
                    # Binary operator.
                    tokens.append(char)
                    i += 1
            elif char in "*/":
                tokens.append(char)
                i += 1
            elif char in "()":
                tokens.append(char)
                i += 1
            else:
                raise ValueError(f"Invalid character encountered: {char}")
        return tokens

    def _read_number(self, expression: str, i: int) -> (str, int):
        """
        Reads a number (which may include a unary sign and a decimal point) 
        starting from the given index in the expression.

        Args:
            expression (str): The arithmetic expression.
            i (int): The current index in the expression.

        Returns:
            tuple: A tuple containing the number token (str) and the updated index (int).

        Raises:
            ValueError: If the number format is invalid.
        """
        num_str = ""
        # Process a unary sign if present.
        if expression[i] in "+-":
            num_str += expression[i]
            i += 1

        digit_found = False
        dot_found = False
        # Read the digit and dot characters.
        while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
            if expression[i] == ".":
                if dot_found:  # Second dot encountered; break out to let float() catch the error.
                    break
                dot_found = True
                num_str += expression[i]
            else:
                digit_found = True
                num_str += expression[i]
            i += 1

        if not digit_found:
            raise ValueError(f"Invalid number format near: {num_str}")

        # Validate number conversion.
        try:
            float(num_str)
        except ValueError:
            raise ValueError(f"Invalid number format: {num_str}")

        return num_str, i

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts a list of infix tokens to postfix notation using the Shunting Yard algorithm.

        Args:
            tokens (list): The list of tokens from the arithmetic expression.

        Returns:
            list: The postfix (Reverse Polish Notation) list of tokens.

        Raises:
            ValueError: If there are mismatched parentheses.
        """
        output = []
        op_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if self._is_number(token):
                output.append(token)
            elif token in precedence:
                while op_stack and op_stack[-1] in precedence and precedence[op_stack[-1]] >= precedence[token]:
                    output.append(op_stack.pop())
                op_stack.append(token)
            elif token == "(":
                op_stack.append(token)
            elif token == ")":
                found_parenthesis = False
                while op_stack:
                    top = op_stack.pop()
                    if top == "(":
                        found_parenthesis = True
                        break
                    output.append(top)
                if not found_parenthesis:
                    raise ValueError("Mismatched parentheses.")
            else:
                raise ValueError(f"Invalid token encountered in parsing: {token}")

        while op_stack:
            top = op_stack.pop()
            if top in "()":
                raise ValueError("Mismatched parentheses.")
            output.append(top)

        return output

    def _is_number(self, token: str) -> bool:
        """
        Checks whether the token represents a valid number.

        Args:
            token (str): The token to check.

        Returns:
            bool: True if the token is a number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix (Reverse Polish Notation) expression.

        Args:
            tokens (list): The postfix list of tokens.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression is invalid.
            ZeroDivisionError: If division by zero occurs.
        """
        stack = []
        for token in tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in ("+", "-", "*", "/"):
                if len(stack) < 2:
                    raise ValueError("Insufficient operands in the expression.")
                right = stack.pop()
                left = stack.pop()
                if token == "+":
                    stack.append(left + right)
                elif token == "-":
                    stack.append(left - right)
                elif token == "*":
                    stack.append(left * right)
                elif token == "/":
                    if right == 0:
                        raise ZeroDivisionError("Division by zero encountered.")
                    stack.append(left / right)
            else:
                raise ValueError(f"Invalid token encountered during evaluation: {token}")

        if len(stack) != 1:
            raise ValueError("The expression is invalid.")

        return stack[0]


if __name__ == '__main__':
    calc = Calculator()
    print("Console-based Arithmetic Calculator")
    print("Supports operations: +, -, *, / and parentheses ().")
    print("Enter 'quit' to exit.\n")

    while True:
        try:
            expr = input("Enter an arithmetic expression: ").strip()
            if expr.lower() in {"quit", "exit"}:
                break
            result = calc.calculate(expr)
            print("Result:", result, "\n")
        except Exception as error:
            print("Error:", error, "\n")
