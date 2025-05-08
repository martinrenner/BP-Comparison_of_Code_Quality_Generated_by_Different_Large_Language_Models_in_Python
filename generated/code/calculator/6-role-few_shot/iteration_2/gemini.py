import re


class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions with
    addition, subtraction, multiplication, division, and parentheses.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
        """
        normalized_expression = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expression):
            raise ValueError("Expression has unbalanced parentheses.")

        try:
            result = self._parse_expression(normalized_expression)
            return float(result)
        except ZeroDivisionError:
            raise ValueError("Division by zero encountered.")
        except (SyntaxError, TypeError) as e:
            raise ValueError(f"Invalid expression: {e}")


    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.

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

    def _parse_expression(self, expression: str) -> float:
        """
        Parses a mathematical expression and returns the result.  This method
        implements the shunting yard algorithm to handle operator precedence.

        Args:
            expression (str): The normalized mathematical expression.

        Returns:
            float: The result of the expression.

        Raises:
            SyntaxError: If the expression is malformed.
        """

        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        operator_stack = []

        tokens = re.findall(r"(\d+\.?\d*|\+|\-|\*|\/|\(|\))", expression)

        for token in tokens:
            if re.match(r"\d+\.?\d*", token):  # If the token is a number
                output_queue.append(float(token))
            elif token in precedence:  # If the token is an operator
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':  # If the token is a left parenthesis
                operator_stack.append(token)
            elif token == ')':  # If the token is a right parenthesis
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise SyntaxError("Mismatched parentheses")
                operator_stack.pop()  # Pop the '('

        while operator_stack:  # Pop any remaining operators
            if operator_stack[-1] == '(':
                raise SyntaxError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())

        # Evaluate the RPN expression
        evaluation_stack = []
        for token in output_queue:
            if isinstance(token, float):
                evaluation_stack.append(token)
            else:  # token is an operator
                if len(evaluation_stack) < 2:
                    raise SyntaxError("Malformed expression")
                operand2 = evaluation_stack.pop()
                operand1 = evaluation_stack.pop()
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

        if len(evaluation_stack) != 1:
            raise SyntaxError("Malformed expression")

        return evaluation_stack[0]


def main():
    """
    Main function to run the calculator in a loop.
    """
    calculator = Calculator()
    while True:
        try:
            expression = input("Enter a mathematical expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

