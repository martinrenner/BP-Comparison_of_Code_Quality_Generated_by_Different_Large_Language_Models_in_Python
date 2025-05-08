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
            float: The result of the calculation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
        """
        normalized_expression = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expression):
            raise ValueError("Unbalanced parentheses in expression.")

        try:
            result = self._parse_expression(normalized_expression)
            return float(result)
        except ZeroDivisionError:
            raise ValueError("Division by zero encountered.")
        except (ValueError, TypeError) as e:  # improved specific error handling
            raise ValueError(f"Invalid expression: {e}")


    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression by removing spaces and validating characters.

        Args:
            expression (str): The mathematical expression.

        Returns:
            str: The normalized expression.

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
            expression (str): The mathematical expression.

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


    def _parse_expression(self, expression: str) -> float:
        """
        Parses the expression and evaluates it using the shunting yard algorithm.
        This implementation handles operator precedence and parentheses correctly.

        Args:
            expression: The mathematical expression (normalized).

        Returns:
            The result of the evaluation.
        
        Raises:
            ValueError: If there's an issue in parsing (e.g. empty expression)

        """

        if not expression:
           raise ValueError("Expression is empty during parsing.")

        tokens = re.findall(r"(\b\d+\.?\d*\b|[()+*/-])", expression)  # Tokenize

        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if re.match(r"\b\d+\.?\d*\b", token):  # Number
                output_queue.append(float(token))
            elif token in precedence:  # Operator
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':  # Left parenthesis
                operator_stack.append(token)
            elif token == ')':  # Right parenthesis
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack: # Check empty stack, throw error if no opening parenthesis
                    raise ValueError("Mismatched parentheses.")
                operator_stack.pop()  # Pop the '('

        while operator_stack:
            if operator_stack[-1] == '(': # Check if '(' still existing, then throw error
               raise ValueError("Mismatched parentheses.")            
            output_queue.append(operator_stack.pop())


        # Evaluate RPN
        stack = []
        for token in output_queue:
            if isinstance(token, float):
                stack.append(token)
            else:  # Operator
                if len(stack) < 2:
                    raise ValueError("Invalid expression format (not enough operands).")
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
                        raise ZeroDivisionError  # Explicitly handle division by zero
                    stack.append(operand1 / operand2)

        if len(stack) != 1:
             raise ValueError("Invalid expression format (too many operands).")       

        return stack.pop()


from calculator import Calculator # assuming you saved as calculator.py

calc = Calculator()

# Valid expressions
print(calc.calculate("1 + 2 * 3"))          # Output: 7.0
print(calc.calculate("(1 + 2) * 3"))        # Output: 9.0
print(calc.calculate("10 / (2 + 3)"))       # Output: 2.0
print(calc.calculate("-5 + 2.5 * 4"))     # Output: 5.0
print(calc.calculate("10.5 - 2 * 3.14"))   # Output: 4.22
print(calc.calculate("5"))                  # Output: 5.0
print(calc.calculate("2*(1+3)"))          # Output: 8.0

# Invalid expressions (will raise ValueErrors)

try:
    print(calc.calculate("1 + (2 * 3"))      # Unbalanced parentheses
except ValueError as e:
    print(e)

try:
    print(calc.calculate("1 + a * 3"))      # Invalid character
except ValueError as e:
    print(e)
    
try:
    print(calc.calculate("10 / 0"))         # Division by zero
except ValueError as e:
    print(e)
    
try:
    print(calc.calculate("(1+1"))   # missing closing )
except ValueError as e:
print(e)

try:
    print(calc.calculate("+1+1"))       # missing operand
except ValueError as e:
    print(e)
    
try:
    print(calc.calculate("1 1"))       # missing operator
except ValueError as e:
    print(e)
    
try:
    print(calc.calculate(""))       # blank
except ValueError as e:
    print(e)
