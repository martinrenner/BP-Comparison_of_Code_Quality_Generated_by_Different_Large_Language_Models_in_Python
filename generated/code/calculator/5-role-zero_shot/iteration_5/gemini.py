import re


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, parentheses, and correct operator precedence.
    It handles both integers and floating-point numbers.
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
            TypeError: If the input expression is not a string.
        """

        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        # Remove whitespace and validate characters
        expression = expression.replace(" ", "")
        self._validate_characters(expression)

        # Tokenize, convert to postfix, and evaluate.
        tokens = self._tokenize(expression)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _validate_characters(self, expression: str):
        """Validates that the expression contains only allowed characters."""
        if not re.match(r"^[0-9+\-*/().-]+$", expression):
            raise ValueError("Invalid characters in expression.")

    def _tokenize(self, expression: str) -> list[str]:
        """
        Tokenizes the input expression into a list of numbers, operators, and parentheses.
        Handles multiple-digit numbers, decimal points, and negative numbers correctly.
        """
        tokens = []
        current_number = ""

        for char in expression:
            if char.isdigit() or char == '.':
                current_number += char
            elif char in "+-*/()":
                if current_number:
                    tokens.append(current_number)
                    current_number = ""
                # Handle negative numbers (unary minus):
                if char == '-' and (not tokens or tokens[-1] in '+-*/('):
                    current_number += char
                else:
                    tokens.append(char)
            else:
                # Should not happen, but included for robustness
                raise ValueError(f"Unexpected Character: {char}")

        if current_number:
            tokens.append(current_number)
        return tokens

    def _infix_to_postfix(self, tokens: list[str]) -> list[str]:
        """
        Converts an infix expression (list of tokens) to postfix notation (Reverse Polish Notation)
        using the Shunting Yard algorithm.  Handles operator precedence and parentheses.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"^-?\d+(\.\d+)?$", token):  # Check for numbers (including negative and decimals)
                output.append(float(token))
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
                    raise ValueError("Unbalanced parentheses.")
                operator_stack.pop()  # Pop the '('
            else:
                raise ValueError(f"Invalid token: {token}")  # For unexpected inputs

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Unbalanced parentheses.")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list[str]) -> float:
        """
        Evaluates a postfix expression (list of tokens) and returns the result.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):  # Check if it's a number
                stack.append(token)
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid expression.")
                try:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise ValueError("Invalid Expression: Not Enough Operands")

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
                else:  # Should never happen with correct _infix_to_postfix
                    raise ValueError(f"Invalid operator: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression.")  # e.g., "2 3 +" is valid, "2 3 + 5" is not
        return stack.pop()



def main():
    """
    Main function to run the calculator in a console-based loop.
    """
    calculator = Calculator()
    while True:
        try:
            expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print("Result:", result)
        except (ValueError, TypeError, ZeroDivisionError) as e:
            print("Error:", e)
        except Exception as e:
            print(f"An unexpected error: {e}")

if __name__ == "__main__":
    main()

