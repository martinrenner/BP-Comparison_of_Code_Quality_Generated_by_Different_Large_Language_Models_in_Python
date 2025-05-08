class Calculator:
    """
    A console-based arithmetic calculator that supports basic arithmetic operations,
    including addition, subtraction, multiplication, division, and the use of parentheses.
    It handles both integers and floating-point numbers (including negative values) and
    ensures proper operator precedence.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result.

        Args:
            expression (str): The arithmetic expression as a string.

        Raises:
            ValueError: If the expression is empty, contains invalid characters,
                        or has unbalanced parentheses.
            ZeroDivisionError: If a division by zero is attempted.

        Returns:
            float: The evaluated result.
        """
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("Unbalanced parentheses in the expression.")
        tokens = self._tokenize(normalized_expr)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.

        Args:
            expression (str): The original arithmetic expression as a string.

        Raises:
            ValueError: If the expression is empty or contains invalid characters.

        Returns:
            str: The normalized expression without spaces.
        """
        # Define the characters permitted in the expression.
        allowed_chars = set("0123456789+-*/(). ")
        if not expression:
            raise ValueError("Empty expression.")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        # Remove spaces.
        normalized = expression.replace(" ", "")
        if not normalized:
            raise ValueError("Expression cannot be only whitespace.")
        return normalized

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether the parentheses in the expression are properly balanced.

        Args:
            expression (str): The normalized arithmetic expression.

        Returns:
            bool: True if the parentheses are balanced, False otherwise.
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
        Converts the expression string into a list of tokens (numbers, operators, and parentheses).

        Args:
            expression (str): The normalized arithmetic expression.

        Raises:
            ValueError: If the expression format is invalid.

        Returns:
            list: Tokens list where numbers are represented as floats and operators/parentheses as strings.
        """
        tokens = []
        i = 0
        n = len(expression)
        while i < n:
            char = expression[i]

            # Tokenize a number (integer or float).
            if char.isdigit() or char == '.':
                num_str = ""
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                try:
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: {num_str}")
                continue

            # Handle potential unary operators with '+' or '-'
            if char in "+-":
                # Determine if this is a unary operator by checking the context.
                if (i == 0) or (tokens and isinstance(tokens[-1], str) and tokens[-1] in "+-*/("):
                    # Special handling when the unary operator is immediately followed by a parenthesis.
                    if (i + 1) < n and expression[i + 1] == '(':
                        if char == '-':
                            # Interpret "-(" as (-1 * ( ... ))
                            tokens.append(-1.0)
                            tokens.append('*')
                        # Unary '+' has no effect.
                        i += 1
                        continue
                    else:
                        # Parse the number with the unary sign.
                        sign = -1 if char == '-' else 1
                        i += 1
                        if i < n and (expression[i].isdigit() or expression[i] == '.'):
                            num_str = "-" if sign == -1 else ""
                            while i < n and (expression[i].isdigit() or expression[i] == '.'):
                                num_str += expression[i]
                                i += 1
                            try:
                                tokens.append(float(num_str))
                            except ValueError:
                                raise ValueError(f"Invalid number format: {num_str}")
                            continue
                        else:
                            raise ValueError("Invalid use of unary operator.")
                else:
                    # Otherwise, treat '+' or '-' as binary operators.
                    tokens.append(char)
                    i += 1
                    continue

            # Tokenize multiplication and division operators.
            if char in "*/":
                tokens.append(char)
                i += 1
                continue

            # Tokenize parentheses.
            if char in "()":
                tokens.append(char)
                i += 1
                continue

            # Should not reach here due to earlier validation.
            raise ValueError(f"Invalid character encountered: {char}")
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts an infix token list to a postfix (Reverse Polish Notation) token list using
        the shunting-yard algorithm.

        Args:
            tokens (list): List of tokens in infix order.

        Raises:
            ValueError: If there is a mismatched parentheses in the expression.

        Returns:
            list: Tokens list in postfix order.
        """
        precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
        output = []
        op_stack = []

        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token in precedence:
                while op_stack and op_stack[-1] != '(' and precedence.get(token, 0) <= precedence.get(op_stack[-1], 0):
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
                raise ValueError(f"Unknown token: {token}")

        # Pop any remaining operators from the stack.
        while op_stack:
            token = op_stack.pop()
            if token in "()":
                raise ValueError("Mismatched parentheses.")
            output.append(token)
        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix (Reverse Polish Notation) expression.

        Args:
            tokens (list): List of tokens in postfix notation.

        Raises:
            ValueError: If the postfix expression format is invalid.
            ZeroDivisionError: If division by zero occurs.

        Returns:
            float: The result of the evaluated expression.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in "+-*/":
                if len(stack) < 2:
                    raise ValueError("Invalid expression format.")
                right = stack.pop()
                left = stack.pop()
                if token == '+':
                    stack.append(left + right)
                elif token == '-':
                    stack.append(left - right)
                elif token == '*':
                    stack.append(left * right)
                elif token == '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero.")
                    stack.append(left / right)
            else:
                raise ValueError(f"Unsupported token during evaluation: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression format.")
        return stack[0]


# Example usage:
if __name__ == "__main__":
    calc = Calculator()
    try:
        expression = input("Enter an arithmetic expression: ")
        result = calc.calculate(expression)
        print("Result:", result)
    except Exception as error:
        print("Error:", error)
