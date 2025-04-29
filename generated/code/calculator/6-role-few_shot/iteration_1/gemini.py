import re


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It handles operator precedence
    and validates input for correctness and security.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                parentheses, invalid characters, division by zero).
        """
        normalized_expression = self._normalize_expression(expression)
        self._validate_parentheses(normalized_expression)
        try:
            result = self._parse_expression(normalized_expression)
            return float(result)
        except ZeroDivisionError:
            raise ValueError("Division by zero encountered.")
        except (SyntaxError, ValueError) as e:
            raise ValueError(f"Invalid expression: {e}")


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
            ValueError: If the parentheses are unbalanced.
        """
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise ValueError("Unbalanced parentheses: unmatched ')'")
                stack.pop()
        if stack:
            raise ValueError("Unbalanced parentheses: unmatched '('")

    def _parse_expression(self, expression: str) -> float:
        """
        Parses the expression using the Shunting Yard algorithm.  This
        implementation handles operator precedence and parentheses.

        Args:
             expression: The normalized mathematical expression.

        Returns:
            The result of the expression.
        """

        def precedence(operator: str) -> int:
            """Helper function to determine operator precedence."""
            if operator in ('+', '-'):
                return 1
            if operator in ('*', '/'):
                return 2
            return 0

        def apply_operator(operators, values):
            """Applies an operator to the top two values on the value stack."""
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

        tokens = re.findall(r"(\b\d+\b|\d+\.\d+|\+|\-|\*|\/|\(|\))", expression)  # Improved tokenization
        values = []
        operators = []

        for token in tokens:
            if re.match(r"\b\d+\b|\d+\.\d+", token):  # Check for numbers (integers and floats)
                values.append(float(token))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operator(operators, values)
                operators.pop()  # Remove the '('
            elif token in ('+', '-', '*', '/'):
                while operators and precedence(operators[-1]) >= precedence(token):
                    apply_operator(operators, values)
                operators.append(token)

        while operators:
            apply_operator(operators, values)

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

