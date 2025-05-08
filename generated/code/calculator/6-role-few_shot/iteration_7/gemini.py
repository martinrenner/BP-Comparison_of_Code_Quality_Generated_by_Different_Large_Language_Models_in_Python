import re


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It handles operator precedence
    and both integer and floating-point numbers.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, division by zero).
        """
        normalized_expression = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expression):
            raise ValueError("Unbalanced parentheses")

        try:
            result = self._parse_expression(normalized_expression)
            return float(result)
        except ZeroDivisionError:
            raise ValueError("Division by zero")
        except (ValueError, TypeError) as e: # added broader exception, original was just ValueError
            raise ValueError(f"Invalid expression: {e}")


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

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if the parentheses in the expression are balanced.

        Args:
            expression (str): The mathematical expression.

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

    def _parse_expression(self, expression: str) -> float:
        """
        Parses and evaluates a normalized mathematical expression.  This method
        implements the shunting yard algorithm to handle operator precedence.

        Args:
            expression (str): The normalized mathematical expression.

        Returns:
            float: The result of the expression.

        Raises:
            ValueError: If there are any errors during parsing.
        """

        def precedence(operator: str) -> int:
            """Helper function to get the precedence of an operator."""
            if operator in ('+', '-'):
                return 1
            if operator in ('*', '/'):
                return 2
            return 0

        def apply_operator(operators, values):
            """Applies an operator to the top two values on the values stack."""
            operator = operators.pop()
            right = values.pop()
            left = values.pop()
            if operator == '+':
                values.append(left + right)
            elif operator == '-':
                values.append(left - right)
            elif operator == '*':
                values.append(left * right)
            elif operator == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                values.append(left / right)

        tokens = re.findall(r"(\b\d+\.?\d*\b|\+|\-|\*|\/|\(|\))", expression)  # Improved tokenization
        values = []
        operators = []

        for token in tokens:
            if token.isdigit() or '.' in token:
                values.append(float(token))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operator(operators, values)
                if not operators:
                    raise ValueError ("Mismatched parentheses") # added for edge case when closing parentheses are more than opening ones
                operators.pop()  # Pop the '('
            elif token in ('+', '-', '*', '/'):
                while operators and precedence(operators[-1]) >= precedence(token):
                    apply_operator(operators, values)
                operators.append(token)

        while operators:
            if operators[-1] == '(':  # Added: Check to avoid apply_operation on '('
                raise ValueError("Mismatched parentheses")  # Handle unmatched '('
            apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("Invalid expression")  # More descriptive error

        return values[0]



def main():
    """
    Main function to run the calculator in a loop.
    """
    calculator = Calculator()
    while True:
        try:
            expression = input("Enter a mathematical expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
