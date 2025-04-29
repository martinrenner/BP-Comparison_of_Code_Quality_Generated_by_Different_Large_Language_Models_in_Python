import re
import unittest


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, parentheses, and floating-point numbers.  It adheres
    to operator precedence and provides input validation.  The design and
    implementation aim to meet aspects of ISO/IEC 25010 quality characteristics.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result.

        Args:
            expression: The arithmetic expression string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the input expression is invalid (e.g., unbalanced
                parentheses, invalid characters, division by zero).
            TypeError: On incorrect input types.
        """

        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        # Remove whitespace to simplify processing.
        expression = expression.replace(" ", "")

        # Input Validation:
        self._validate_expression(expression)

        # Tokenize, convert to postfix, and evaluate.
        tokens = self._tokenize(expression)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result


    def _validate_expression(self, expression: str):
        """
        Validates the expression for balanced parentheses and invalid characters.
        It also detects multiple consecutive operators.
        """

        # Check for invalid characters using a regular expression.
        if re.search(r"[^\d\+\-\*\/\(\)\.]", expression):
            raise ValueError("Invalid characters in expression.")

        # Check for balanced parentheses.
        parenthesis_level = 0
        for char in expression:
            if char == '(':
                parenthesis_level += 1
            elif char == ')':
                parenthesis_level -= 1
            if parenthesis_level < 0:
                raise ValueError("Unbalanced parentheses (unexpected closing parenthesis).")
        if parenthesis_level != 0:
            raise ValueError("Unbalanced parentheses (missing closing parenthesis).")


        # Check for multiple consecutive operators (e.g., ++, --, *+, etc.)
        # Allow cases like '2*-3' (2 multiplied by -3). Handle cases with parentheses.
        for i in range(len(expression) - 1):
            if (expression[i] in "+-*/") and (expression[i+1] in "+*/"):
                # Check if it is a number followed by a negative sign
                prev_char_index = self._find_previous_non_operator(expression, i)
                # Invalid cases: *, /, +/, */, ++, +*, ...
                # Allowed cases: Digit-,( -,+-,*-
                if prev_char_index == -1 and expression[i+1] != '-':  # Starts with invalid operator.
                    raise ValueError(f"Invalid consecutive operators at index {i}: '{expression[i]}{expression[i+1]}'")
                
                if prev_char_index != -1:
                    prev_char = expression[prev_char_index]
                    #Previous char must be a digit or a closed parenthesis.
                    if prev_char not in '0123456789)' and expression[i+1] != '-':
                        raise ValueError(f"Invalid consecutive operators at index {i}: '{expression[i]}{expression[i+1]}'")


    def _find_previous_non_operator(self, expression, index):
        """ Helper method to find non +-*/ operators """

        current_index = index - 1
        while current_index >= 0:
            if expression[current_index] not in "+-*/":
                return current_index
            current_index -=1
        return -1


    def _tokenize(self, expression: str) -> list[str]:
        """
        Tokenizes the expression string into a list of tokens (numbers, operators,
        and parentheses).
        """
        # Use regular expression to handle numbers (including decimals and negatives), operators, and parentheses.
        tokens = re.findall(r"(\d+\.?\d*|\.\d+|[-+*/()]|\d+)", expression)
        return tokens


    def _infix_to_postfix(self, tokens: list[str]) -> list[str]:
        """
        Converts the infix expression tokens to postfix notation using the
        Shunting Yard algorithm.

        Args:
            tokens: A list of tokens in infix notation.

        Returns:
            A list of tokens in postfix notation.
        """

        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"(\d+\.?\d*|\.\d+)", token):  # Number (including decimals) - Improved Regex.
                output.append(float(token))  # Convert to float during tokenization.
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                operator_stack.pop()  # Remove the '('
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            else:
                raise ValueError(f"Unknown token : {token}")

        while operator_stack:
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            tokens: A list of tokens in postfix notation.

        Returns:
            The result of the expression.

        Raises:
            ValueError: If division by zero is attempted.
        """
        stack = []

        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            else:
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
                        raise ValueError("Division by zero.")
                    stack.append(operand1 / operand2)

        if len(stack) != 1:
          raise ValueError("Invalid expression (too many operands).")
        return stack.pop()



class TestCalculator(unittest.TestCase):
    """
    Test cases for the Calculator class, covering various scenarios, including
    valid expressions, edge cases, error handling, and operator precedence.
    """
    def setUp(self):
        self.calculator = Calculator()

    def test_valid_expressions(self):
        self.assertAlmostEqual(self.calculator.calculate("2 + 3"), 5.0)
        self.assertAlmostEqual(self.calculator.calculate("10 - 5"), 5.0)
        self.assertAlmostEqual(self.calculator.calculate("2 * 3"), 6.0)
        self.assertAlmostEqual(self.calculator.calculate("10 / 5"), 2.0)
        self.assertAlmostEqual(self.calculator.calculate("2 + 3 * 4"), 14.0)
        self.assertAlmostEqual(self.calculator.calculate("(2 + 3) * 4"), 20.0)
        self.assertAlmostEqual(self.calculator.calculate("10 / (2 + 3)"), 2.0)
        self.assertAlmostEqual(self.calculator.calculate("2.5 + 3.5"), 6.0)
        self.assertAlmostEqual(self.calculator.calculate("-2 + 3"), 1.0)
        self.assertAlmostEqual(self.calculator.calculate("2 + -3"), -1.0)
        self.assertAlmostEqual(self.calculator.calculate("2 * -3"), -6.0)
        self.assertAlmostEqual(self.calculator.calculate("2 * ( -3 + 5)"), 4.0)
        self.assertAlmostEqual(self.calculator.calculate(" -2 * ( -3 + 5)"), -4.0)
        self.assertAlmostEqual(self.calculator.calculate("2 * (-3)"), -6.0)
        self.assertAlmostEqual(self.calculator.calculate("(-2) * (-3)"), 6.0)  # Test with parentheses around single negative numbers
        self.assertAlmostEqual(self.calculator.calculate("0.1 + 0.2"), 0.3)
        self.assertAlmostEqual(self.calculator.calculate("10"), 10.0)
        self.assertAlmostEqual(self.calculator.calculate("2*(1+3)"),8.0) #Without spaces
      

    def test_division_by_zero(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("10 / 0")
        self.assertEqual(str(context.exception), "Division by zero.")

        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("5 / (2 - 2)")
        self.assertEqual(str(context.exception), "Division by zero.")

    def test_unbalanced_parentheses(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("(2 + 3")
        self.assertEqual(str(context.exception), "Unbalanced parentheses (missing closing parenthesis).")

        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("2 + 3)")
        self.assertEqual(str(context.exception), "Unbalanced parentheses (unexpected closing parenthesis).")

        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("((2 + 3) * 4")
        self.assertEqual(str(context.exception), "Unbalanced parentheses (missing closing parenthesis).")

    def test_invalid_characters(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("2a + 3")
        self.assertTrue("Invalid characters" in str(context.exception))

    def test_invalid_input_type(self):
        with self.assertRaises(TypeError) as context:
            self.calculator.calculate(123)  # Pass an integer instead of a string
        self.assertEqual(str(context.exception), "Input expression must be a string.")
    
    def test_multiple_consecutive_operators(self):
        
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("2++3")
        self.assertIn("Invalid consecutive operators", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("2--3")
        self.assertIn("Invalid consecutive operators", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("2+/3")
        self.assertIn("Invalid consecutive operators", str(context.exception))

    def test_invalid_operands_count(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("2+")
        self.assertEqual(str(context.exception), "Invalid expression (not enough operands).")
        
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("+")
        self.assertIn("Invalid expression", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("2 3 +")
        self.assertEqual(str(context.exception), "Invalid expression (too many operands).")

    def test_edge_cases(self):
        self.assertAlmostEqual(self.calculator.calculate("   2 + 3   "), 5.0)  # Extra spaces
        self.assertAlmostEqual(self.calculator.calculate("2+3*4/2"), 8.0)      # Multiple operations
        self.assertAlmostEqual(self.calculator.calculate("0"), 0.0)         # Zero
        self.assertAlmostEqual(self.calculator.calculate("-0"), 0.0)        # Negative Zero
        self.assertAlmostEqual(self.calculator.calculate("(-(-2))"), 2.0)    #Nested negative
        self.assertAlmostEqual(self.calculator.calculate(".5 + .5"), 1.0)    # Decimal starting with .

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
        except ValueError as e:
            print("Error:", e)
        except TypeError as e:
            print("Error:", e)

if __name__ == "__main__":
    # Run tests first
    print("Running tests...\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    unittest.TextTestRunner(verbosity=2).run(suite)
    print("\n--- Calculator ---")
    main()

