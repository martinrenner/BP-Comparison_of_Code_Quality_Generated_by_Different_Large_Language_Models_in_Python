import re

class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It handles operator precedence
    and both integer and floating-point numbers.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
        """
        try:
            return self._evaluate(self._tokenize(expression))
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"Invalid expression: {expression} - {e}")

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the expression string into a list of numbers, operators, and parentheses.

        Args:
            expression: The arithmetic expression string.

        Returns:
            A list of tokens.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Regular expression to split the expression into tokens.  Handles integers,
        # floating-point numbers, operators, and parentheses.  Spaces are ignored.
        tokens = re.findall(r"[-+]?\d*\.?\d+|[-+*/()]", expression.replace(" ", ""))

        # Validate characters: Ensure only allowed characters are present.
        for token in tokens:
            if not re.match(r"^([-+]?\d*\.?\d+|[-+*/()])$", token):
                raise ValueError(f"Invalid character: {token}")
        return tokens

    def _evaluate(self, tokens: list) -> float:
        """
        Evaluates the tokenized expression using the shunting yard algorithm.

        Args:
            tokens: A list of tokens representing the expression.

        Returns:
            The result of the expression.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        division by zero) or operator issues.

        """

        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        def process_operator(op):
            """Helper function to process operators based on precedence."""
            if op == '(':
                operator_stack.append(op)
            elif op == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Unbalanced parentheses")
                operator_stack.pop()  # Remove the '('
            else:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(op, -1)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(op)

        for token in tokens:
            if re.match(r"^[-+]?\d*\.?\d+$", token):  # Number (integer or float)
                output_queue.append(float(token))
            elif token in precedence:  # Operator
                process_operator(token)
            elif token in '()':  # Parenthesis
                process_operator(token)

        while operator_stack:
            if operator_stack[-1] == '(':  # Check for unbalanced opening parenthesis
                raise ValueError("Unbalanced parentheses")
            output_queue.append(operator_stack.pop())

        # Evaluate RPN (Reverse Polish Notation) using a stack
        evaluation_stack = []
        for token in output_queue:
            if isinstance(token, float):
                evaluation_stack.append(token)
            else:  # Operator
                try:
                    operand2 = evaluation_stack.pop()
                    operand1 = evaluation_stack.pop()
                except IndexError:
                    raise ValueError("Invalid expression format")

                if token == '+':
                    evaluation_stack.append(operand1 + operand2)
                elif token == '-':
                    evaluation_stack.append(operand1 - operand2)
                elif token == '*':
                    evaluation_stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero")
                    evaluation_stack.append(operand1 / operand2)
                else: # pragma: no cover  (This should be prevented during tokenization)
                       raise ValueError("Unknown Operator")
        if len(evaluation_stack) != 1:
            raise ValueError("Invalid Expression (too many values)") # should happen only if shunting-yard algorithm has a bug

        return evaluation_stack[0]


def main():
    """
    Main function to run the calculator in a console loop.
    """
    calculator = Calculator()

    while True:
        try:
            expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")
        except ZeroDivisionError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
