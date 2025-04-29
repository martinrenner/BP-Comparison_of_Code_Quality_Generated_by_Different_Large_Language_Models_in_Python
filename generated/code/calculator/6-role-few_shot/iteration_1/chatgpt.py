class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses with proper operator precedence.
    It accepts both integers and floating-point numbers, including negative values.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result as a float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The evaluated result.

        Raises:
            ValueError: If the expression contains invalid characters or unbalanced parentheses.
            ZeroDivisionError: If a division by zero occurs.
        """
        # Normalize expression: remove whitespace and validate allowed characters.
        normalized = self._normalize_expression(expression)
        # Check that parentheses are balanced.
        self._check_balanced(normalized)
        # Tokenize the normalized expression.
        tokens = self._tokenize(normalized)
        # Convert infix tokens to postfix (Reverse Polish Notation) using Shunting Yard algorithm.
        postfix_tokens = self._infix_to_postfix(tokens)
        # Evaluate the postfix expression.
        return self._evaluate_postfix(postfix_tokens)

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression by removing whitespace and validating characters.

        Args:
            expression (str): The raw mathematical expression.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().")
        # Remove whitespace.
        normalized = expression.replace(" ", "")
        if not all(char in allowed_chars for char in normalized):
            raise ValueError("Expression contains invalid characters.")
        return normalized

    def _check_balanced(self, expression: str) -> None:
        """
        Checks whether the expression has properly paired parentheses.

        Args:
            expression (str): The normalized mathematical expression.

        Raises:
            ValueError: If the parentheses in the expression are unbalanced.
        """
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise ValueError("Unbalanced parentheses detected.")
                stack.pop()
        if stack:
            raise ValueError("Unbalanced parentheses detected.")

    def _tokenize(self, expression: str) -> list:
        """
        Converts the normalized expression into a list of tokens.
        Tokens include numbers (as strings) and operators: +, -, *, /, (, ).

        This tokenizer also handles negative numbers by checking the context
        in which a '-' appears.

        Args:
            expression (str): The normalized mathematical expression.

        Returns:
            list: A list of tokens (strings).

        Raises:
            ValueError: If an invalid numerical format is encountered.
        """
        tokens = []
        i = 0
        n = len(expression)

        while i < n:
            char = expression[i]

            # Handle numbers (integer or floating-point)
            if char.isdigit() or char == '.':
                num_str = ""
                dot_count = 0
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid numeric format: multiple decimal points.")
                    num_str += expression[i]
                    i += 1
                tokens.append(num_str)
                continue

            # Handle an operator or parenthesis.
            elif char in "+-*/()":
                # Check for unary minus (negative numbers)
                if char == '-' and (
                    (len(tokens) == 0) or (tokens[-1] in "+-*/(")
                ):
                    # Lookahead to see if there is a number after the unary minus.
                    j = i + 1
                    if j < n and (expression[j].isdigit() or expression[j] == '.'):
                        num_str = "-"
                        dot_count = 0
                        i += 1  # Skip the '-' sign.
                        while i < n and (expression[i].isdigit() or expression[i] == '.'):
                            if expression[i] == '.':
                                dot_count += 1
                                if dot_count > 1:
                                    raise ValueError("Invalid numeric format: multiple decimal points.")
                            num_str += expression[i]
                            i += 1
                        tokens.append(num_str)
                        continue
                    else:
                        # Treat as a binary minus if not followed by a numeric value.
                        tokens.append(char)
                        i += 1
                        continue
                else:
                    tokens.append(char)
                    i += 1
                    continue
            else:
                raise ValueError(f"Invalid character encountered: {char}")

        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts a list of tokens in infix notation to postfix notation using
        the Shunting Yard algorithm.

        Args:
            tokens (list): List of tokens in infix order.

        Returns:
            list: List of tokens in postfix (Reverse Polish) order.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        operator_stack = []

        for token in tokens:
            # If token is a number, push it to the output queue.
            if self._is_number(token):
                output_queue.append(token)
            # If token is an operator.
            elif token in precedence:
                while operator_stack:
                    top = operator_stack[-1]
                    if top == '(':
                        break
                    if precedence.get(top, 0) >= precedence[token]:
                        output_queue.append(operator_stack.pop())
                    else:
                        break
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                # Pop operators until '(' is encountered.
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Unbalanced parentheses encountered during conversion.")
                operator_stack.pop()  # Remove the '(' from the stack.
            else:
                raise ValueError(f"Unknown token encountered: {token}")

        # Pop any remaining operators from the stack.
        while operator_stack:
            top = operator_stack.pop()
            if top in "()":
                raise ValueError("Unbalanced parentheses encountered in final stack cleanup.")
            output_queue.append(top)

        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix (Reverse Polish Notation) expression.

        Args:
            tokens (list): List of tokens in postfix order.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ValueError: If the expression is malformed.
        """
        stack = []
        for token in tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in "+-*/":
                if len(stack) < 2:
                    raise ValueError("Insufficient operands for operator.")
                b = stack.pop()  # Second operand.
                a = stack.pop()  # First operand.
                result = None
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    result = a / b
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in expression: {token}")

        if len(stack) != 1:
            raise ValueError("The expression is malformed; multiple items remain after evaluation.")
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


def main():
    """
    Entry point for the console-based arithmetic calculator.
    Continuously prompts the user for expressions, evaluates them,
    and outputs the result. To exit, the user may input an empty line
    or interrupt the program.
    """
    calc = Calculator()
    print("Arithmetic Calculator (Enter an empty line to exit)")
    while True:
        try:
            expr = input("Enter expression: ")
            if not expr.strip():
                break
            result = calc.calculate(expr)
            print(f"Result: {result}")
        except Exception as ex:
            print(f"Error: {ex}")


if __name__ == "__main__":
    main()
