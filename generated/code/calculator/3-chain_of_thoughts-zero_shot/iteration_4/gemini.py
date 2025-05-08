import re  # Importing the regular expression module

class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions
    according to the order of operations, supporting parentheses and
    basic arithmetic operations (+, -, *, /).

    This class adheres to ISO/IEC 25010 standards for software quality,
    focusing on functionality, reliability, usability, efficiency,
    maintainability, and portability.

    Methods:
        calculate(expression: str) -> float: Evaluates the expression string.
    """

    def __init__(self):
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2}  # Operator precedence


    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the input expression into a list of numbers, operators.

        Splits the expression string into tokens using regular expressions.

        Args:
            expression (str): The expression string.

        Returns:
            list: A list of tokens (numbers, operators, and parentheses).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        tokens = re.findall(r"(\b\d+\.?\d*\b|\+|\-|\*|\/|\(|\)|\^-?\d+\.?\d*)", expression)
        if not all(re.match(r"^(-?\d+\.?\d*|\+|\-|\*|\/|\(|\))$", token) for token in tokens):
            raise ValueError("Invalid characters in expression.")

        # Fix for handling negative numbers at different positions(beginning, after operator, in parenthesis)
        processed_tokens = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '-' and (i == 0 or tokens[i-1] in '+-*/('):
                # Negative number case
                if i + 1 < len(tokens) and re.match(r"^\d+\.?\d*$", tokens[i+1]):
                    processed_tokens.append(str(-float(tokens[i+1])))  # Combine '-' and the number
                    i += 2  # Skip the next token (the number)
                    continue
                else:
                  raise ValueError("Invalid use of '-' operator")
            processed_tokens.append(token)
            i += 1
        return processed_tokens


    def _infix_to_postfix(self, tokens: list) -> list:
      """Converts an infix expression (tokenized) to postfix (RPN)."""
      output = []
      operator_stack = []

      for token in tokens:
          if re.match(r"^-?\d+\.?\d*$", token):  # Is it a number?
              output.append(float(token))
          elif token in self.precedence:  # Is it an operator?
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
                  raise ValueError("Unbalanced parentheses (missing '(').")
          else:
                raise ValueError(f"Internal error: invalid token '{token}' during conversion.")

      while operator_stack:
          if operator_stack[-1] == '(':
              raise ValueError("Unbalanced parentheses (missing ')').")
          output.append(operator_stack.pop())
      return output

    def _evaluate_postfix(self, tokens: list) -> float:
      """Evaluates a postfix expression (represented as a list of tokens)."""
      stack = []

      for token in tokens:
          if isinstance(token, float):
            stack.append(token)
          else:  # It's an operator
              try:
                  operand2 = stack.pop()
                  operand1 = stack.pop()
              except IndexError:
                  raise ValueError("Invalid expression format (not enough operands).")

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
              else: #should never occur
                  raise ValueError(f"Internal error: invalid token '{token}' during evaluation.")

      if len(stack) != 1:
          raise ValueError("Invalid expression format (too many operands).") # Example: 2 3 5 + *  is too many
      return stack[0]



    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression.

        Args:
            expression (str): The arithmetic expression string.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                parentheses, invalid characters).
            ZeroDivisionError: If the expression attempts division by zero.
        """
        try:
            tokens = self._tokenize(expression)
            postfix_tokens = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except (ValueError, ZeroDivisionError, IndexError) as e:  # Catch specific exceptions
            raise  # Re-raise the exception to be handled by the caller

# --- Example Usage and Testing ---

if __name__ == "__main__":
    calculator = Calculator()

    test_cases = [
      ("1 + 1", 2.0),
      ("2 * (3 + 4)", 14.0),
      ("10 / (2 + 3)", 2.0),
      ("1 - 2 * 3", -5.0),
      ("(1 + 2) * (3 - 4) / 5", -0.6),
      ("10 + 2 * (6 - (4 + 1) / 3) + 7", 29.666666666666668),
      ("-5 + 3", -2.0),
      ("-(5 + 3)", -8.0),
      ("(-5 + 3) * 2", -4.0),
      ("2 * -3", -6.0),
      ("(-2) * (-3)", 6.0),
      ("1.5 + 2.5 * 3", 9.0),
      ("10 / 0", ZeroDivisionError),         # Division by zero
      ("(1 + 2", ValueError),            # Unbalanced parentheses
      ("1 ++ 2", ValueError),            # Invalid operator sequence
      ("1 + a", ValueError),              # Invalid character
      ("2 * (3 + 4", ValueError),         # Unbalanced parentheses
    ]

    for expression, expected in test_cases:
        try:
            result = calculator.calculate(expression)
            if isinstance(expected, type) and issubclass(expected, Exception):
              print(f"TEST FAILED: '{expression}' - Expected exception {expected}, got {result}")

            elif abs(result - expected) < 1e-6:
                print(f"TEST PASSED: '{expression}' = {result}")
            else:
                print(f"TEST FAILED: '{expression}' - Expected {expected}, got {result}")

        except Exception as e:
            if isinstance(expected, type) and issubclass(expected, Exception):
                if isinstance(e, expected):
                    print(f"TEST PASSED (exception): '{expression}' - Exception: {e}")
                else:
                     print(f"TEST FAILED (exception type): '{expression}' - Expected {expected}, got : {e}")
            else:
                 print(f"TEST FAILED (exception): '{expression}' - Got unexpected exception: {e}")



    # Interactive Console Loop
    print("\nArithmetic Calculator (Enter 'quit' to exit)")
    while True:
        expression = input("Enter expression: ")
        if expression.lower() == 'quit':
            break
        try:
            result = calculator.calculate(expression)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
