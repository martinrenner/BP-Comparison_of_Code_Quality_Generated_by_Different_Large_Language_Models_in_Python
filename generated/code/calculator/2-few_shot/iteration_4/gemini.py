import re


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It handles operator precedence
    and validates input for correctness and security.
    """

    def _tokenize(self, expression: str) -> list[str]:
        """
        Tokenizes the input expression into a list of numbers, operators, and parentheses.

        Args:
            expression: The mathematical expression string.

        Returns:
            A list of tokens.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Regex to split by operators and parentheses, keeping delimiters
        tokens = re.findall(r"(\d+\.?\d*|\+|\-|\*|\/|\(|\))", expression)

        # Validate that we only captured valid characters
        combined_tokens = "".join(tokens)
        cleaned_expression = expression.replace(" ", "")  # Remove spaces first
        if combined_tokens != cleaned_expression:
            raise ValueError("Expression contains invalid characters.")

        return tokens

    def _precedence(self, op: str) -> int:
        """
        Returns the precedence of an operator.

        Args:
            op: The operator (+, -, *, /).

        Returns:
            An integer representing the precedence (higher value means higher precedence).
        """
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        return 0  # For parentheses

    def _apply_op(self, operators: list[str], values: list[float]) -> None:
        """
        Applies the top operator from the operators stack to the top two values
        from the values stack.  Handles potential division by zero.

        Args:
            operators: The stack of operators.
            values: The stack of values.

        Raises:
            ValueError: If division by zero is attempted.
        """
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

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result.

        Args:
            expression: The mathematical expression string.

        Returns:
            The result of the calculation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
        """
        expression = expression.replace(" ", "") #remove blank spaces

        if not self._is_balanced(expression): #check parentheses balance
            raise ValueError("Unbalanced parentheses")

        tokens = self._tokenize(expression)  # Tokenize

        values = []
        operators = []

        for token in tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit():
                # If the token is a number (handling floats and negatives)
                values.append(float(token))

            elif token == '(':
                operators.append(token)

            elif token == ')':
                while operators and operators[-1] != '(':
                    self._apply_op(operators, values)
                operators.pop()  # Remove the '('

            elif token in ('+', '-', '*', '/'):
                # While top of 'operators' has same or greater precedence
                while (operators and operators[-1] != '(' and
                       self._precedence(operators[-1]) >= self._precedence(token)):
                    self._apply_op(operators, values)
                operators.append(token)

        # Apply remaining operators
        while operators:
            self._apply_op(operators, values)

        # Final result should be the only value left
        if len(values) != 1:
            raise ValueError("Invalid expression")  # Should not happen with proper validation
        return values[0]
    
    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether a mathematical expression has properly paired parentheses.

        :param expression: A string containing the mathematical expression.
        :return: True if parentheses are correctly paired, otherwise False.
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



def main():
    """
    Main function for the console-based calculator.  Interacts with the user.
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
