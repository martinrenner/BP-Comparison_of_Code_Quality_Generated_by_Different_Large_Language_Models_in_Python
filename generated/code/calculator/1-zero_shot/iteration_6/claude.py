"""
Arithmetic Expression Calculator

This module provides a Calculator class for evaluating arithmetic expressions
with support for basic operations, parentheses, and proper operator precedence.
"""
from typing import List, Union, Tuple
import re


class Calculator:
    """
    A class that evaluates arithmetic expressions.
    
    Supports addition, subtraction, multiplication, division, and parentheses
    with correct operator precedence. Handles both integers and floating-point numbers.
    """
    
    def __init__(self):
        """Initialize the Calculator object."""
        # Define the valid tokens in expressions
        self.NUMBER_PATTERN = r'-?\d+(\.\d+)?'
        self.OPERATORS = {'+', '-', '*', '/'}
        self.PARENTHESES = {'(', ')'}
        
    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return the result.
        
        Args:
            expression: A string containing an arithmetic expression
            
        Returns:
            The numerical result of evaluating the expression
            
        Raises:
            ValueError: If the expression contains invalid characters or syntax
            ZeroDivisionError: If division by zero is attempted
            ArithmeticError: For other arithmetic errors
        """
        # Remove all whitespace from the expression
        expression = expression.replace(' ', '')
        
        if not expression:
            raise ValueError("Empty expression")
            
        # Validate the expression
        self._validate_expression(expression)
        
        # Tokenize and parse the expression
        tokens = self._tokenize(expression)
        
        # Evaluate the expression using a recursive descent parser
        result, _ = self._parse_expression(tokens, 0)
        return result
    
    def _validate_expression(self, expression: str) -> None:
        """
        Validate the expression for syntax errors.
        
        Args:
            expression: The arithmetic expression to validate
            
        Raises:
            ValueError: If the expression contains invalid characters or syntax
        """
        # Check for balanced parentheses
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise ValueError("Unbalanced parentheses: too many closing parentheses")
                stack.pop()
        
        if stack:
            raise ValueError("Unbalanced parentheses: missing closing parentheses")
        
        # Check for valid characters
        valid_chars = set('0123456789.+-*/()') 
        for char in expression:
            if char not in valid_chars:
                raise ValueError(f"Invalid character: '{char}'")
        
        # Check for consecutive operators
        for op in self.OPERATORS:
            if op*2 in expression:
                raise ValueError(f"Invalid syntax: consecutive operators '{op}{op}'")
                
        # Check for invalid decimal points
        if re.search(r'\d*\.\d*\.', expression):
            raise ValueError("Invalid number format: multiple decimal points")
            
    def _tokenize(self, expression: str) -> List[str]:
        """
        Convert an expression string into a list of tokens.
        
        Args:
            expression: The expression to tokenize
            
        Returns:
            A list of tokens (numbers and operators)
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Handle numbers (including decimals and leading minus signs)
            if char.isdigit() or (char == '-' and (i == 0 or expression[i-1] in self.OPERATORS or expression[i-1] == '(')):
                # Find the complete number
                j = i
                if char == '-':
                    j += 1
                
                # Get the integer part
                while j < len(expression) and expression[j].isdigit():
                    j += 1
                
                # Check for decimal part
                if j < len(expression) and expression[j] == '.':
                    j += 1
                    while j < len(expression) and expression[j].isdigit():
                        j += 1
                
                tokens.append(expression[i:j])
                i = j
            # Handle operators and parentheses
            elif char in self.OPERATORS or char in self.PARENTHESES:
                tokens.append(char)
                i += 1
            else:
                i += 1
        
        return tokens
    
    def _parse_expression(self, tokens: List[str], start_pos: int) -> Tuple[float, int]:
        """
        Recursively parse an expression following operator precedence.
        
        Args:
            tokens: List of tokens to parse
            start_pos: Starting position in the token list
            
        Returns:
            (result, new_position): The result of the expression and the new position
        """
        return self._parse_addition_subtraction(tokens, start_pos)
    
    def _parse_addition_subtraction(self, tokens: List[str], pos: int) -> Tuple[float, int]:
        """
        Parse addition and subtraction operations.
        
        Args:
            tokens: List of tokens to parse
            pos: Current position in the token list
            
        Returns:
            (result, new_position): The result of the expression and the new position
        """
        left, pos = self._parse_multiplication_division(tokens, pos)
        
        while pos < len(tokens) and tokens[pos] in {'+', '-'}:
            op = tokens[pos]
            right, pos = self._parse_multiplication_division(tokens, pos + 1)
            
            if op == '+':
                left += right
            else:  # op == '-'
                left -= right
        
        return left, pos
    
    def _parse_multiplication_division(self, tokens: List[str], pos: int) -> Tuple[float, int]:
        """
        Parse multiplication and division operations.
        
        Args:
            tokens: List of tokens to parse
            pos: Current position in the token list
            
        Returns:
            (result, new_position): The result of the expression and the new position
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
        """
        left, pos = self._parse_factor(tokens, pos)
        
        while pos < len(tokens) and tokens[pos] in {'*', '/'}:
            op = tokens[pos]
            right, pos = self._parse_factor(tokens, pos + 1)
            
            if op == '*':
                left *= right
            else:  # op == '/'
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                left /= right
        
        return left, pos
    
    def _parse_factor(self, tokens: List[str], pos: int) -> Tuple[float, int]:
        """
        Parse a factor (number or parenthesized expression).
        
        Args:
            tokens: List of tokens to parse
            pos: Current position in the token list
            
        Returns:
            (result, new_position): The value of the factor and the new position
            
        Raises:
            ValueError: If the expression has invalid syntax
        """
        if pos >= len(tokens):
            raise ValueError("Unexpected end of expression")
            
        token = tokens[pos]
        
        # Handle parenthesized expression
        if token == '(':
            result, pos = self._parse_expression(tokens, pos + 1)
            
            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError("Missing closing parenthesis")
            
            return result, pos + 1
            
        # Handle numbers
        elif re.match(self.NUMBER_PATTERN, token):
            return float(token), pos + 1
            
        raise ValueError(f"Unexpected token: {token}")


def main():
    """
    Main function to run the calculator as a command-line application.
    """
    calculator = Calculator()
    
    print("Console Calculator - Type 'exit' to quit")
    print("Supported operations: +, -, *, / and parentheses")
    
    while True:
        try:
            expression = input("\nEnter expression: ")
            
            if expression.lower() == 'exit':
                print("Calculator exiting. Goodbye!")
                break
                
            result = calculator.calculate(expression)
            
            # Format the result - show as integer if it's a whole number
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except (ValueError, ZeroDivisionError, ArithmeticError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nCalculator interrupted. Exiting...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
