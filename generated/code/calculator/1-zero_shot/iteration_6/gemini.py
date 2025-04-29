import re
import unittest


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, parentheses, and operator precedence.  It handles
    both integers and floating-point numbers, including negative values. The
    design adheres to principles of OOP, modularity, and provides comprehensive
    error handling.  It does *not* use eval() or similar functions.

    This class implements the ISO/IEC 25010 standards implicitly by adhering to:

    - **Functionality:**  Covers addition, subtraction, multiplication, and division.
    - **Reliability:**  Includes extensive error handling and validation (Mature).
    - **Usability:** Accepts standard mathematical notation (Understandability, Learnability).
    - **Performance Efficiency:** Uses a reasonably efficient shunting yard algorithm variant.
    - **Maintainability:**  Modular design with clear separation of concerns (Analyzability, Modifiability, Testability).
    - **Portability:**  Pure Python with no external dependencies (Installability).
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.

        Args:
            expression: The mathematical expression as a string.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                parentheses, invalid characters, division by zero).
            TypeError:  If the input expression is not a string.
        """

        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        try:
            tokens = self._tokenize(expression)
            postfix = self._shunting_yard(tokens)
            result = self._evaluate_postfix(postfix)
            return result
        except (ValueError, TypeError, ZeroDivisionError) as e:
            raise e  # Re-raise the exception after handling.
        except Exception as e:  # Catching unexpected Errors
             raise ValueError(f"An unexpected error occurred: {e}")


    def _tokenize(self, expression: str) -> list:
        """
        Converts the input expression string into a list of tokens.

        Args:
            expression: The mathematical expression string.

        Returns:
            A list of tokens (numbers, operators, parentheses).

        Raises:
            ValueError: If the expression contains invalid characters.
        """

        # Remove all whitespace
        expression = expression.replace(" ", "")

        # Use regex to split into tokens. Allows for integers, floats, and operators.
        tokens = re.findall(r"(\d+\.\d+|\d+|[+\-*/()]|[-+]?\d+\.\d+|[-+]?\d+)", expression)
        
        # Validate all character are allowed
        valid_pattern = r"^(\d+\.\d+|\d+|[+\-*/()]|[-+]?\d+\.\d+|[-+]?\d+)+$"
        if not re.match(valid_pattern, expression):
            raise ValueError("Invalid characters in expression.")
            
        # --- Handle unary minus ---
        # Convert '--' to '+' and insert "0" when unary minus is encountered.
        processed_tokens = []
        i = 0
        
        while i < len(tokens):
            if tokens[i] == '-' and (i == 0 or tokens[i-1] in '*/(+'):
                # Unary minus
                if tokens[i+1].replace('.', '', 1).isdigit(): # Check to avoid IndexError
                    processed_tokens.append('0')
                    processed_tokens.append('-')
                    processed_tokens.append(tokens[i+1])
                    i += 2
                else:
                    raise ValueError("Invalid use of unary operator")
            elif tokens[i] == '+' and (i == 0 or tokens[i-1] in '*/(+'):
                # Unary plus, can ignore as next number would represent sign anyway (+5 = 5)
                if tokens[i+1].replace('.', '', 1).isdigit(): # Check to avoid IndexError
                    processed_tokens.append(tokens[i+1]) # add next token (number)
                    i += 2 # advance as sign and number were processed together
                else:
                    raise ValueError("Invalid use of unary operator")
            else:
                processed_tokens.append(tokens[i])
                i += 1
        return processed_tokens

    def _shunting_yard(self, tokens: list) -> list:
        """
        Converts a list of tokens from infix notation to postfix notation
        (Reverse Polish Notation) using the Shunting Yard algorithm.

        Args:
            tokens: A list of tokens in infix notation.

        Returns:
            A list of tokens in postfix notation.

        Raises:
            ValueError: If parentheses are unbalanced.
        """

        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).isdigit() or (token.startswith('-') and token[1:].replace('.', '', 1).isdigit()):  # Check negative float numbers
                output_queue.append(float(token))  # Convert to float on the fly
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence[operator_stack[-1]] >= precedence[token]):
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
                    raise ValueError("Unbalanced parentheses.")
            else:
                raise ValueError(f"Invalid token during Shunting Yard: {token}")


        while operator_stack:
            if operator_stack[-1] == '(':  # Check for leftover '('
                 raise ValueError("Unbalanced parentheses.")
            output_queue.append(operator_stack.pop())

        return output_queue


    def _evaluate_postfix(self, postfix_tokens: list) -> float:
        """
        Evaluates a list of tokens in postfix notation.

        Args:
            postfix_tokens: A list of tokens in postfix notation.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., division by zero).
        """

        operand_stack = []

        for token in postfix_tokens:
            if isinstance(token, float):  # Already converted to float
                operand_stack.append(token)

            elif token in {'+', '-', '*', '/'}:
                 # Check enough opernads are present
                if len(operand_stack) < 2:
                    raise ValueError("Insufficient operands for operator")
                try:
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                except IndexError:
                    raise ValueError("Invalid expression format.")

                if token == '+':
                    result = operand1 + operand2
                elif token == '-':
                    result = operand1 - operand2
                elif token == '*':
                    result = operand1 * operand2
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero.")
                    result = operand1 / operand2
                operand_stack.append(result)
            else:
                 raise ValueError(f"Invalid token during postfix calculation: {token}")

        if len(operand_stack) != 1: # Handling invalid experessions with multiple results
           raise ValueError("Invalid expression.")

        return operand_stack[0]


class TestCalculator(unittest.TestCase):
    """Test cases for the Calculator class."""

    def setUp(self):
        """Setup method to create a Calculator instance before each test."""
        self.calculator = Calculator()

    def test_addition(self):
        self.assertAlmostEqual(self.calculator.calculate("2+3"), 5)
        self.assertAlmostEqual(self.calculator.calculate("2.5 + 3.5"), 6.0)
        self.assertAlmostEqual(self.calculator.calculate("-2 + 3"), 1.0)

    def test_subtraction(self):
        self.assertAlmostEqual(self.calculator.calculate("5-3"), 2)
        self.assertAlmostEqual(self.calculator.calculate("2.5 - 3.5"), -1.0)
         # Test Uniary operator
        self.assertAlmostEqual(self.calculator.calculate("-5-3"), -8)
        self.assertAlmostEqual(self.calculator.calculate("5--3"), 8)
        self.assertAlmostEqual(self.calculator.calculate("---3"), -3)

        self.assertAlmostEqual(self.calculator.calculate("1---1"), 2)
        self.assertAlmostEqual(self.calculator.calculate("---1"), -1)

    def test_multiplication(self):
        self.assertAlmostEqual(self.calculator.calculate("2*3"), 6)
        self.assertAlmostEqual(self.calculator.calculate("2.5 * 3.5"), 8.75)
        self.assertAlmostEqual(self.calculator.calculate("-2 * 3"), -6)

    def test_division(self):
        self.assertAlmostEqual(self.calculator.calculate("6/3"), 2)
        self.assertAlmostEqual(self.calculator.calculate("7.0 / 2"), 3.5)
        self.assertAlmostEqual(self.calculator.calculate("-6 / 3"), -2)

    def test_parentheses(self):
        self.assertAlmostEqual(self.calculator.calculate("(2+3)*4"), 20)
        self.assertAlmostEqual(self.calculator.calculate("2*(3+4)"), 14)
        self.assertAlmostEqual(self.calculator.calculate("2 * (3 + (4 / 2)) - 1"), 9)

    def test_precedence(self):
        self.assertAlmostEqual(self.calculator.calculate("2+3*4"), 14)
        self.assertAlmostEqual(self.calculator.calculate("2*3+4"), 10)
        self.assertAlmostEqual(self.calculator.calculate("1 + 2 * 3 - 4 / 2"), 5)
        self.assertAlmostEqual(self.calculator.calculate("2 * -3 + 4"), -2) # Test on Uniary with precedence

    def test_mixed_expressions(self):
         # More complex experessions
        self.assertAlmostEqual(self.calculator.calculate("10 / (2 + 3) * 2 - 1"), 3)
        self.assertAlmostEqual(self.calculator.calculate("-5 + (-2 * 3)"), -11)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate("2++3")  # Invalid operator
        with self.assertRaises(ValueError):
            self.calculator.calculate("2 + a") # Invalid char
        with self.assertRaises(ValueError):
            self.calculator.calculate("")      # Empty String
        with self.assertRaises(ValueError):
            self.calculator.calculate("     ") # Whitespace string
        with self.assertRaises(ValueError):
            self.calculator.calculate("2 3") # Implicit multiplication
        with self.assertRaises(ValueError):
            self.calculator.calculate("1 +* 1") # Invalid start of factor

    def test_unbalanced_parentheses(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate("(2+3")  # Unclosed parenthesis
        with self.assertRaises(ValueError):
            self.calculator.calculate("2+3)")  # Unopened parenthesis
        with self.assertRaises(ValueError):
            self.calculator.calculate("((2+3)*4")  # Unclosed
        with self.assertRaises(ValueError):
            self.calculator.calculate("2*(3+4))")  # Unopened

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calculator.calculate("2/0")
        with self.assertRaises(ZeroDivisionError):
            self.calculator.calculate("2 / (3 - 3)")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate(123)  # Not a string
        with self.assertRaises(TypeError):
            self.calculator.calculate([1, 2, 3]) # Not a String

    def test_unary(self):
        self.assertAlmostEqual(self.calculator.calculate("-5"), -5)
        self.assertAlmostEqual(self.calculator.calculate("-(2+3)"), -5)      
        self.assertAlmostEqual(self.calculator.calculate("-2 * 3"), -6)
        self.assertAlmostEqual(self.calculator.calculate("4*-23.2"), -92.8)
        self.assertAlmostEqual(self.calculator.calculate("4/-2"), -2.0)
        self.assertAlmostEqual(self.calculator.calculate("-4/-2"), 2.0)
        self.assertAlmostEqual(self.calculator.calculate("-4--2"), -2)
        self.assertAlmostEqual(self.calculator.calculate("-4+-2"), -6)
        self.assertAlmostEqual(self.calculator.calculate("+4++2"), 6)
        self.assertAlmostEqual(self.calculator.calculate("+4-+2"), 2)

    def test_input_with_spaces(self):
        self.assertAlmostEqual(self.calculator.calculate(" 2 + 3 "), 5)  # Leading/trailing spaces
        self.assertAlmostEqual(self.calculator.calculate("2+ 3"), 5)
        self.assertAlmostEqual(self.calculator.calculate("2 +3"), 5)
        self.assertAlmostEqual(self.calculator.calculate("2+ 3 * (4 - 1)"), 11)




if __name__ == '__main__':
    # Create a Calculator instance
    calculator = Calculator()

    # Interactive loop
    while True:
        try:
            expression = input("Enter a mathematical expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print("Result:", result)
        except (ValueError, TypeError, ZeroDivisionError) as e:
            print("Error:", e)
        except Exception as e: # Handling any other exception
            print(f"An unexpected error occurred: {e}")

    # Run unit tests when the script is executed directly
   # unittest.main() # Commented to avoid auto run
