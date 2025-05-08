class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions containing
    addition (+), subtraction (-), multiplication (*), division (/), and parentheses.
    It supports integers, decimals, and negative numbers while ensuring the correct
    order of operations.

    Methods:
        calculate(expression: str) -> float:
            Evaluates the arithmetic expression and returns its numerical result.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression provided as a string.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The evaluated result.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, or is otherwise malformed.
            ZeroDivisionError: If division by zero is encountered.
        """
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("The expression has unbalanced parentheses.")

        tokens = self._tokenize(normalized_expr)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the arithmetic expression by removing spaces and validating characters.

        Args:
            expression (str): The input arithmetic expression.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("The expression contains invalid characters.")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if the parentheses in the expression are properly balanced.

        Args:
            expression (str): The input arithmetic expression.

        Returns:
            bool: True if the parentheses are balanced, otherwise False.
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
        Converts the normalized expression string into a list of tokens (numbers and operators).

        Args:
            expression (str): The normalized arithmetic expression.

        Returns:
            list: A list of tokens where numbers are represented as floats and operators as strings.

        Raises:
            ValueError: If an invalid number is encountered.
        """
        tokens = []
        i = 0
        n = len(expression)
        while i < n:
            char = expression[i]
            if char.isdigit() or char == '.':
                # Start accumulating a number token (integer or decimal)
                num_str = char
                i += 1
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                try:
                    number = float(num_str)
                except ValueError:
                    raise ValueError(f"Invalid number: {num_str}")
                tokens.append(number)
            elif char in "+-":
                # Check for unary operator (e.g., -3 or +5)
                if (i == 0) or (expression[i - 1] in "(+*/-"):
                    j = i + 1
                    if j < n and (expression[j].isdigit() or expression[j] == '.'):
                        # Accumulate the number including the unary sign
                        num_str = char
                        i += 1
                        while i < n and (expression[i].isdigit() or expression[i] == '.'):
                            num_str += expression[i]
                            i += 1
                        try:
                            number = float(num_str)
                        except ValueError:
                            raise ValueError(f"Invalid number: {num_str}")
                        tokens.append(number)
                    else:
                        # If not followed by a digit, treat it as a binary operator
                        tokens.append(char)
                        i += 1
                else:
                    tokens.append(char)
                    i += 1
            elif char in "*/()":
                tokens.append(char)
                i += 1
            else:
                raise ValueError(f"Invalid character encountered: {char}")
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts a list of tokens from infix notation to postfix notation using the Shunting Yard algorithm.

        Args:
            tokens (list): List of tokens in infix notation.

        Returns:
            list: List of tokens in postfix (Reverse Polish) notation.

        Raises:
            ValueError: If there are mismatched parentheses in the expression.
        """
        output = []
        op_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token in precedence:
                # Pop operators from the stack with greater or equal precedence
                while (op_stack and op_stack[-1] in precedence and
                       precedence[op_stack[-1]] >= precedence[token]):
                    output.append(op_stack.pop())
                op_stack.append(token)
            elif token == '(':
                op_stack.append(token)
            elif token == ')':
                while op_stack and op_stack[-1] != '(':
                    output.append(op_stack.pop())
                if not op_stack:
                    raise ValueError("Mismatched parentheses in the expression.")
                op_stack.pop()  # Remove the '(' from the stack

        while op_stack:
            if op_stack[-1] in "()":
                raise ValueError("Mismatched parentheses in the expression.")
            output.append(op_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix (Reverse Polish Notation) expression.

        Args:
            tokens (list): List of tokens in postfix notation.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If a division by zero occurs.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid expression.")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero.")
                    result = a / b
                else:
                    raise ValueError(f"Unknown operator: {token}")
                stack.append(result)
        if len(stack) != 1:
            raise ValueError("Invalid expression.")
        return stack[0]


if __name__ == "__main__":
    calc = Calculator()
    print("Welcome to the Arithmetic Calculator!")
    print("Enter 'q' or 'quit' to exit.\n")
    while True:
        user_input = input("Enter expression: ")
        if user_input.strip().lower() in ("q", "quit"):
            print("Exiting the calculator. Goodbye!")
            break
        try:
            result = calc.calculate(user_input)
            print(f"Result: {result}\n")
        except Exception as error:
            print(f"Error: {error}\n")
