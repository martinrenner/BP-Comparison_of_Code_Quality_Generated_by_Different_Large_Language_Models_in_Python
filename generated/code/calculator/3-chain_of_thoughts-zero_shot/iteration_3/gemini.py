import re  # Used for tokenization

class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions
    according to the standard order of operations, supporting parentheses.
    """

    def __init__(self):
        self.precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
        }

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., invalid characters,
                        unbalanced parentheses).
            ZeroDivisionError: If the expression attempts division by zero.
        """
        try:
            tokens = self._tokenize(expression)
            postfix_tokens = self._shunting_yard(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except (ValueError, ZeroDivisionError, TypeError) as e:
            raise e  # Re-raise the exception to be handled by the caller

    def _tokenize(self, expression: str) -> list:
        """
        Splits the expression into a list of tokens (numbers, operators, parentheses).

        Args:
            expression: The expression string.

        Returns:
            A list of tokens.
        """
        # Regex to split by operators and parentheses, keeping the delimiters.
        tokens = re.findall(r"(\d+\.\d+|\d+|[+\-*/()]|\s+)", expression)
        # filter out empty strings and whitespace.
        return [t for t in tokens if t.strip()]

    def _shunting_yard(self, tokens: list) -> list:
        """
        Converts the infix expression (tokens) to postfix notation (RPN).

        Args:
            tokens: The list of tokens in infix notation.

        Returns:
            A list of tokens in postfix notation.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if re.match(r"^-?\d+(\.\d+)?$", token):  # Check if it's a number (integer or decimal)
                output_queue.append(float(token))
            elif token in self.precedence:  # Check if it's an operator
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       self.precedence.get(operator_stack[-1], -1) >= self.precedence.get(token, -1)
                       ):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                try:
                    while operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    operator_stack.pop()  # Discard the '('
                except IndexError:
                    raise ValueError("Unbalanced parentheses")
            else:
                raise ValueError(f"Invalid character: {token}")

        while operator_stack:
            if operator_stack[-1] == '(':  # Check unbalanced parenthesis
                raise ValueError("Unbalanced parentheses")
            output_queue.append(operator_stack.pop())

        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates an expression in postfix notation (RPN).

        Args:
            tokens:  The list of tokens in postfix notation.

        Returns:
            The result of the expression.
        """
        value_stack = []

        for token in tokens:
            if isinstance(token, float):
                value_stack.append(token)
            else:  # It's an operator
                try:
                    operand2 = value_stack.pop()
                    operand1 = value_stack.pop()
                except IndexError:
                    raise ValueError("Invalid expression format")

                if token == '+':
                    value_stack.append(operand1 + operand2)
                elif token == '-':
                    value_stack.append(operand1 - operand2)
                elif token == '*':
                    value_stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero")
                    value_stack.append(operand1 / operand2)

        if len(value_stack) != 1:
            raise ValueError("Invalid expression format")
        return value_stack[0]


import unittest

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        self.assertAlmostEqual(self.calculator.calculate("2 + 3"), 5.0)
        self.assertAlmostEqual(self.calculator.calculate("2.5 + 3.5"), 6.0)
        self.assertAlmostEqual(self.calculator.calculate("-2 + 3"), 1.0)


    def test_subtraction(self):
        self.assertAlmostEqual(self.calculator.calculate("5 - 2"), 3.0)
        self.assertAlmostEqual(self.calculator.calculate("2.5 - 3.5"), -1.0)
        self.assertAlmostEqual(self.calculator.calculate("-2 - 3"), -5.0)

    def test_multiplication(self):
        self.assertAlmostEqual(self.calculator.calculate("2 * 3"), 6.0)
        self.assertAlmostEqual(self.calculator.calculate("2.5 * 3.5"), 8.75)
        self.assertAlmostEqual(self.calculator.calculate("-2 * 3"), -6.0)


    def test_division(self):
        self.assertAlmostEqual(self.calculator.calculate("6 / 3"), 2.0)
        self.assertAlmostEqual(self.calculator.calculate("7 / 2"), 3.5)
        self.assertAlmostEqual(self.calculator.calculate("-6 / 3"), -2.0)


    def test_parentheses(self):
        self.assertAlmostEqual(self.calculator.calculate("(2 + 3) * 4"), 20.0)
        self.assertAlmostEqual(self.calculator.calculate("2 + (3 * 4)"), 14.0)
        self.assertAlmostEqual(self.calculator.calculate("(2 + 3) * (4 - 1)"), 15.0)
        self.assertAlmostEqual(self.calculator.calculate("10 / (2 + 3)"), 2.0)

    def test_order_of_operations(self):
        self.assertAlmostEqual(self.calculator.calculate("2 + 3 * 4"), 14.0)
        self.assertAlmostEqual(self.calculator.calculate("10 / 2 - 3"), 2.0)
        self.assertAlmostEqual(self.calculator.calculate("2 * 3 + 4 / 2"), 8.0)

    def test_complex_expressions(self):
         self.assertAlmostEqual(self.calculator.calculate("2 * (3 + 4) / (1 + 1)"), 7.0)
         self.assertAlmostEqual(self.calculator.calculate("-5 + (10 * 2) / 4"), 0.0)
         self.assertAlmostEqual(self.calculator.calculate("((1 + 2) * 3) - 4 / (5 - 3)"), 7.0)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate("2 + a")  # Invalid character
        with self.assertRaises(ValueError):
            self.calculator.calculate("2 ++ 3") # Invalid expression
        with self.assertRaises(ValueError):
            self.calculator.calculate("2 + + 3")  # Consecutive operators
        with self.assertRaises(ValueError):
            self.calculator.calculate("2 * (3 + 4")  # Unbalanced parentheses
        with self.assertRaises(ValueError):
             self.calculator.calculate("2 * )3 + 4(")  # Unbalanced parentheses
        with self.assertRaises(ValueError):
            self.calculator.calculate("2 3")
        with self.assertRaises(ValueError):
            self.calculator.calculate(")1+1(")

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calculator.calculate("1 / 0")


if __name__ == '__main__':
    unittest.main()

    # Example of running from console:
    calculator = Calculator()
    while True:
        try:
            expression = input("Enter an arithmetic expression (or 'exit' to quit): ")
            if expression.lower() == 'exit':
                break
            result = calculator.calculate(expression)
            print("Result:", result)
        except (ValueError, ZeroDivisionError,TypeError) as e:
            print("Error:", e)
