import re


class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions with
    addition, subtraction, multiplication, division, and parentheses.
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
        """
        normalized_expression = self._normalize_expression(expression)
        self._validate_parentheses(normalized_expression)
        return self._evaluate(normalized_expression)

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
        Validates that parentheses in the expression are balanced.

        Args:
            expression (str): The expression to validate.

        Raises:
            ValueError: If parentheses are unbalanced.
        """
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise ValueError("Unbalanced parentheses.")
                stack.pop()
        if stack:
            raise ValueError("Unbalanced parentheses.")

    def _evaluate(self, expression: str) -> float:
        """
        Evaluates a normalized mathematical expression.

        Args:
            expression (str): The normalized expression string.

        Returns:
            float:  The result of the expression.

        Raises:
            ValueError: If there's a division by zero.
        """
        tokens = self._tokenize(expression)
        postfix_tokens = self._infix_to_postfix(tokens)
        return self._evaluate_postfix(postfix_tokens)

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the expression string.

        Args:
            expression (str): The normalized expression.

        Returns:
              list: A list of tokens (numbers, operators and parentheses).
        """
        return re.findall(r"(\d+\.\d+|\d+|[+\-*/()])", expression)

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts an infix expression (list of tokens) to postfix notation.

        Args:
            tokens (list): List of tokens in infix notation.

        Returns:
           list: A list of tokens in postfix notation.
        """

        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        stack = []

        for token in tokens:
            if re.match(r"(\d+\.\d+|\d+)", token):  # If it's a number
                output.append(float(token))
            elif token in precedence:  # If it's an operator
                while stack and stack[-1] != '(' and precedence.get(stack[-1], -1) >= precedence[token]:
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Mismatched parentheses")
                stack.pop()  # Remove the '('

        while stack:
            if stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression (represented as a list of tokens).

        Args:
            tokens (list): List of tokens in postfix notation.

        Returns:
            float: The result value.

        Raises:
            ValueError: If there's a division by zero.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            else:  # It's an operator
                if len(stack) < 2:
                    raise ValueError("Invalid expression format")
                operand2 = stack.pop()
                operand1 = stack.pop()
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
        if len(stack) != 1:
           raise ValueError("Invalid expression format")
        return stack[0]

if __name__ == '__main__':
    calculator = Calculator()

    while True:
        try:
            expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print("Result:", result)
        except (ValueError, ZeroDivisionError) as e:
            print("Error:", e)

