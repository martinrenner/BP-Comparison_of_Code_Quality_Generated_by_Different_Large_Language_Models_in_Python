import re

class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, parentheses, and floating-point numbers.  It adheres
    to operator precedence and provides input validation.
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
                    raise ValueError("Unbalanced parentheses: unmatched ')'")
                stack.pop()
        if stack:
            raise ValueError("Unbalanced parentheses: unmatched '('")

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the normalized expression.

        Args:
            expression: The normalized mathematical expression.

        Returns:
          A list of tokens (numbers, operators, and parentheses).
        """

        return re.findall(r"(\d+\.?\d*|\+|\-|\*|\/|\(|\))", expression)


    def _parse_expression(self, tokens: list) -> float:
        """
        Parses the tokenized expression using the Shunting Yard algorithm and
        evaluates it.  Handles operator precedence and parentheses.

        Args:
            tokens: A list of tokens.

        Returns:
            The result of the evaluated expression.
        """
        def precedence(operator):
            if operator in ('+', '-'):
                return 1
            if operator in ('*', '/'):
                return 2
            return 0

        def apply_operator(operators, values):
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


        values = []
        operators = []

        for token in tokens:
            if re.match(r"\d+\.?\d*", token):  # If it's a number
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

        return values[0]



def main():
    """
    Main function to run the calculator in the console.
    """
    calculator = Calculator()
    while True:
        try:
            expression = input("Enter a mathematical expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print("Result:", result)
        except ValueError as e:
            print("Error:", e)
        except Exception as e:
            print("An unexpected error occurred", e)


if __name__ == "__main__":
    main()
