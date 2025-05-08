import re


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, parentheses, and correct operator precedence.
    It handles both integers and floating-point numbers (including negatives).
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression and returns the result.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
        """
        try:
            return self._evaluate_expression(self._tokenize(expression))
        except ZeroDivisionError:
            raise ValueError("Division by zero error.")
        except (IndexError, AttributeError):
            raise ValueError("Invalid expression format: Check operators and parentheses.")


    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the input expression into a list of numbers, operators, and parentheses.

        Args:
            expression: The input expression string.

        Returns:
             A list of tokens.

        Raises:
            ValueError:  If expression contains not allowed characters
        """
        # Remove all whitespace first for consistent tokenization
        expression = expression.replace(" ", "")

        # Regular expression to split the expression into tokens.  This regex handles:
        #   - Numbers (integers and decimals, including negative numbers)
        #   - Operators (+, -, *, /)
        #   - Parentheses ( and )
        token_pattern = r"(-?\d+\.?\d*|[\+\-\*\/\(\)])"
        tokens = re.findall(token_pattern, expression)

        # Validate characters:  This check happens *after* splitting to handle
        #  cases like "2 * (3+x)" correctly (where "x" is the invalid part).
        allowed_chars = r"^[0-9\+\-\*\/\(\)\.]+$"  # Floating point allowed
        if not re.match(allowed_chars, expression):
            raise ValueError("Invalid characters in expression.")

        return tokens


    def _evaluate_expression(self, tokens: list) -> float:
        """
        Evaluates a tokenized arithmetic expression using the Shunting Yard algorithm.

        Args:
            tokens: A list of tokens representing the expression.

        Returns:
            The result of evaluating the expression.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses).
        """

        def precedence(operator):
            if operator in ('+', '-'):
                return 1
            if operator in ('*', '/'):
                return 2
            return 0

        def apply_operator(operators, values):
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
                        raise ZeroDivisionError("Division by zero")  # Explicitly check.
                    values.append(left / right)
            except IndexError:
                raise ValueError("Invalid expression: operator/operand mismatch")

        values = []
        operators = []

        for token in tokens:
            if re.match(r"^-?\d+\.?\d*$", token):  # numbers (including negative)
                values.append(float(token))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                try:
                    while operators[-1] != '(':
                        apply_operator(operators, values)
                    operators.pop()  # Pop the '('
                except IndexError:
                    raise ValueError("Unbalanced parentheses")  # Mismatched )

            elif token in ('+', '-', '*', '/'):
                while (operators and operators[-1] != '(' and
                       precedence(operators[-1]) >= precedence(token)):
                    apply_operator(operators, values)
                operators.append(token)

        while operators:
            if operators[-1] == '(':  # Check and raise for unbalanced (
                raise ValueError("Unbalanced parentheses") # Mismatched (
            apply_operator(operators, values)

        if len(values) != 1:  # Should be exactly one value left
            raise ValueError("Invalid Expression: Check operators and operands")

        return values[0]


def main():
    """Main function to run the calculator in a loop."""
    calculator = Calculator()
    while True:
        try:
            expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print("Result:", result)
        except ValueError as e:
            print("Error:", e)
        except Exception as e:  # General exception handling
            print(f"An unexpected error occurred: {e}")



if __name__ == "__main__":
    main()

