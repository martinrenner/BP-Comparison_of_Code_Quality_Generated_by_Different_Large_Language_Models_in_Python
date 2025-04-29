import re
import unittest


class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions with
    addition, subtraction, multiplication, division, and parentheses.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result.

        Args:
            expression: The arithmetic expression string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
            TypeError: If input is not a string
        """

        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        try:
            # Tokenize, parse, and evaluate
            tokens = self._tokenize(expression)
            postfix_tokens = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except (ValueError, TypeError, ZeroDivisionError) as e:
            raise e  # Re-raise for consistent error handling

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the expression string into a list of numbers, operators, and parentheses.

        Args:
            expression: The arithmetic expression.
        Returns:
            list of tokens
        Raises:
            ValueError: for invalid characters within the string
        """

        # Regex to match valid tokens: integers, floats, operators (+,-,*,/), and parentheses ().
        token_pattern = r"(\d+\.?\d*|\.\d+|[+\-*/()]|\s+)"
        tokens = re.findall(token_pattern, expression)

        # Remove whitespace
        tokens = [token for token in tokens if not token.isspace()]

        cleaned_tokens = []
        i = 0
        while i < len(tokens):
            if tokens[i] == '-' and (i == 0 or tokens[i - 1] in '+-*/('):
                # Handle negative numbers
                if i + 1 < len(tokens) and re.match(r'\d+\.?\d*|\.\d+', tokens[i + 1]):
                    cleaned_tokens.append(str(float(tokens[i] + tokens[i + 1])))  # Combine '-' and number
                    i += 2  # Skip next token (already combined)
                else:
                    # if '-' is not followed by a digit, expression is invalid
                    raise ValueError("Invalid usage of '-' operator")
            else:
                cleaned_tokens.append(tokens[i])
                i += 1
        # Check for invalid characters immediately.  This improves security and gives better error messages.
        for token in cleaned_tokens:
            if not re.match(r"^\d+\.?\d*$|^\.\d+$|^[+\-*/()]$", token):
                raise ValueError(f"Invalid character or token: '{token}' in expression.")

        return cleaned_tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts a list of tokens from infix notation to postfix notation (Reverse Polish Notation).

        Args:
          tokens: tokens in infix notation
        Returns:
            tokens arranged in postfix notation
        Raises:
            ValueError: for unbalanced parentheses issues
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"^\d+\.?\d*$|^\.\d+$", token):  # Check for both integers and floats.
                output.append(float(token))  # Convert to float immediately
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence[operator_stack[-1]] >= precedence[token]):
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
                raise ValueError(f"Invalid operation: {token}")  # Should ideally not reach, earlier checks

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Unbalanced parentheses: Mismatched '('")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, postfix_tokens: list) -> float:
        """        Evaluates a list of tokens in postfix notation.

        Args:
            postfix_tokens (list): A list of tokens in postfix notation.

        Returns:
            float: The result of the evaluation.
        """
        operand_stack = []

        for token in postfix_tokens:
            if isinstance(token, float):
                operand_stack.append(token)
            else:  # token must be and operator
                try:
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                except IndexError:
                    raise ValueError("Invalid expression: insufficient operands")

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
            raise ValueError("Invalid expression: too many operands")

        return operand_stack[0]


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        self.assertAlmostEqual(self.calculator.calculate("1 + 2"), 3)
        self.assertAlmostEqual(self.calculator.calculate('1+2+3'), 6)

    def test_subtraction(self):
        self.assertAlmostEqual(self.calculator.calculate("5 - 3"), 2)
        self.assertAlmostEqual(self.calculator.calculate("1 - 2 - 1"), -2)

    def test_multiplication(self):
        self.assertAlmostEqual(self.calculator.calculate("2 * 4"), 8)
        self.assertAlmostEqual(self.calculator.calculate("2 * 3 * 4"), 24.0)

    def test_division(self):
        self.assertAlmostEqual(self.calculator.calculate("8 / 4"), 2)
        self.assertAlmostEqual(self.calculator.calculate("5 / 2"), 2.5)

    def test_precedence(self):
        self.assertAlmostEqual(self.calculator.calculate("2 + 3 * 4"), 14)
        self.assertAlmostEqual(self.calculator.calculate("10 / 2 - 1"), 4)

    def test_parentheses(self):
        self.assertAlmostEqual(self.calculator.calculate("(2 + 3) * 4"), 20)
        self.assertAlmostEqual(self.calculator.calculate("10 / (2 + 3)"), 2)
        self.assertAlmostEqual(self.calculator.calculate("(1 + (2 - (3 * (4 / 2))))"), -3)

    def test_negative_numbers(self):
        self.assertAlmostEqual(self.calculator.calculate("-1 + 2"), 1)
        self.assertAlmostEqual(self.calculator.calculate("2 * -3"), -6)
        self.assertAlmostEqual(self.calculator.calculate("-(1 + 2) * 3"), -9)
        self.assertAlmostEqual(self.calculator.calculate("-(-2)"), 2)
        self.assertAlmostEqual(self.calculator.calculate("1+-1"), 0)

    def test_floating_point_numbers(self):
        self.assertAlmostEqual(self.calculator.calculate("1.5 + 2.5"), 4)
        self.assertAlmostEqual(self.calculator.calculate("2.5 * 2.5"), 6.25)
        self.assertAlmostEqual(self.calculator.calculate("1 / 3"), 0.3333333333333333)
        self.assertAlmostEqual(self.calculator.calculate(".5 * 2"), 1)

    def test_mixed_operations(self):
        self.assertAlmostEqual(self.calculator.calculate("2 + 3 * 4 / 2 - 1"), 7)
        self.assertAlmostEqual(self.calculator.calculate('2+3*4/2-1'), 7)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calculator.calculate("1 / 0")

    def test_unbalanced_parentheses(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("(1 + 2")
        self.assertIn("Unbalanced parentheses", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("1 + 2)")
        self.assertIn("Unbalanced parentheses", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("((1+2)*3")
        self.assertIn("Unbalanced parentheses", str(context.exception))

    def test_invalid_characters(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("1 + a")
        self.assertIn("Invalid character", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("1 + ?")
        self.assertIn("Invalid character", str(context.exception))

    def test_invalid_expression_insufficient_operands(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("+")
        self.assertIn("Invalid expression", str(context.exception))
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("1 +")
        self.assertIn("Invalid expression", str(context.exception))

    def test_invalid_expression_too_many_operands(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("1 1 +")
        self.assertIn("Invalid expression", str(context.exception))

    def test_empty_input(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("")
        self.assertIn("Invalid expression", str(context.exception))

    def test_whitespace_handling(self):
        self.assertEqual(self.calculator.calculate(" 1 +   2  "), 3)
        self.assertEqual(self.calculator.calculate("   2  * (3 + 4)  "), 14)

    def test_invalid_input_type(self):
        with self.assertRaises(TypeError) as context:
            self.calculator.calculate(123)  # int
        self.assertIn("Input expression must be a string", str(context.exception))
        with self.assertRaises(TypeError) as context:
            self.calculator.calculate(None)  # NoneType
        self.assertIn("Input expression must be a string", str(context.exception))

    def test_invalid_usage_of_operator(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("1++1")
        self.assertIn("Invalid character or token", str(context.exception))
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("*1+1")
        self.assertIn("Invalid character or token", str(context.exception))


if __name__ == '__main__':
    # Run from terminal with python <file_name>.py
    unittest.main()

