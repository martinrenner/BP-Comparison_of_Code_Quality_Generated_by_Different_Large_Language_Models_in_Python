import re  # Importing the regular expression module


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It adheres to operator precedence
    and handles both integer and floating-point numbers.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
            TypeError: If input is not a string
        """
        if not isinstance(expression, str):
            raise TypeError("Input must be a string.")

        normalized_expression = self._normalize_expression(expression)
        self._validate_parentheses(normalized_expression)
        tokens = self._tokenize(normalized_expression)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression by removing spaces and validating characters.

        Args:
            expression (str): The input expression.

        Returns:
            str: The normalized expression.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")

    def _validate_parentheses(self, expression: str) -> None:
        """
        Checks if the parentheses in the expression are balanced.

        Args:
            expression (str): The expression to check.

        Raises:
            ValueError: If the parentheses are unbalanced.
        """
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise ValueError("Unbalanced parentheses: Too many closing parentheses.")
                stack.pop()
        if stack:
            raise ValueError("Unbalanced parentheses: Unclosed opening parentheses.")

    def _tokenize(self, expression: str) -> list[str]:
        """
        Tokenizes the expression into a list of numbers and operators.  Handles
        multiple-digit numbers and decimal points.

        Args:
            expression (str): The normalized expression.

        Returns:
            list[str]: A list of tokens.
        """
        return re.findall(r"[-+]?\d*\.\d+|[-+]?\d+|[+\-*/()]", expression)  # Regular expression for tokenization


    def _infix_to_postfix(self, tokens: list[str]) -> list[str]:
        """
        Converts the infix expression (represented as a list of tokens) to
        postfix notation (Reverse Polish Notation) using the Shunting Yard algorithm.

        Args:
            tokens (list[str]):  The list of tokens in infix notation.

        Returns:
            list[str]: The list of tokens in postfix notation.

        Raises:
            ValueError: If there's an unexpected error during conversion.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"[-+]?\d*\.\d+|[-+]?\d+", token):  # Check if it is a number (integer or float)
                output.append(token)
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses.")  # Extra closing parenthesis
                operator_stack.pop()  # Pop the '('
            else:
                 raise ValueError(f"Invalid token: {token}")

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses.")   # Extra opening parenthesis
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list[str]) -> float:
        """
        Evaluates a postfix expression (represented as a list of tokens).

        Args:
            tokens (list[str]): The list of tokens in postfix notation.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression attempts division by zero or contains invalid operators.
        """
        stack = []
        for token in tokens:
            if re.match(r"[-+]?\d*\.\d+|[-+]?\d+", token):
                stack.append(float(token))  # Convert to float to handle decimals
            else:
                try:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise ValueError("Invalid expression: Insufficient operands.")

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
                else:
                    raise ValueError(f"Invalid operator: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression: Too many operands.")
        return stack[0]


def main():
    """Main function to run the calculator."""
    calculator = Calculator()
    while True:
        try:
            expression = input("Enter a mathematical expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

