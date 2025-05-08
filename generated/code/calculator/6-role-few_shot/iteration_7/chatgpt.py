class Calculator:
    """
    A simple arithmetic calculator that supports addition (+), subtraction (-),
    multiplication (*), division (/), and the use of parentheses in expressions.
    It handles operator precedence correctly and accepts both integers and floating
    point numbers, including negative values.

    Usage:
        calculator = Calculator()
        result = calculator.calculate("3 + (2 * -4.5) / 2")
        print(result)
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the numerical result.

        Args:
            expression (str): The arithmetic expression as a string.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression contains invalid characters,
                        has unbalanced parentheses, or is malformed.
            ZeroDivisionError: If division by zero is encountered.
        """
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("Unbalanced parentheses in expression.")
        tokens = self._tokenize(normalized_expr)
        postfix_tokens = self._infix_to_postfix(tokens)
        return self._evaluate_postfix(postfix_tokens)

    def _normalize_expression(self, expression: str) -> str:
        """
        Removes spaces from the expression and validates allowed characters.

        Args:
            expression (str): The original expression.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().")
        for char in expression:
            if not (char in allowed_chars or char.isspace()):
                raise ValueError("Expression contains invalid characters.")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether the parentheses in the expression are properly balanced.

        Args:
            expression (str): The mathematical expression.

        Returns:
            bool: True if parentheses are correctly paired, otherwise False.
        """
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        return not stack

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the normalized expression into numbers, operators, and parentheses.

        Args:
            expression (str): A normalized arithmetic expression.

        Returns:
            list: A list of tokens in the order they appear in the expression.

        Raises:
            ValueError: If an invalid number format is detected.
        """
        tokens = []
        i = 0
        n = len(expression)
        while i < n:
            char = expression[i]

            # If the character is a digit or a decimal point, it's the start of a number.
            if char.isdigit() or char == '.':
                num_str = char
                i += 1
                dot_count = 1 if char == '.' else 0
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid number with multiple decimal points.")
                    num_str += expression[i]
                    i += 1
                tokens.append(num_str)
                continue

            # Handle potential unary plus or minus.
            if char in '+-':
                # If at the beginning or after an operator or left paren, treat as unary.
                if (i == 0) or (expression[i - 1] in "+-*/("):
                    # Expect a number following the unary operator.
                    if i + 1 < n and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                        num_str = char
                        i += 1
                        # Process the number after the sign.
                        if i < n and (expression[i].isdigit() or expression[i] == '.'):
                            dot_count = 1 if expression[i] == '.' else 0
                            num_str += expression[i]
                            i += 1
                            while i < n and (expression[i].isdigit() or expression[i] == '.'):
                                if expression[i] == '.':
                                    dot_count += 1
                                    if dot_count > 1:
                                        raise ValueError("Invalid number with multiple decimal points.")
                                num_str += expression[i]
                                i += 1
                            tokens.append(num_str)
                            continue
                        else:
                            raise ValueError("Invalid expression format after unary operator.")
                # Otherwise, it's a binary operator.
                tokens.append(char)
                i += 1
                continue

            # Handle multiplication and division operators.
            if char in "*/":
                tokens.append(char)
                i += 1
                continue

            # Handle parentheses.
            if char in "()":
                tokens.append(char)
                i += 1
                continue

            # Should not reach here; all invalid characters are caught in normalization.
            raise ValueError(f"Invalid character encountered: {char}")
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts a list of tokens in infix notation to postfix (Reverse Polish Notation)
        using the shunting-yard algorithm.

        Args:
            tokens (list): List of tokens in infix notation.

        Returns:
            list: List of tokens in postfix order.

        Raises:
            ValueError: If there is a mismatch in parentheses.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        op_stack = []

        for token in tokens:
            if self._is_number(token):
                output.append(token)
            elif token in precedence:
                while op_stack and op_stack[-1] in precedence and precedence[op_stack[-1]] >= precedence[token]:
                    output.append(op_stack.pop())
                op_stack.append(token)
            elif token == '(':
                op_stack.append(token)
            elif token == ')':
                while op_stack and op_stack[-1] != '(':
                    output.append(op_stack.pop())
                if not op_stack:
                    raise ValueError("Mismatched parentheses.")
                op_stack.pop()  # Remove the '(' from the stack.
            else:
                raise ValueError(f"Invalid token encountered in expression: {token}")

        while op_stack:
            if op_stack[-1] in "()":
                raise ValueError("Mismatched parentheses.")
            output.append(op_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix (RPN) expression and returns the result.

        Args:
            tokens (list): List of tokens in postfix notation.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression is invalid.
            ZeroDivisionError: If a division by zero occurs.
        """
        stack = []
        for token in tokens:
            if self._is_number(token):
                try:
                    stack.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid number encountered: {token}")
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid expression structure.")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero.")
                    stack.append(a / b)
                else:
                    raise ValueError(f"Unknown operator: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression evaluation.")
        return stack[0]

    def _is_number(self, token: str) -> bool:
        """
        Checks whether a token represents a valid number.

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


if __name__ == "__main__":
    calculator = Calculator()
    print("Welcome to the console-based Arithmetic Calculator!")
    print("Enter a mathematical expression or type 'quit' to exit.")
    while True:
        try:
            user_input = input(">> ")
            if user_input.strip().lower() in {"quit", "exit"}:
                print("Goodbye!")
                break
            result = calculator.calculate(user_input)
            print("Result:", result)
        except Exception as error:
            print("Error:", error)
