"""
Console-based Arithmetic Calculator

This module implements a calculator that evaluates arithmetic expressions
following proper operator precedence and supporting parentheses.

Author: AI Assistant
Version: 1.0
"""
from typing import List, Union, Tuple
import re


class Calculator:
    """
    A calculator class that evaluates arithmetic expressions.
    
    This class implements a calculator that can evaluate expressions with:
    - Addition, subtraction, multiplication, and division
    - Parentheses for grouping
    - Negative numbers
    - Integer and floating-point values
    """
    
    def __init__(self):
        """Initialize the Calculator object."""
        # Define the supported operators and their precedence
        self.operators = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate the given arithmetic expression and return the result.
        
        Args:
            expression (str): The arithmetic expression to evaluate.
            
        Returns:
            float: The result of the expression evaluation.
            
        Raises:
            ValueError: If the expression is invalid or contains syntax errors.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        # Validate and sanitize the input
        expression = self._sanitize_expression(expression)
        
        # Tokenize the expression
        tokens = self._tokenize(expression)
        
        # Convert to postfix notation (Reverse Polish Notation)
        postfix = self._infix_to_postfix(tokens)
        
        # Evaluate the postfix expression
        return self._evaluate_postfix(postfix)
    
    def _sanitize_expression(self, expression: str) -> str:
        """
        Validate and clean the input expression.
        
        Args:
            expression (str): The raw expression.
            
        Returns:
            str: The sanitized expression.
            
        Raises:
            ValueError: If the expression contains invalid characters or has unbalanced parentheses.
        """
        # Check if the expression is empty
        if not expression or expression.isspace():
            raise ValueError("Expression cannot be empty")
        
        # Remove all whitespace
        expression = expression.replace(" ", "")
        
        # Check for invalid characters
        valid_chars = set("0123456789.+-*/() ")
        if any(char not in valid_chars for char in expression):
            raise ValueError("Expression contains invalid characters")
        
        # Check for balanced parentheses
        if not self._check_balanced_parentheses(expression):
            raise ValueError("Expression has unbalanced parentheses")
        
        return expression
    
    def _check_balanced_parentheses(self, expression: str) -> bool:
        """
        Check if parentheses in the expression are balanced.
        
        Args:
            expression (str): The expression to check.
            
        Returns:
            bool: True if parentheses are balanced, False otherwise.
        """
        stack = []
        
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack or stack.pop() != '(':
                    return False
        
        return len(stack) == 0
    
    def _tokenize(self, expression: str) -> List[Union[float, str]]:
        """
        Convert the expression string into a list of tokens.
        
        Args:
            expression (str): The expression to tokenize.
            
        Returns:
            List[Union[float, str]]: List of tokens (numbers and operators).
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Handle numbers (including decimals)
            if char.isdigit() or (char == '.' and i + 1 < len(expression) and expression[i + 1].isdigit()):
                # Find the end of the number
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                
                # Convert the number string to float
                try:
                    number = float(expression[i:j])
                    # Convert to int if it's an integer value to display cleaner
                    tokens.append(int(number) if number.is_integer() else number)
                except ValueError:
                    raise ValueError(f"Invalid number format: {expression[i:j]}")
                
                i = j
            # Handle operators and parentheses
            elif char in self.operators or char in "()":
                # Handle negative numbers (unary minus)
                if char == '-' and (i == 0 or expression[i-1] in '(+-*/'):
                    # Look ahead to find the number after the unary minus
                    j = i + 1
                    while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                        j += 1
                    
                    if j > i + 1:  # There is a number after the unary minus
                        try:
                            number = -float(expression[i+1:j])
                            # Convert to int if it's an integer value
                            tokens.append(int(number) if number.is_integer() else number)
                        except ValueError:
                            raise ValueError(f"Invalid number format: -{expression[i+1:j]}")
                        
                        i = j
                    else:
                        tokens.append(char)
                        i += 1
                else:
                    tokens.append(char)
                    i += 1
            else:
                i += 1
        
        return tokens
    
    def _infix_to_postfix(self, tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Convert infix notation tokens to postfix notation (RPN).
        
        Args:
            tokens (List[Union[float, str]]): Tokens in infix notation.
            
        Returns:
            List[Union[float, str]]: Tokens in postfix notation.
        """
        output = []
        operator_stack = []
        
        for token in tokens:
            # If token is a number, add to output
            if isinstance(token, (int, float)):
                output.append(token)
            
            # If token is an opening parenthesis, push to stack
            elif token == '(':
                operator_stack.append(token)
            
            # If token is a closing parenthesis, pop operators until matching opening parenthesis
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                
                # Pop the opening parenthesis
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
                else:
                    raise ValueError("Mismatched parentheses")
            
            # If token is an operator
            elif token in self.operators:
                while (operator_stack and 
                       operator_stack[-1] != '(' and 
                       self.operators.get(operator_stack[-1], 0) >= self.operators.get(token, 0)):
                    output.append(operator_stack.pop())
                
                operator_stack.append(token)
        
        # Pop any remaining operators from the stack to the output
        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, tokens: List[Union[float, str]]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            tokens (List[Union[float, str]]): Tokens in postfix notation.
            
        Returns:
            float: The result of the expression.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ValueError: If the expression is invalid.
        """
        if not tokens:
            raise ValueError("Empty expression")
            
        operand_stack = []
        
        for token in tokens:
            # If token is a number, push to stack
            if isinstance(token, (int, float)):
                operand_stack.append(token)
            
            # If token is an operator, pop operands and apply operator
            elif token in self.operators:
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                
                # Pop operands (note the order)
                b = operand_stack.pop()
                a = operand_stack.pop()
                
                # Apply operator
                if token == '+':
                    operand_stack.append(a + b)
                elif token == '-':
                    operand_stack.append(a - b)
                elif token == '*':
                    operand_stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    operand_stack.append(a / b)
        
        # The final result should be the only item on the stack
        if len(operand_stack) != 1:
            raise ValueError("Invalid expression: too many operands")
        
        return operand_stack[0]


def main():
    """
    Main function to run the calculator as a console application.
    """
    calculator = Calculator()
    
    print("Console-based Arithmetic Calculator")
    print("Enter 'q' or 'quit' to exit")
    print("Examples: 2+2, 3*(4+5), 10/2")
    print()
    
    while True:
        try:
            expression = input("Enter an expression: ")
            
            if expression.lower() in ('q', 'quit', 'exit'):
                break
                
            result = calculator.calculate(expression)
            
            # Display as integer if the result is a whole number
            if isinstance(result, float) and result.is_integer():
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            
        print()  # Empty line for better readability

if __name__ == "__main__":
    main()
