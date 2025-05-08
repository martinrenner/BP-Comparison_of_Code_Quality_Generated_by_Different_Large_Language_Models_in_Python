import re
import unittest


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It handles operator precedence
    correctly and accepts both integers and floating-point numbers.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression and returns the result.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the input expression is invalid (e.g., unbalanced
                parentheses, invalid characters, division by zero).
            TypeError: if the input is not string
        """

        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        # Remove whitespace from the expression
        expression = expression.replace(" ", "")

        # Tokenize the expression
        tokens = self._tokenize(expression)

        # Check for empty expression after whitespace removal
        if not tokens:
            raise ValueError("Input expression cannot be empty.")


        # Convert tokens to postfix notation (Reverse Polish Notation)
        postfix_tokens = self._infix_to_postfix(tokens)

        # Evaluate the postfix expression
        result = self._evaluate_postfix(postfix_tokens)

        return result

    def _tokenize(self, expression: str) -> list[str]:
        """
        Tokenizes the expression string into a list of tokens.

        Args:
            expression: string

        Returns:
             list of tokens
        """

        # Use regular expression to handle various scenarios, including negative numbers
        tokens = re.findall(r"(-?\d+\.?\d*)|[+\-*/()]", expression)

        # Validate characters
        for char in expression:
            if not re.match(r"[-.\d\s+\-*/()]", char):
                raise ValueError(f"Invalid character found: {char}")
        return tokens

    def _infix_to_postfix(self, tokens: list[str]) -> list[str]:
        """
        Converts a list of tokens from infix notation to postfix notation
        (Reverse Polish Notation) using the Shunting Yard algorithm.

        Args:
            tokens: list of tokens in infix notation

        Returns:
            list of tokens in postfix notation
        """

        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"-?\d+\.?\d*", token):  # Check for numbers (including negative)
                output.append(float(token))  # Convert to float during tokenization
            elif token in precedence:
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Unbalanced parentheses: Mismatched ')'")
                operator_stack.pop()  # Pop the '('
            else:
                raise ValueError(f"Invalid token: {token}")  # Should not happen due to regex in _tokenize()

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Unbalanced parentheses: Mismatched '('")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list[str]) -> float:
        """
        Evaluates a list of tokens in postfix notation.

        Args:
            tokens: list of tokens in postfix notation

        Returns:
             Result of expression
        """

        stack = []
        for token in tokens:
            if isinstance(token, float):  # Check if it's a number (already converted to float)
                stack.append(token)
            else:
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

        if len(stack) != 1:
            raise ValueError("Invalid expression: Too many operands")
        return stack[0]


class TestCalculator(unittest.TestCase):
    """
    Test cases for the Calculator class, covering various scenarios, 
    including edge cases and error handling.
    """

    def setUp(self):
        """Set up for test methods."""
        self.calculator = Calculator()

    def test_addition(self):
        """Test cases for Addition."""
        self.assertAlmostEqual(self.calculator.calculate("2+3"), 5.0)
        self.assertAlmostEqual(self.calculator.calculate("10.5+2.3"), 12.8)
        self.assertAlmostEqual(self.calculator.calculate("-5+3"), -2.0)

    def test_subtraction(self):
        """Test cases for Subtraction."""
        self.assertAlmostEqual(self.calculator.calculate("5-2"), 3.0)
        self.assertAlmostEqual(self.calculator.calculate("2-5"), -3.0)
        self.assertAlmostEqual(self.calculator.calculate("10.5-2.3"), 8.2)
        self.assertAlmostEqual(self.calculator.calculate("-5-3"), -8.0)
        self.assertAlmostEqual(self.calculator.calculate("3--5"), 8.0) #test double negative

    def test_multiplication(self):
        """Test cases for Multiplication."""
        self.assertAlmostEqual(self.calculator.calculate("2*3"), 6.0)
        self.assertAlmostEqual(self.calculator.calculate("-5*3"), -15.0)
        self.assertAlmostEqual(self.calculator.calculate("10.5*2"), 21.0)
        self.assertAlmostEqual(self.calculator.calculate("-4*-6"), 24.0)
        self.assertAlmostEqual(self.calculator.calculate("1.5*2.5"), 3.75)

    def test_division(self):
        """Test cases for Division."""
        self.assertAlmostEqual(self.calculator.calculate("6/2"), 3.0)
        self.assertAlmostEqual(self.calculator.calculate("10/4"), 2.5)
        self.assertAlmostEqual(self.calculator.calculate("7.5/2.5"), 3.0)
        self.assertAlmostEqual(self.calculator.calculate("-8/2"), -4.0)
        self.assertAlmostEqual(self.calculator.calculate("9/-3"), -3.0)
        # Division by zero and other division related error test
        with self.assertRaises(ZeroDivisionError):
            self.calculator.calculate("5/0")

    def test_parentheses(self):
        """Test cases with Parentheses."""
        self.assertAlmostEqual(self.calculator.calculate("(2+3)*4"), 20.0)
        self.assertAlmostEqual(self.calculator.calculate("2*(3+4)"), 14.0)
        self.assertAlmostEqual(self.calculator.calculate("(10-2)/4"), 2.0)
        self.assertAlmostEqual(self.calculator.calculate("2*(5-(3-1))/2"), 3.0)
        self.assertAlmostEqual(self.calculator.calculate("((2+3)*4)/2"), 10.0)

    def test_complex_expressions(self):
        """Test cases for Complex expressions."""
        self.assertAlmostEqual(self.calculator.calculate("2+3*4-5/5"), 13.0)
        self.assertAlmostEqual(self.calculator.calculate("2*(3+4)-5*2"), 4.0)
        self.assertAlmostEqual(self.calculator.calculate("(2+3)*(4-5)/5"), -1.0)
        self.assertAlmostEqual(self.calculator.calculate("10-(5-2)*3+4/2"), 3.0)
        self.assertAlmostEqual(self.calculator.calculate("2.5*4+(7-3)/2-1"), 11.0)
        self.assertAlmostEqual(self.calculator.calculate("-2 * (4-2)"), -4.0)
        self.assertAlmostEqual(self.calculator.calculate("(4 - 2) * -2"), -4.0)

    def test_invalid_input(self):
        """Test cases for Invalid inputs."""
        # Invalid character
        with self.assertRaises(ValueError):
            self.calculator.calculate("2+a")
        # Invalid number
        with self.assertRaises(ValueError):
            self.calculator.calculate("2..5+3")
        # Unbalanced open parenthesis
        with self.assertRaises(ValueError):
            self.calculator.calculate("(2+3")
        # Unbalanced close parenthesis
        with self.assertRaises(ValueError):
            self.calculator.calculate("2+3)")
        # Mismatched parentheses
        with self.assertRaises(ValueError):
            self.calculator.calculate("(2+3)*4)")
        # Multiple operators
        with self.assertRaises(ValueError):
            self.calculator.calculate("2++3")
        # Empty input
        with self.assertRaises(ValueError):
            self.calculator.calculate("")
        # Just spaces input
        with self.assertRaises(ValueError):
            self.calculator.calculate("   ")
        # Missing operand at the beginning(unary minus is handled now, so no error expected)
        self.assertAlmostEqual(self.calculator.calculate("-2+3"), 1) #Test unary operator
        # Missing operand at the beginning
        with self.assertRaises(ValueError):
            self.calculator.calculate("*2+3")
        # Missing operand at the end
        with self.assertRaises(ValueError):
            self.calculator.calculate("2+3*")
        # No operands at all
        with self.assertRaises(ValueError):
            self.calculator.calculate("*")
        # Too many operands
        with self.assertRaises(ValueError):
            self.calculator.calculate("1 2")
        # Input is not String
        with self.assertRaises(TypeError):
            self.calculator.calculate(2 + 3)

if __name__ == '__main__':
    # Create a Calculator instance
    calculator = Calculator()

    # Run tests
    # unittest.main(argv=[''], exit=False) # Use this line in jupyter notebook or interactive python

    # Run tests and capture the result
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)  # Removed verbosity=2

    # Check if tests were successful before prompting for input
    if result.wasSuccessful():
        # Get input from the user
        expression = input("Enter an arithmetic expression (or 'quit' to exit): ")

        while expression.lower() != 'quit':
            try:
                # Calculate the result
                result = calculator.calculate(expression)
                # Print the result
                print(f"Result: {result}")
            except ValueError as e:
                print(f"Error: {e}")
            except ZeroDivisionError as e:
                print(f"Error: {e}")

            # Get the next input
            expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
    else:
        print("Please fix the errors in tests first")

