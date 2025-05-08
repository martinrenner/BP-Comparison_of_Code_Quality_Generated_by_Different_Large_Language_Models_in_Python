import re  # Used for tokenization

class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions.

    This calculator supports addition, subtraction, multiplication, division,
    parentheses, and handles operator precedence.  It uses the Shunting Yard
    algorithm for expression evaluation.  It includes comprehensive error
    handling for invalid input and operations.
    """

    def __init__(self):
        """Initializes the Calculator object."""
        self.precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '(': 0  # Lowest precedence inside the stack
        }

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, division by zero).
            TypeError: If input has invalid type
        """
        try:
            if not isinstance(expression, str):
                raise TypeError("Input expression must be a string.")

            tokens = self._tokenize(expression)
            postfix = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix)
            return result
        except (ValueError, TypeError, ZeroDivisionError) as e:
            raise e # Re-raise for the caller to handle

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the input expression.

        Args:
            expression: The expression string.

        Returns:
            A list of tokens (numbers, operators, parentheses).

        Raises:
            ValueError: for invalid characters
        """
        # Regex to split by operators, parentheses, but keep them.
        # Also handles spaces and negative numbers correctly.
        tokens = re.findall(r"(\b\d+\.?\d*\b|[\+\-\*\/\(\)])", expression)

        # Validate tokens
        for token in tokens:
            if not re.match(r"^\d+\.?\d*$|^[\+\-\*\/\(\)]$|^\-\d+\.?\d*$", token):
                raise ValueError(f"Invalid character or token: {token}")
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts infix notation to postfix notation (RPN) using the Shunting Yard algorithm.

        Args:
            tokens: A list of tokens in infix notation.

        Returns:
            A list of tokens in postfix notation.
        Raises:
            ValueError: If there are unbalanced parentheses
        """
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"^\d+\.?\d*$", token) or re.match(r"^\-\d+\.?\d*$", token):  # Number or negative number
                output.append(float(token))  # Convert to float immediately
            elif token in self.precedence:  # Operator
                while (operator_stack and operator_stack[-1] != '(' and
                       self.precedence[operator_stack[-1]] >= self.precedence[token]):
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
                    raise ValueError("Unbalanced parentheses (missing opening parenthesis).")
            else:
                raise ValueError(f"Invalid token: {token}")

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Unbalanced parentheses (missing closing parenthesis).")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, postfix_tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            postfix_tokens: A list of tokens in postfix notation.

        Returns:
            The result of the evaluation.

        Raises:
            ValueError: If the expression contains an invalid operator or division by zero
        """
        stack = []

        for token in postfix_tokens:
            if isinstance(token, float):
                stack.append(token)
            else:  # Operator
                try:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise ValueError("Invalid expression (not enough operands).")

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
                else:
                    raise ValueError(f"Invalid operator: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression (too many operands).")

        return stack[0]

# Example usage and testing in a separate block:
if __name__ == "__main__":
    calculator = Calculator()

    test_cases = [
        ("2 + 3 * 4", 14.0),
        ("(2 + 3) * 4", 20.0),
        ("10 / (2 + 3)", 2.0),
        ("10 / 2 + 3", 8.0),
        ("10 - 2 * 3", 4.0),
        ("-5 + 2", -3.0),
        ("1.5 * 2", 3.0),
        ("1 + 2 * (3 - 1) / 4", 2.0),
        ("2 * (3 + 4 * (1 + 2))", 30.0),
        ("10 / 0", ZeroDivisionError),  # Expect exception
        ("2 + + 3", ValueError),  # Expect exception
        ("(2 + 3", ValueError),  # Expect exception
        ("2 + 3)", ValueError), # Expect exception
         ("2 ? 3", ValueError),  # Expect exception
        ("", ValueError), #Expect exception
    ]

    for expression, expected in test_cases:
        try:
            result = calculator.calculate(expression)
            if isinstance(expected, type) and issubclass(expected, Exception):
                 print(f"TEST FAILED: Expression: '{expression}'. Expected exception: {expected}, but no exception raised.")
            elif result != expected:
                print(f"TEST FAILED: Expression: '{expression}'. Expected: {expected}, Got: {result}")
            else:
                print(f"TEST PASSED: Expression: '{expression}'. Result: {result}")
        except Exception as e:
            if isinstance(expected, type) and issubclass(expected, Exception):
                if isinstance(e, expected):
                    print(f"TEST PASSED (Expected Exception): Expression: '{expression}'. Exception: {e}")
                else:
                   print(f"TEST FAILED: Expression: '{expression}'. Expected exception: {expected}, Got exception: {type(e)}")
            else:
                 print(f"TEST FAILED: Expression: '{expression}'. Unexpected exception: {e}")


    # Interactive console mode
    while True:
        try:
            expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
