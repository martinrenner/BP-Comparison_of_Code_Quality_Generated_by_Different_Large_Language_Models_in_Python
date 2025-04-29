import re


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It handles operator precedence
    and  validates input for correctness and security.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the expression.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, division by zero).
        """
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
            expression (str): The mathematical expression.

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
            expression (str): The mathematical expression.

        Raises:
            ValueError: If parentheses are unbalanced.
        """
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise ValueError("Unbalanced parentheses: too many closing parentheses.")
                stack.pop()
        if stack:
            raise ValueError("Unbalanced parentheses: unclosed opening parentheses.")

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the expression into numbers, operators, and parentheses.

        Args:
            expression (str): The mathematical expression.

        Returns:
            list: A list of tokens.
        """
        return re.findall(r"(\d+\.?\d*|\+|\-|\*|\/|\(|\))", expression)

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts an infix expression (list of tokens) to postfix notation
        using the Shunting Yard algorithm.

        Args:
            tokens (list): The infix expression as a list of tokens.

        Returns:
            list: The postfix expression as a list of tokens.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"\d+\.?\d*", token):  # If it's a number
                output.append(float(token))
            elif token in precedence:  # If it's an operator
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
                    raise ValueError("Mismatched parentheses.")
                operator_stack.pop()  # Remove the '('

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses.")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            tokens (list):  The postfix expression as a list of tokens.

        Returns:
            float: The result of the expression.

        Raises:
            ValueError: If the expression is invalid (e.g., division by zero).
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            else:  # token is an operator
                if len(stack) < 2:
                    raise ValueError("Invalid expression (not enough operands).")
                operand2 = stack.pop()
                operand1 = stack.pop()
                if token == '+':
                    result = operand1 + operand2
                elif token == '-':
                    result = operand1 - operand2
                elif token == '*':
                    result = operand1 * operand2
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero.")
                    result = operand1 / operand2
                else:
                    raise ValueError(f"Invalid operator: {token}")
                stack.append(result)

        if len(stack) != 1:
             raise ValueError("Invalid expression (too many operands).")
        return stack.pop()


def main():
    """
    Main function to run the calculator in a console loop.
    """
    calculator = Calculator()
    while True:
        try:
            expression = input("Enter a mathematical expression (or 'exit' to quit): ")
            if expression.lower() == 'exit':
                break
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")  # Catch-all for unexpected errors


if __name__ == "__main__":
    main()

