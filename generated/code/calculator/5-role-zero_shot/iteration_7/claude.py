"""
Calculator Module - A console-based arithmetic calculator.

This module provides a Calculator class that can evaluate arithmetic expressions
with support for addition, subtraction, multiplication, division, and parentheses
while maintaining proper operator precedence.
"""
from typing import List, Tuple, Union, Optional
import re


class Calculator:
    """
    A calculator class that evaluates arithmetic expressions.
    
    This class implements a calculator that can evaluate string expressions
    containing basic arithmetic operations (addition, subtraction, 
    multiplication, division) with proper operator precedence and support
    for parentheses.
    """
    
    def __init__(self):
        """Initialize the Calculator instance."""
        self._operators = {
            '+': (1, lambda x, y: x + y),
            '-': (1, lambda x, y: x - y),
            '*': (2, lambda x, y: x * y),
            '/': (2, lambda x, y: x / y)
        }
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return the result.
        
        Args:
            expression (str): A string containing an arithmetic expression.
                Supports +, -, *, / operators, parentheses, and negative numbers.
        
        Returns:
            float: The result of the evaluated expression.
        
        Raises:
            ValueError: If the expression has invalid syntax, unbalanced parentheses,
                       or contains invalid characters.
            ZeroDivisionError: If the expression attempts division by zero.
            ArithmeticError: For other arithmetic-related errors.
        """
        # Validate and sanitize the input
        self._validate_expression(expression)
        
        # Tokenize the expression
        tokens = self._tokenize(expression)
        
        # Evaluate the expression using shunting yard algorithm
        return self._evaluate_expression(tokens)
    
    def _validate_expression(self, expression: str) -> None:
        """
        Validate the input expression for syntax errors.
        
        Args:
            expression (str): The expression to validate.
            
        Raises:
            ValueError: If the expression is invalid.
        """
        if not expression or expression.isspace():
            raise ValueError("Expression cannot be empty")
        
        # Check for balanced parentheses
        open_count = 0
        for char in expression:
            if char == '(':
                open_count += 1
            elif char == ')':
                open_count -= 1
                if open_count < 0:
                    raise ValueError("Unbalanced parentheses: too many closing parentheses")
        
        if open_count > 0:
            raise ValueError("Unbalanced parentheses: missing closing parentheses")
        
        # Check for valid characters
        valid_char_pattern = r'^[\d\s\+\-\*\/\(\)\.]+$'
        if not re.match(valid_char_pattern, expression):
            raise ValueError("Expression contains invalid characters")
        
        # Check for invalid operator sequences like "++", "*/", etc.
        invalid_sequences = ['++', '--', '**', '//', '+-', '-+', '*+', '/+', 
                             '*-', '/-', '+*', '-*', '+/', '-/', '()', '(*', 
                             '(/', '(+', '(-', '*)', '/)', '+)', '-)', '*/']
                             
        for seq in invalid_sequences:
            if seq in expression:
                # Special case for negative numbers after operators or at beginning
                if seq in ['-+', '--', '*-', '/-', '(-'] and seq != expression.strip():
                    continue
                raise ValueError(f"Invalid operator sequence: {seq}")
    
    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Convert an expression string into a list of tokens.
        
        Args:
            expression (str): The expression to tokenize.
            
        Returns:
            list: A list of tokens (numbers and operators).
        """
        # Replace spaces for easier parsing
        expression = expression.replace(' ', '')
        
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # Handle numbers (including decimal points)
            if char.isdigit() or (char == '.' and i + 1 < len(expression) and expression[i + 1].isdigit()):
                # Find the complete number
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                try:
                    tokens.append(float(expression[i:j]))
                except ValueError:
                    raise ValueError(f"Invalid number format: {expression[i:j]}")
                i = j
                continue
            
            # Handle operators and parentheses
            if char in self._operators or char in '()':
                # Handle negative numbers
                if char == '-' and (i == 0 or expression[i-1] in '(+-*/'):
                    # This is a negative number, not a subtraction
                    j = i + 1
                    while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                        j += 1
                    if j > i + 1:  # Ensure there's at least one digit after the minus sign
                        try:
                            tokens.append(-float(expression[i+1:j]))
                            i = j
                            continue
                        except ValueError:
                            raise ValueError(f"Invalid number format: -{expression[i+1:j]}")
                
                tokens.append(char)
                i += 1
                continue
            
            # If we reach here, we've encountered an invalid character
            raise ValueError(f"Invalid character in expression: {char}")
        
        return tokens
    
    def _evaluate_expression(self, tokens: List[Union[float, str]]) -> float:
        """
        Evaluate the expression using the Shunting Yard algorithm.
        
        Args:
            tokens (list): A list of tokens (numbers and operators).
            
        Returns:
            float: The result of the expression.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ArithmeticError: For other arithmetic errors.
        """
        # Output queue for the final expression in RPN
        output_queue: List[float] = []
        
        # Operator stack
        operator_stack: List[str] = []
        
        for token in tokens:
            # If the token is a number, add it to the output queue
            if isinstance(token, (int, float)):
                output_queue.append(token)
            # If the token is an operator
            elif token in self._operators:
                while (operator_stack and operator_stack[-1] != '(' and 
                       (self._operators.get(operator_stack[-1], (0, None))[0] >= 
                        self._operators.get(token, (0, None))[0])):
                    self._apply_operator(output_queue, operator_stack.pop())
                operator_stack.append(token)
            # If the token is a left parenthesis, push it onto the stack
            elif token == '(':
                operator_stack.append(token)
            # If the token is a right parenthesis, process operators until matching left parenthesis
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    self._apply_operator(output_queue, operator_stack.pop())
                    
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Remove the left parenthesis
                else:
                    raise ValueError("Mismatched parentheses")
        
        # Process any remaining operators
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses")
            self._apply_operator(output_queue, op)
        
        # The result should be the only item left in the output queue
        if len(output_queue) != 1:
            raise ValueError("Invalid expression syntax")
            
        return output_queue[0]
    
    def _apply_operator(self, output_queue: List[float], operator: str) -> None:
        """
        Apply an operator to the top values in the output queue.
        
        Args:
            output_queue (list): The output queue of numbers.
            operator (str): The operator to apply.
            
        Raises:
            ValueError: If there are not enough operands for the operator.
            ZeroDivisionError: If division by zero is attempted.
        """
        if len(output_queue) < 2:
            raise ValueError(f"Not enough operands for operator: {operator}")
        
        # Pop the top two values from the stack
        b = output_queue.pop()
        a = output_queue.pop()
        
        # Apply the operator
        _, operation = self._operators[operator]
        
        try:
            if operator == '/' and b == 0:
                raise ZeroDivisionError("Division by zero")
            result = operation(a, b)
            output_queue.append(result)
        except (ArithmeticError, ZeroDivisionError) as e:
            raise e
        except Exception as e:
            raise ArithmeticError(f"Error applying operator {operator}: {e}")


def main():
    """
    Main function to demonstrate the calculator functionality.
    """
    calculator = Calculator()
    
    print("Console-based Arithmetic Calculator")
    print("Type 'exit' to quit")
    print("Supported operations: +, -, *, / and parentheses ()")
    
    while True:
        try:
            expression = input("\nEnter an expression: ")
            if expression.lower() == 'exit':
                break
                
            result = calculator.calculate(expression)
            
            # Check if the result is an integer
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
