import re

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
            TypeError: If input is not string
        """
        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        normalized_expression = self._normalize_expression(expression)
        self._validate_expression(normalized_expression)
        tokens = self._tokenize(normalized_expression)
        result = self._parse_expression(tokens)
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

    def _validate_expression(self, expression: str):
        """
        Validates the expression for balanced parentheses.

        Args:
            expression (str):  The expression to validate

        Raises:
            ValueError: If parentheses are unbalanced.
        """
        if not self._is_balanced(expression):
            raise ValueError("Unbalanced parentheses in expression.")


    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if the parentheses in the expression are balanced.

        Args:
            expression (str): The expression to check.

        Returns:
            bool: True if balanced, False otherwise.
        """
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        return not stack  # Stack should be empty if balanced


    def _tokenize(self, expression: str) -> list[str]:
        """
        Tokenizes the expression into a list of numbers and operators.

        Args:
            expression (str): The normalized expression.

        Returns:
            list[str]: A list of tokens.
        """
        return re.findall(r"(\d+\.\d+|\d+|[+\-*/()])", expression)

    def _parse_expression(self, tokens: list[str]) -> float:
        """
        Parses the tokenized expression and evaluates it using operator precedence.
        Uses the Shunting Yard algorithm.

        Args:
            tokens (list[str]): The list of tokens.

        Returns:
            float: The result of the expression.

        Raises:
            ValueError: On division by zero.
        """
        def precedence(operator: str) -> int:
            """Helper function to get precedence of an operator."""
            if operator in ('+', '-'):
                return 1
            if operator in ('*', '/'):
                return 2
            return 0

        def apply_operator(operators: list[str], values: list[float]):
            """Helper function to apply an operator to two values."""
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
                    raise ValueError("Division by zero.")
                values.append(left / right)


        values = []
        operators = []

        for token in tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit():  # Check if it's a number (including floats and negatives)
                values.append(float(token))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operator(operators, values)
                operators.pop()  # Pop the '('
            else:  # It's an operator
                while operators and operators[-1] != '(' and precedence(operators[-1]) >= precedence(token):
                    apply_operator(operators, values)
                operators.append(token)

        while operators:
            apply_operator(operators, values)

        return values[0]  # Final result


# Example usage and testing.
if __name__ == "__main__":
    calculator = Calculator()

    test_cases = [
        ("2 + 3 * 4", 14.0),
        ("(2 + 3) * 4", 20.0),
        ("10 / (2 + 3)", 2.0),
        ("10 / 2 + 3", 8.0),
        ("10.5 - 2.5 * 2", 5.5),
        ("-5 + 3", -2.0),
        ("2 * (3 + 4) / (1 + 1)", 7.0),
        ("1 + 2 * (3 + 4 / (2 - 1))", 11),
        ("2 * -3", -6.0),
        (" -2  + 3", 1.0) #Test for whitespaces with negative numbers
    ]
    
    # Test correctness
    for expression, expected in test_cases:
        try:
            result = calculator.calculate(expression)
            print(f"Expression: {expression}, Result: {result}, Expected: {expected}")
            assert result == expected, f"Test failed for {expression}: expected {expected}, got {result}"
        except ValueError as e:
            print(f"Expression: {expression}, Error: {e}")

    # Test error handling
    error_test_cases = [
        ("2 +", "invalid characters"),
        ("(2 + 3", "Unbalanced parentheses"),
        ("2 + )", "Unbalanced parentheses"),
        ("1 / 0", "Division by zero."),
        ("abc", "invalid characters"),
        ("1..2", "invalid characters"),
        (123, "Input expression must be a string."),
   ]

    for expression, expected_error in error_test_cases:
        try:
            calculator.calculate(expression)
            print(f"Test FAILED for {expression}: Expected an error, but none occurred.")
            assert False, f"Test FAILED for {expression}: Expected {expected_error}, but no error occurred."
        except (ValueError, TypeError) as e:
            print(f"Expression: {expression}, Error: {e}, Expected: {expected_error}")
            # Use assert to raise an exception if the error message is not expected
            assert expected_error in str(e), f"Test failed for {expression}, Expected {expected_error}, but actual: {e}"

    print("All tests passed!")

