import re


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, parentheses, and floating-point numbers.  It adheres
    to operator precedence and provides input validation.  This implementation
    specifically avoids using eval() or similar functions.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero, or incorrect operator placement).
        """
        try:
            # 1. Input Sanitization and Validation (Security and Correctness)
            sanitized_expression = self._sanitize_expression(expression)

            # 2. Tokenization (Modularity)
            tokens = self._tokenize(sanitized_expression)

            # 3. Shunting Yard Algorithm (Correctness and Performance)
            postfix_tokens = self._shunting_yard(tokens)

            # 4. Evaluation of Postfix Expression (Correctness)
            result = self._evaluate_postfix(postfix_tokens)

            return result

        except (ValueError, TypeError, ZeroDivisionError) as e:
            raise ValueError(f"Invalid expression: {e}") from e


    def _sanitize_expression(self, expression: str) -> str:
        """
        Sanitizes the input expression by removing whitespace and validating characters.

        Args:
          expression: The original expression.

        Returns:
            A sanitized expression string with whitespace removed.

        Raises:
            ValueError: If invalid characters are present.
        """
        sanitized_expression = expression.replace(" ", "")

        # Check for invalid characters (Security and Correctness).  Only allow numbers,
        # operators, parentheses, and decimal points.
        if not re.match(r"^[\d+\-*/().-]+$", sanitized_expression):
            raise ValueError("Invalid characters in expression.")

        # Check for multiple decimal point in the single number
        if any(".." in part for part in re.split(r"[\+\-*/()]", sanitized_expression)):
            raise ValueError("Invalid number format: multiple decimal points.")

        # Check for immediate incorrect operators combinations
        if re.search(r"[/+\-*/]{2,}", sanitized_expression):
            raise ValueError("Invalid operator sequence.")
        if re.search(r"[(][*/]", sanitized_expression) or re.search(r"[+\-*/][)]", sanitized_expression):
            raise ValueError("Invalid operator placement.")

        return sanitized_expression

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the sanitized expression string into a list of numbers and operators.

        Args:
            expression:  Sanitized expression string.

        Returns:
            A list of tokens (strings).

        Raises:
            ValueError: In case of adjacent numbers with missing operator
        """

        # Split into tokens with lookarounds to keep operators and parentheses as separate tokens
        tokens = re.findall(r"(\b\d+\.\d+|\b\d+|\+|\-|\*|\/|\(|\))", expression)  # Improved tokenization

        # check for adjacent numbers like 5 5.5
        if any(
            tokens[i].replace(".", "", 1).isdigit() and tokens[i + 1].replace(".", "", 1).isdigit()
                for i in range(len(tokens) - 1)
        ):
                raise ValueError("Missing operator between numbers.")

        return tokens

    def _shunting_yard(self, tokens: list) -> list:
        """
        Converts the token list from infix notation to postfix notation (Reverse
        Polish Notation) using the Shunting Yard Algorithm.

        Args:
            tokens: A list of tokens (numbers and operators).

        Returns:
            A list of tokens in postfix notation.

        Raises:
            ValueError: If parentheses are unbalanced.
          """
        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if re.match(r"^\d+\.?\d*$", token):  # Efficiently check if it's a number
                output_queue.append(float(token))  # Convert to float immediately
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Unbalanced parentheses (missing '(').")
                operator_stack.pop()  # Remove the '('

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Unbalanced parentheses (missing ')').")
            output_queue.append(operator_stack.pop())

        return output_queue

    def _evaluate_postfix(self, postfix_tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            postfix_tokens: A list of tokens in postfix notation.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., division by zero).
            TypeError: If an operand is of incorrect type during operations.
        """

        stack = []
        for token in postfix_tokens:
            if isinstance(token, float):  # Already converted to float in _shunting_yard
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
                        raise ZeroDivisionError("Division by zero.")
                    stack.append(operand1 / operand2)
                else:
                    raise ValueError(f"Unknown operator: {token}")
        if len(stack) != 1:
              raise ValueError("Invalid expression (too many operands)")

        return stack.pop()


def main():
    """
    Main function to run the calculator in a loop.
    """
    calculator = Calculator()

    while True:
        expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
        if expression.lower() == 'quit':
            break

        try:
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
