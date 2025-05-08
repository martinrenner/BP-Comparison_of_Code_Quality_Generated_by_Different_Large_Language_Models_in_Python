import re

class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, parentheses, and operator precedence.  It handles
    both integers and floating-point numbers, including negative values.  The
    implementation adheres to ISO/IEC 25010 principles.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result.

        Args:
            expression: The arithmetic expression string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                parentheses, invalid characters, division by zero).
            TypeError: If expression is not a string
        """

        if not isinstance(expression, str):
            raise TypeError("Expression must be a string.")

        try:
            # Tokenize, parse, and evaluate
            tokens = self._tokenize(expression)
            postfix_tokens = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except (ValueError, TypeError, ZeroDivisionError) as e:
            raise e  # Re-raise for consistent error handling
        except Exception as e:  # Catching Unexpected errors
            raise ValueError(f"Unexpected error during calculation: {e}")


    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the input expression string.

        Args:
            expression: The input expression string.

        Returns:
            A list of tokens (numbers, operators, parentheses).
        """

        # Use regular expression to handle numbers (including decimals and negatives), operators, and parentheses
        tokens = re.findall(r"[-+]?\d*\.?\d+|[-+*/()]", expression)

        # Validate characters
        for token in tokens:
            if not re.match(r'^([-+]?\d*\.?\d+|[-+*/()])$', token):
                raise ValueError(f"Invalid character or token: {token}")

        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts an infix expression (represented as a list of tokens) to
        postfix notation (Reverse Polish Notation) using the Shunting Yard algorithm.

        Args:
            tokens: A list of tokens in infix notation.

        Returns:
            A list of tokens in postfix notation.

        Raises:
            ValueError: if parentheses are unbalanced.
        """

        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"[-+]?\d*\.?\d+", token):  # Number (including decimals and negatives)
                output.append(float(token))  # Convert to float during tokenization
            elif token in precedence:  # Operator
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                try:
                    while operator_stack[-1] != '(':
                        output.append(operator_stack.pop())
                    operator_stack.pop()  # Remove the '('
                except IndexError:
                    raise ValueError("Unbalanced parentheses: Mismatched ')'")
            else:
                raise ValueError(f"Invalid token: {token}") # Redundant check, but good for safety

        while operator_stack:
            if operator_stack[-1] == '(': # Check for open parenthesis
                raise ValueError("Unbalanced parentheses: Mismatched '('")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression (represented as a list of tokens).

        Args:
            tokens: A list of tokens in postfix notation.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression contains division by zero or
                is otherwise invalid.
        """

        stack = []
        for token in tokens:
            if isinstance(token, float):  # Numbers pushed directly
                stack.append(token)
            else:  # Operator
                try:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise ValueError("Invalid expression: Not enough operands")

                if token == '+':
                    stack.append(operand1 + operand2)
                elif token == '-':
                    stack.append(operand1 - operand2)
                elif token == '*':
                    stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero")
                    stack.append(operand1 / operand2)
                else: # Redundant, but adding as a defensive
                    raise ValueError(F"Invalid operator in postfix: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression: Too many operands")
        return stack[0]
def main():
    """
    Main function to run the calculator in the console.
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
        except Exception as e: # Catches Unexpected errors
             print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
