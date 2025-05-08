class Calculator:
    """
    A console-based arithmetic calculator that supports addition (+), subtraction (-),
    multiplication (*), division (/), and parentheses. It accepts integer and decimal numbers,
    including negatives, and evaluates expressions while ensuring proper input validation.

    This implementation uses the Shunting-yard algorithm for converting infix expressions to
    postfix notation and then evaluates the postfix expression. It is designed with modularity,
    safety, and ease-of-testing in mind.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given mathematical expression and returns the result as a float.

        Args:
            expression (str): A string containing the mathematical expression.

        Returns:
            float: The result of evaluating the expression.

        Raises:
            ValueError: If the expression contains invalid characters, has unbalanced parentheses,
                        or its syntax is incorrect.
            ZeroDivisionError: If a division by zero occurs during evaluation.
        """
        # Normalize the expression (remove whitespace and validate allowed characters)
        norm_expr = self._normalize_expression(expression)
        # Check for balanced parentheses
        if not self._is_balanced(norm_expr):
            raise ValueError("The expression has unbalanced parentheses.")
        # Tokenize the normalized expression into numbers and operators
        tokens = self._tokenize(norm_expr)
        # Convert the tokenized infix expression to postfix notation
        postfix = self._infix_to_postfix(tokens)
        # Evaluate the postfix expression and return the result
        result = self._evaluate_postfix(postfix)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the input expression by removing spaces and validating allowed characters.

        Args:
            expression (str): The math expression as a string.

        Returns:
            str: A normalized expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789.+-*/() ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether the expression has balanced parentheses.

        Args:
            expression (str): The mathematical expression as a string.

        Returns:
            bool: True if parentheses are correctly paired; False otherwise.
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
        Converts the normalized expression string into a list of tokens consisting of numbers,
        operators, and parentheses. It handles negative numbers by supporting a unary '-' symbol.

        Args:
            expression (str): A normalized mathematical expression (no spaces).

        Returns:
            list: A list of tokens (strings).

        Raises:
            ValueError: If an invalid number format is encountered.
        """
        tokens = []
        i = 0
        n = len(expression)
        while i < n:
            char = expression[i]

            # If the character is a digit or a decimal point, parse the full number.
            if char.isdigit() or char == '.':
                num_chars = []
                dot_count = 0
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid number format: multiple decimal points.")
                    num_chars.append(expression[i])
                    i += 1
                tokens.append(''.join(num_chars))
            # Handle potential unary plus or minus
            elif char in "+-":
                # Determine if this sign is unary.
                if i == 0 or expression[i - 1] in "(+-*/":
                    # Check if sign is immediately followed by a digit or a dot.
                    if i + 1 < n and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                        sign = char
                        i += 1
                        num_chars = [sign]
                        dot_count = 0
                        while i < n and (expression[i].isdigit() or expression[i] == '.'):
                            if expression[i] == '.':
                                dot_count += 1
                                if dot_count > 1:
                                    raise ValueError(
                                        "Invalid number format: multiple decimal points."
                                    )
                            num_chars.append(expression[i])
                            i += 1
                        tokens.append(''.join(num_chars))
                        continue
                    # If there's no number following, treat it as a binary operator.
                    else:
                        tokens.append(char)
                        i += 1
                else:
                    tokens.append(char)
                    i += 1
            # Handle operators: multiplication, division and parentheses.
            elif char in "*/()":
                tokens.append(char)
                i += 1
            else:
                # Should never happen due to normalization, but added as a safeguard.
                raise ValueError(f"Invalid character encountered: {char}")
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts an infix token list to postfix (Reverse Polish Notation) using the Shunting-yard
        algorithm.

        Args:
            tokens (list): A list of tokens in infix order.

        Returns:
            list: A list of tokens in postfix order.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        operator_stack = []

        for token in tokens:
            if self._is_number(token):
                output_queue.append(token)
            elif token in precedence:
                while operator_stack and operator_stack[-1] in precedence and \
                        precedence[operator_stack[-1]] >= precedence[token]:
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop()  # Remove the '('
        # Pop any remaining operators
        while operator_stack:
            top = operator_stack.pop()
            if top in "()":
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(top)
        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix (Reverse Polish Notation) expression and returns its result.

        Args:
            tokens (list): A list of tokens in postfix order.

        Returns:
            float: The result of evaluating the expression.

        Raises:
            ZeroDivisionError: If division by zero takes place.
            ValueError: If the expression is syntactically incorrect.
        """
        stack = []
        for token in tokens:
            if self._is_number(token):
                stack.append(float(token))
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid expression.")
                b = stack.pop()  # Second operand
                a = stack.pop()  # First operand
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
            raise ValueError("Invalid expression.")
        return stack[0]

    def _is_number(self, token: str) -> bool:
        """
        Determines if the given token represents a valid number.

        Args:
            token (str): The token to check.

        Returns:
            bool: True if the token can be converted to a float, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    calc = Calculator()
    print("Simple Arithmetic Calculator (type 'quit' or 'exit' to leave)")
    while True:
        try:
            expression = input("Enter expression: ")
            if expression.lower() in {"quit", "exit"}:
                print("Exiting calculator.")
                break
            result = calc.calculate(expression)
            print("Result:", result)
        except Exception as error:
            print("Error:", error)
