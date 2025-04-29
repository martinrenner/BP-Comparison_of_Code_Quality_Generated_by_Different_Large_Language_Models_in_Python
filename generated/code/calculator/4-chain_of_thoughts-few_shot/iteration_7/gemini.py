import re  # Used for tokenization

class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions with
    addition, subtraction, multiplication, division, and parentheses.
    Adheres to operator precedence and handles errors gracefully.
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
            normalized_expression = self.normalize_expression(expression)
            if not self.is_balanced(normalized_expression):
                raise ValueError("Unbalanced parentheses.")

            tokens = self.tokenize(normalized_expression)
            postfix_tokens = self.infix_to_postfix(tokens)
            result = self.evaluate_postfix(postfix_tokens)
            return result

        except ZeroDivisionError:
            raise ValueError("Division by zero.")
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")



    def normalize_expression(self, expression: str) -> str:
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
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")

    def is_balanced(self, expression: str) -> bool:
        """
        Checks whether a mathematical expression has properly paired parentheses.

        Args:
            expression (str): A string containing the mathematical expression.

        Returns:
            bool: True if parentheses are correctly paired, otherwise False.
        """
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        return not stack  # If stack is empty, parentheses are balanced

    def precedence(self, operator: str) -> int:
        """
        Returns the precedence of a given operator.

        Args:
            operator (str): The operator (+, -, *, /).

        Returns:
            int: The precedence level (higher value means higher precedence).
        """
        if operator in ('+', '-'):
            return 1
        elif operator in ('*', '/'):
            return 2
        return 0  # For parentheses

    def tokenize(self, expression: str) -> list:
        """
        Tokenizes a mathematical expression into a list of numbers and operators.
        Handles multi-digit numbers, decimal points, and negative numbers correctly.

        Args:
            expression (str): The mathematical expression.

        Returns:
            list: A list of tokens (strings).
        """
        return re.findall(r"(\b\d+\.?\d*\b|\+|\-|\*|\/|\(|\))", expression)

    def infix_to_postfix(self, tokens: list) -> list:
        """
        Converts an infix expression (list of tokens) to postfix notation.

        Args:
            tokens (list): The list of tokens in infix notation.

        Returns:
            list: The list of tokens in postfix notation.
        """
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"\b\d+\.?\d*\b", token):  # If it's a number
                output.append(float(token))
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Pop the '('
            else:  # It's an operator
                while (operator_stack and
                       self.precedence(operator_stack[-1]) >= self.precedence(token)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())

        return output

    def evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression (list of tokens).

        Args:
            tokens (list): The list of tokens in postfix notation.

        Returns:
            float: The result of the evaluation.
        """
        operand_stack = []

        for token in tokens:
            if isinstance(token, float):  # Check if token is a float type
                operand_stack.append(token)
            else:
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression")
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()

                if token == '+':
                    operand_stack.append(operand1 + operand2)
                elif token == '-':
                    operand_stack.append(operand1 - operand2)
                elif token == '*':
                    operand_stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero")
                    operand_stack.append(operand1 / operand2)

        if len(operand_stack) != 1:
            raise ValueError("Invalid expression")

        return operand_stack.pop()


# --- Example Usage ---
if __name__ == "__main__":
    calculator = Calculator()

    # Test cases
    test_expressions = [
        "2 + 3 * 4",  # 14
        "(2 + 3) * 4",  # 20
        "10 / (2 + 3)",  # 2
        "10 - 2 * 3 + 1",  # 5
        "1 + 2 * (3 - 1) / 2", # 3
        "-5 + 2",  # -3 - Negative numbers
        "2.5 * 4",  # 10.0 - Decimal numbers
        "10 / 0", # Division by zero error
        "2 + (3 * 4",  # Unbalanced parentheses error
        "2 $ 3",  # Invalid character error
        "5 +" # Invalid expression
    ]

    for expression in test_expressions:
        try:
            result = calculator.calculate(expression)
            print(f"'{expression}' = {result}")
        except ValueError as e:
            print(f"'{expression}' - Error: {e}")
