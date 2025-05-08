class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses while respecting operator precedence.
    It accepts both integers and floating-point numbers including negative values.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result.

        Args:
            expression (str): The arithmetic expression as a string.

        Returns:
            float: The calculated result.

        Raises:
            ValueError: If the expression contains invalid characters or unbalanced/mismatched parentheses.
            ZeroDivisionError: When a division by zero is attempted.
        """
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("Unbalanced parentheses in expression.")
        tokens = self._tokenize(normalized_expr)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the arithmetic expression by removing spaces and
        validating that all characters are allowed.

        Allowed characters: digits, '+', '-', '*', '/', '.', '(', ')', and spaces.

        Args:
            expression (str): The original expression string.

        Returns:
            str: The expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if the parentheses in the expression are properly balanced.

        Args:
            expression (str): The normalized expression.

        Returns:
            bool: True if parentheses are balanced, else False.
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
        Breaks the normalized expression into tokens (numbers, operators, parentheses).

        This method handles negative numbers as well by checking if a '-' sign is
        used as a unary operator (e.g., at the start of the expression or after an opening
        parenthesis or another operator) and merging it with the subsequent number.

        Args:
            expression (str): The normalized mathematical expression.

        Returns:
            list: The list of tokens.

        Raises:
            ValueError: If an invalid token or malformed number is encountered.
        """
        tokens = []
        i = 0
        n = len(expression)
        while i < n:
            char = expression[i]

            # Detect a unary minus indicating a negative number.
            if char == '-' and (i == 0 or expression[i - 1] in "(+-*/"):
                num_str = char
                i += 1
                if i < n and (expression[i].isdigit() or expression[i] == '.'):
                    dot_count = 0
                    while i < n and (expression[i].isdigit() or expression[i] == '.'):
                        if expression[i] == '.':
                            dot_count += 1
                            if dot_count > 1:
                                raise ValueError("Invalid number format: multiple decimal points in a number.")
                        num_str += expression[i]
                        i += 1
                    tokens.append(num_str)
                else:
                    raise ValueError("Invalid usage of '-' for negative number: expected digit after '-'")
            elif char.isdigit() or char == '.':
                num_str = ""
                dot_count = 0
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid number format: multiple decimal points in a number.")
                    num_str += expression[i]
                    i += 1
                tokens.append(num_str)
            elif char in "+*/":
                tokens.append(char)
                i += 1
            elif char == '-':
                # This '-' is treated as the subtraction operator (binary operator).
                tokens.append(char)
                i += 1
            elif char in "()":
                tokens.append(char)
                i += 1
            else:
                raise ValueError(f"Invalid character in expression: {char}")
        return tokens

    def _to_rpn(self, tokens: list) -> list:
        """
        Converts a list of tokens in infix notation to Reverse Polish Notation (RPN)
        using the Shunting Yard algorithm.

        Args:
            tokens (list): The list of tokens in infix order.

        Returns:
            list: The tokens in RPN order.

        Raises:
            ValueError: If there are mismatched parentheses.
        """
        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            # If token is a number, push it to the output queue.
            try:
                float(token)
                output_queue.append(token)
            except ValueError:
                if token in precedence:
                    # For operators, pop from the stack to the output queue while the top
                    # of the stack has an operator of greater or equal precedence.
                    while operator_stack and operator_stack[-1] in precedence and \
                          precedence[operator_stack[-1]] >= precedence[token]:
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(token)
                elif token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    # Pop operators until an opening parenthesis is encountered.
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    if not operator_stack:
                        raise ValueError("Mismatched parentheses")
                    operator_stack.pop()  # Remove the '(' from stack.
                else:
                    raise ValueError(f"Unknown token: {token}")

        # Append any remaining operators.
        while operator_stack:
            top = operator_stack.pop()
            if top in "()":
                raise ValueError("Mismatched parentheses")
            output_queue.append(top)

        return output_queue

    def _evaluate_rpn(self, tokens: list) -> float:
        """
        Evaluates an expression written in Reverse Polish Notation (RPN).

        Args:
            tokens (list): The RPN tokens.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ZeroDivisionError: If a division by zero occurs.
            ValueError: If the expression format is invalid.
        """
        stack = []
        for token in tokens:
            try:
                # If token is a number, push it onto the stack.
                number = float(token)
                stack.append(number)
            except ValueError:
                # The token is assumed to be an operator.
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands.")
                right = stack.pop()
                left = stack.pop()
                if token == '+':
                    result = left + right
                elif token == '-':
                    result = left - right
                elif token == '*':
                    result = left * right
                elif token == '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    result = left / right
                else:
                    raise ValueError(f"Unsupported operator: {token}")
                stack.append(result)
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands.")
        return stack[0]


# Example usage:
if __name__ == "__main__":
    calc = Calculator()
    expressions = [
        "3 + 4 * 2 / (1 - 5)",      # Basic arithmetic with precedence and parentheses.
        "-3.5 + 2.5 * 4",           # Negative number and float arithmetic.
        "(2 + 3) * (7 - 2) / 5",    # Multiple parentheses.
        "10 / (5 - 5)"              # Division by zero example.
    ]

    for expr in expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"Error evaluating '{expr}': {e}")
