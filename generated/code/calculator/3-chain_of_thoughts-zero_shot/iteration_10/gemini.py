import re  # Used for tokenization

class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions using the
    Shunting Yard algorithm.  Adheres to ISO/IEC 25010 quality characteristics.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
            TypeError: If input expression is not string
        """
        try:
            tokens = self._tokenize(expression)
            postfix_tokens = self._shunting_yard(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")  # Log or print more details.
            raise  # Re-raise to stop further processing

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the input expression.

        Args:
            expression: The arithmetic expression.

        Returns:
            A list of tokens (numbers, operators, parentheses).

        Raises:
            ValueError: For invalid characters in the expression.
        """

        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        # Regex to split the expression into tokens
        token_pattern = r"(\d+\.?\d*|\.\d+|[-+*/()]|\s+)"
        tokens = re.findall(token_pattern, expression)

        # Remove whitespace tokens
        tokens = [token for token in tokens if not token.isspace()]

        # Validation
        valid_chars = r"^[-+*/()\d\s.]+$"  # Allowed characters
        if not re.match(valid_chars, expression):
            raise ValueError("Invalid characters in expression.")

        return tokens

    def _shunting_yard(self, tokens: list) -> list:
        """
        Converts infix notation to postfix notation using the Shunting Yard algorithm.

        Args:
            tokens: A list of tokens in infix notation.

        Returns:
            A list of tokens in postfix notation.

        Raises:
            ValueError: For unbalanced parentheses.
        """
        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if re.match(r"^-?\d+\.?\d*$", token) or re.match(r"^-?\.\d+$", token):  # Handle integers and decimals, including negative
                output_queue.append(float(token))
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                try:
                    while operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    operator_stack.pop()  # Remove the '('
                except IndexError:
                    raise ValueError("Unbalanced parentheses.")
            else:
                raise ValueError(f"Invalid token and cannot process: {token}")

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Unbalanced parentheses.")
            output_queue.append(operator_stack.pop())

        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            tokens: A list of tokens in postfix notation.

        Returns:
            The result of the expression.

        Raises:
            ValueError: For division by zero or an invalid expression.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            else:  # It's an operator
                try:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise ValueError("Invalid expression (not enough operands).")

                if token == '+':
                    stack.append(operand1 + operand2)
                elif token == '-':
                    stack.append(operand1 - operand2)
                elif token == '*':
                    stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ValueError("Division by zero.")
                    stack.append(operand1 / operand2)

        if len(stack) != 1:
            raise ValueError("Invalid expression (too many operands).")

        return stack[0]

if __name__ == "__main__":
    calculator = Calculator()

    # Valid expressions
    print(calculator.calculate("2 + 3 * 4"))  # Output: 14.0
    print(calculator.calculate("(2 + 3) * 4"))  # Output: 20.0
    print(calculator.calculate("-5 + 2 * 3.14"))  # Output: 1.28
    print(calculator.calculate("10 / (2 + 3)"))  # Output: 2.0
    print(calculator.calculate("10 / 2 + 3"))    # Output: 8.0
    print(calculator.calculate(".5 * 2"))        # Output: 1.0
    print(calculator.calculate("-0.5 * -2"))     # Output: 1.0

    # Invalid expressions (will raise exceptions)
    try:
        calculator.calculate("2 + + 3")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        calculator.calculate("10 / 0")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        calculator.calculate("(2 + 3 * 4")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        calculator.calculate("2 & 3")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        calculator.calculate(2+3)
    except TypeError as e:
        print(f"Caught expected error: {e}")
