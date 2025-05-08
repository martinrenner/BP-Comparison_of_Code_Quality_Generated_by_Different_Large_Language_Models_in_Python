import re  # Used for more robust tokenization

class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions.

    This class implements a calculator that supports addition, subtraction,
    multiplication, division, and parentheses. It uses the Shunting Yard
    algorithm to handle operator precedence and parentheses correctly.
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
        try:
            normalized_expression = self._normalize_expression(expression)
            if not self._is_balanced(normalized_expression):
                raise ValueError("Unbalanced parentheses.")
            tokens = self._tokenize(normalized_expression)
            postfix_tokens = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except ZeroDivisionError:
            raise ValueError("Division by zero.")
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")


    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating
        characters.

        Args:
            expression (str): A mathematical expression as a string.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if the parentheses in the expression are balanced.

        Args:
            expression (str): The expression to check.

        Returns:
            bool: True if parentheses are balanced, False otherwise.
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


    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes a mathematical expression.
        Example: "12.5 + (3 * -4)" -> ['12.5', '+', '(', '3', '*', '-4', ')']

        Args:
            expression (str):  The normalized expression string

        Returns:
            list: list of tokens.
        """
        # Use regular expression for robust tokenization, handling negative numbers correctly
        return re.findall(r"(\d+\.?\d*|\.\d+|[+\-*/()]|[-+]?\d+\.?\d*)", expression)

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts an infix expression (tokens) to postfix notation using the
        Shunting Yard Algorithm.

        Args:
            tokens (list): The list of tokens in infix notation.

        Returns:
            list: The list of tokens in postfix notation.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"([-+]?\d+\.?\d*|\.\d+)", token):  # Check for numbers (including decimals and negatives)
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
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Pop the '('
            else:
                raise ValueError(f"Invalid token: {token}")

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            tokens (list): The list of tokens in postfix notation.

        Returns:
            float: The result of the evaluation.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            else:  # It's an operator
                if len(stack) < 2:
                    raise ValueError("Invalid postfix expression")
                operand2 = stack.pop()
                operand1 = stack.pop()
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
                else:
                    raise ValueError(f"Invalid operator: {token}")
        if len(stack) != 1:
             raise ValueError("Invalid postfix expression")
        return stack[0]


# Example usage and testing
if __name__ == "__main__":
    calculator = Calculator()

    # Test cases
    test_cases = [
        ("2 + 3 * 4", 14.0),
        ("(2 + 3) * 4", 20.0),
        ("10 / (2 + 3)", 2.0),
        ("10 / 2 + 3", 8.0),
        ("10 - 2 * 3", 4.0),
        ("1 + 2 * (3 - 1) / 2", 3.0),
        ("-5 + 3", -2.0),
        ("10 / 0", ValueError),  # Division by zero
        ("2 + (3 * 4", ValueError),  # Unbalanced parentheses
        ("2 + a * 4", ValueError),  # Invalid character
        ("2.5 * 4", 10.0), # Decimal values
        ("10 / 2.5", 4.0),
        ("(1.5 + 2.5) * 3", 12.0),
        ("-1 * (-3 + 5)", -2),  # Negative numbers combined
        ("---1", ValueError), # consecutive negation signs
        ("1.1 + 2.2 + 3.3", 6.6),  # Chain of additions
        ("5 * 4 / 2", 10.0), #Multiplication and Division
        ("5 * (4 / 2)", 10.0), # Multiplication and Division with parentheses
        ("...", ValueError), #Non numeric tokens
    ]

    for expression, expected in test_cases:
        try:
            result = calculator.calculate(expression)
            print(f"Expression: {expression}, Result: {result}, Expected: {expected}, Pass: {result == expected}")
            assert result == expected, f"Test failed for {expression}. Expected {expected}, got {result}" #Added asserts
        except ValueError as e:
            print(f"Expression: {expression}, Result: {e}, Expected: {expected}, Pass: {type(e) == expected}") #Checks error type
            assert type(e) == expected, f"Test failed for {expression}. Expected {expected}, got {e}"

    print("All test cases passed!")

    # Interactive console usage
    while True:
        try:
            expression = input("Enter a mathematical expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print("Result:", result)
        except ValueError as e:
            print("Error:", e)
