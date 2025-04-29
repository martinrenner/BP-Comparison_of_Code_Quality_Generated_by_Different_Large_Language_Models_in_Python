class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions.

    This class implements basic arithmetic operations (+, -, *, /)
    with support for parentheses and proper order of operations.
    It handles input validation and error handling.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, division by zero).
        """
        normalized_expression = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expression):
            raise ValueError("Unbalanced parentheses.")

        result = self._parse_and_evaluate(normalized_expression)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression (removes spaces, validates characters).

        Args:
          expression(str): the mathematical expression
        
        Returns:
          str: normalized string without spaces

        Raises:
          ValueError: with invalid characters
        """
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")
        
    def _is_balanced(self, expression: str) -> bool:
      """
      Check if the parentheses are balanced

      Args:
        expression (str): The mathematical expression

      Returns:
          bool: True if balanced, False otherwise
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

    def _parse_and_evaluate(self, expression: str) -> float:
        """
        Parses and evaluates the normalized expression.

        Args:
            expression (str): The normalized mathematical expression.

        Returns:
            float: The result of the evaluation.
        """
        tokens = self._tokenize(expression)
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        operator_stack = []

        for token in tokens:
            if self._is_number(token):
                output_queue.append(float(token))  # Convert to float here
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Pop the '('

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())

        return self._evaluate_postfix(output_queue)

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the expression into a list of numbers and operators.

        Args:
            expression (str): The mathematical expression.

        Returns:
            list: A list of tokens.
        """
        tokens = []
        current_number = ""
        for char in expression:
            if char.isdigit() or char == '.':
                current_number += char
            elif char in "+-*/()":
                if current_number:
                    tokens.append(current_number)
                    current_number = ""
                tokens.append(char)
            
        if current_number:
            tokens.append(current_number)
        return tokens

    def _is_number(self, token: str) -> bool:
        """
        Checks if a token is a valid number (integer or decimal).

        Args:
            token (str): The token to check.

        Returns:
            bool: True if the token is a number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _evaluate_postfix(self, postfix_expression: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            postfix_expression (list): The postfix expression as a list of tokens.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If division by zero is attempted.
        """
        stack = []
        for token in postfix_expression:
            if isinstance(token, float):
                stack.append(token)
            else:  # token is an operator
                if len(stack) < 2:
                    raise ValueError("Invalid expression")
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
                        raise ValueError("Division by zero")
                    stack.append(operand1 / operand2)
        if len(stack) != 1:
            raise ValueError("Invalid Expression!")   
        return stack.pop()


class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions.

    This class implements basic arithmetic operations (+, -, *, /)
    with support for parentheses and proper order of operations.
    It handles input validation and error handling.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, division by zero).
        """
        normalized_expression = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expression):
            raise ValueError("Unbalanced parentheses.")

        result = self._parse_and_evaluate(normalized_expression)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression (removes spaces, validates characters).

        Args:
          expression(str): the mathematical expression
        
        Returns:
          str: normalized string without spaces

        Raises:
          ValueError: with invalid characters
        """
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")
        
    def _is_balanced(self, expression: str) -> bool:
      """
      Check if the parentheses are balanced

      Args:
        expression (str): The mathematical expression

      Returns:
          bool: True if balanced, False otherwise
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

    def _parse_and_evaluate(self, expression: str) -> float:
        """
        Parses and evaluates the normalized expression.

        Args:
            expression (str): The normalized mathematical expression.

        Returns:
            float: The result of the evaluation.
        """
        tokens = self._tokenize(expression)
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        operator_stack = []

        for token in tokens:
            if self._is_number(token):
                output_queue.append(float(token))  # Convert to float here
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Pop the '('

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())

        return self._evaluate_postfix(output_queue)

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the expression into a list of numbers and operators.

        Args:
            expression (str): The mathematical expression.

        Returns:
            list: A list of tokens.
        """
        tokens = []
        current_number = ""
        for char in expression:
            if char.isdigit() or char == '.':
                current_number += char
            elif char in "+-*/()":
                if current_number:
                    tokens.append(current_number)
                    current_number = ""
                tokens.append(char)
            
        if current_number:
            tokens.append(current_number)
        return tokens

    def _is_number(self, token: str) -> bool:
        """
        Checks if a token is a valid number (integer or decimal).

        Args:
            token (str): The token to check.

        Returns:
            bool: True if the token is a number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _evaluate_postfix(self, postfix_expression: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            postfix_expression (list): The postfix expression as a list of tokens.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If division by zero is attempted.
        """
        stack = []
        for token in postfix_expression:
            if isinstance(token, float):
                stack.append(token)
            else:  # token is an operator
                if len(stack) < 2:
                    raise ValueError("Invalid expression")
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
                        raise ValueError("Division by zero")
                    stack.append(operand1 / operand2)
        if len(stack) != 1:
            raise ValueError("Invalid Expression!")   
        return stack.pop()



# Example Usage (and basic testing)
if __name__ == "__main__":
    calculator = Calculator()

    while True:
        try:
            expression = input("Enter a mathematical expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print("Result:", result)
        except ValueError as e:
            print("Error:", e)


import unittest

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        self.assertEqual(self.calculator.calculate("2+3"), 5)

    def test_subtraction(self):
        self.assertEqual(self.calculator.calculate("5-2"), 3)

    def test_multiplication(self):
        self.assertEqual(self.calculator.calculate("4*6"), 24)

    def test_division(self):
        self.assertEqual(self.calculator.calculate("10/2"), 5)

    def test_parentheses(self):
        self.assertEqual(self.calculator.calculate("(2+3)*4"), 20)

    def test_complex_expression(self):
        self.assertEqual(self.calculator.calculate("10 / (2 + 3) * 4 - 1"), 7)
        self.assertEqual(self.calculator.calculate("10 / (2 + 3) * (4 - 1)"), 6)

    def test_decimal_numbers(self):  # Test for float support
        self.assertEqual(self.calculator.calculate("2.5 + 3.5"), 6)
    
    def test_negative_numbers(self): #Test for negative support
        self.assertEqual(self.calculator.calculate("-2.5 + 3.5"), 1)
        self.assertEqual(self.calculator.calculate("2.5 + -3.5"), -1)
        self.assertEqual(self.calculator.calculate("-2.5 + -3.5"), -6)
        self.assertEqual(self.calculator.calculate("-2*-3"), 6) # test case for negative operations
        self.assertEqual(self.calculator.calculate("-2--3"), 1) # test case for negative operations

    def test_division_by_zero(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("5/0")
        self.assertEqual(str(context.exception), "Division by zero")

    def test_invalid_characters(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("2+a")
        self.assertEqual(str(context.exception), "Expression contains invalid characters.")

    def test_unbalanced_parentheses(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("(2+3")  # Unclosed parenthesis
        self.assertIn("Unbalanced parentheses", str(context.exception))

        with self.assertRaises(ValueError) as context:
              self.calculator.calculate("2+3)") # unOpened parenthesis
        self.assertIn("Unbalanced parentheses", str(context.exception))
    
    def test_invalid_expression(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("+ 2 3")   # starts with  operator without an operand
        self.assertEqual(str(context.exception), "Invalid Expression!")   
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("10 + + 5") # two operators without an operand
        self.assertEqual(str(context.exception), "Invalid Expression!")   
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("10 5")  # two operands. Operator expected
        self.assertEqual(str(context.exception), "Invalid Expression!")   

if __name__ == '__main__':
    unittest.main()
