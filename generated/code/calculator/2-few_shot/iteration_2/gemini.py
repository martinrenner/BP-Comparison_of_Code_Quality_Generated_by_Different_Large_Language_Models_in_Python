import re


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses, conforming to operator precedence.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the expression.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
        """
        normalized_expression = self._normalize_expression(expression)
        self._validate_parentheses(normalized_expression)
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
                    raise ValueError("Unbalanced parentheses: Too many closing parentheses.")
                stack.pop()
        if stack:
            raise ValueError("Unbalanced parentheses: Unclosed opening parentheses.")

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the expression into a list of numbers and operators.  Handles
        multi-digit numbers, decimal points, and negative signs correctly.

        Args:
            expression (str): The normalized expression string.

        Returns:
            list: A list of tokens (numbers and operators).
        """
        return re.findall(r"[-+]?\d*\.?\d+|[-+*/()]", expression)


    def _parse_expression(self, tokens: list) -> float:
        """
        Parses the tokenized expression and evaluates it, respecting operator precedence.
        Uses the Shunting Yard algorithm to convert infix notation to postfix (RPN) and then evaluates RPN.

        Args:
           tokens (list): The list of tokens.

        Returns:
            float: The result of the expression.
        Raises:
            ValueError: If expression is invalid
        """

        def precedence(operator: str) -> int:
            """Returns the precedence of an operator."""
            if operator in ('+', '-'):
                return 1
            if operator in ('*', '/'):
                return 2
            return 0

        def apply_operator(operators: list, values: list) -> None:
            """Applies an operator to the top two values on the value stack."""
            try:
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
                        raise ValueError("Division by zero")
                    values.append(left / right)
            except IndexError:
                raise ValueError("Invalid expression format")


        values = []
        operators = []

        for token in tokens:
            if re.match(r"[-+]?\d*\.?\d+", token):  # Check if it's a number (including negative numbers)
                values.append(float(token))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operator(operators, values)
                if not operators:
                    raise ValueError("Invalid expression: Mismatched parentheses")
                operators.pop()  # Pop the '('
            elif token in ('+', '-', '*', '/'):
                while operators and operators[-1] != '(' and precedence(operators[-1]) >= precedence(token):
                    apply_operator(operators, values)
                operators.append(token)

        while operators:
            if operators[-1] == '(':
                raise ValueError("Invalid Expression: Mismatched parentheses")  # extra '('
            apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("Invalid expression format")

        return values[0]



def main():
    """
    Main function for the console-based calculator.
    """
    calculator = Calculator()
    while True:
        try:
            expression = input("Enter a mathematical expression (or type 'exit' to quit): ")
            if expression.lower() == 'exit':
                break
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

