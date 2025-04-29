"""
Arithmetic Expression Calculator

This module provides a calculator that evaluates arithmetic expressions
following standard operator precedence rules.

Features:
- Supports addition, subtraction, multiplication, and division
- Handles parentheses for expression grouping
- Processes integers and floating-point numbers (including negative values)
- Validates input expressions and throws appropriate errors
"""

import re
from typing import List, Union, Tuple


class Calculator:
    """
    A class that evaluates arithmetic expressions with proper operator precedence.
    
    This calculator handles basic arithmetic operations (+, -, *, /), 
    parentheses, and both integers and floating-point numbers.
    """
    
    def __init__(self):
        """Initialize the Calculator object."""
        # Define the valid tokens for the calculator
        self.number_pattern = r'-?\d+(\.\d+)?'
        self.operator_pattern = r'[\+\-\*/\(\)]'
        self.token_pattern = f'({self.number_pattern}|{self.operator_pattern})'
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return the result.
        
        Args:
            expression: A string containing the arithmetic expression to evaluate
            
        Returns:
            The numerical result of the expression evaluation
            
        Raises:
            ValueError: If the expression contains invalid characters or syntax
            ZeroDivisionError: If the expression attempts to divide by zero
            SyntaxError: If the expression has unbalanced parentheses or invalid structure
        """
        # Validate and tokenize the input expression
        tokens = self._tokenize(expression)
        
        # Parse and evaluate the tokens
        result = self._parse_expression(tokens)
        
        return result
    
    def _tokenize(self, expression: str) -> List[str]:
        """
        Convert an expression string into a list of tokens.
        
        Args:
            expression: The input expression string
            
        Returns:
            A list of tokens (numbers and operators)
            
        Raises:
            ValueError: If the expression contains invalid characters
        """
        # Remove all whitespace from the expression
        expression = expression.replace(' ', '')
        
        # If expression is empty, raise error
        if not expression:
            raise ValueError("Expression cannot be empty")
        
        # Find all valid tokens in the expression
        tokens = re.findall(self.token_pattern, expression)
        tokens = [t[0] for t in tokens]  # Extract the matched groups
        
        # Check if we successfully tokenized the entire expression
        joined_tokens = ''.join(tokens)
        if joined_tokens != expression:
            invalid_chars = set(expression) - set(joined_tokens)
            if invalid_chars:
                raise ValueError(f"Invalid characters in expression: {invalid_chars}")
            raise ValueError("Invalid expression format")
            
        # Check for balanced parentheses
        self._check_balanced_parentheses(tokens)
        
        # Check for invalid token sequences
        self._validate_token_sequence(tokens)
        
        return tokens
    
    def _check_balanced_parentheses(self, tokens: List[str]) -> None:
        """
        Verify that parentheses in the token list are balanced.
        
        Args:
            tokens: The list of tokens to check
            
        Raises:
            SyntaxError: If parentheses are unbalanced
        """
        stack = []
        for token in tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                if not stack:
                    raise SyntaxError("Unbalanced parentheses: too many closing parentheses")
                stack.pop()
        
        if stack:
            raise SyntaxError("Unbalanced parentheses: missing closing parentheses")
    
    def _validate_token_sequence(self, tokens: List[str]) -> None:
        """
        Check for invalid sequences of tokens in the expression.
        
        Args:
            tokens: The list of tokens to validate
            
        Raises:
            SyntaxError: If the token sequence is invalid
        """
        operators = set(['+', '-', '*', '/'])
        
        # Check for empty expression within parentheses
        for i in range(len(tokens) - 1):
            if tokens[i] == '(' and tokens[i + 1] == ')':
                raise SyntaxError("Empty parentheses are not allowed")
        
        # Check for invalid operator sequences
        for i in range(len(tokens)):
            # Operators can't be at the beginning, except minus for negative numbers
            if i == 0 and tokens[i] in operators and tokens[i] != '-':
                raise SyntaxError(f"Expression cannot start with operator '{tokens[i]}'")
            
            # Operators can't be at the end
            if i == len(tokens) - 1 and tokens[i] in operators:
                raise SyntaxError(f"Expression cannot end with operator '{tokens[i]}'")
            
            # Two consecutive operators are invalid (except when using parentheses or negative numbers)
            if i > 0 and tokens[i] in operators and tokens[i] != '-' and tokens[i-1] in operators:
                if tokens[i-1] != ')':
                    raise SyntaxError(f"Invalid operator sequence: '{tokens[i-1]}{tokens[i]}'")
            
            # Check special case for negative numbers
            if tokens[i] == '-' and i > 0:
                if tokens[i-1] in operators and tokens[i-1] != ')':
                    # Check if this might be a negative number
                    if i+1 < len(tokens) and re.match(self.number_pattern, tokens[i+1]):
                        # This is likely a negative number, so combine with the next token
                        continue
                    else:
                        raise SyntaxError(f"Invalid operator sequence: '{tokens[i-1]}{tokens[i]}'")
        
    def _parse_expression(self, tokens: List[str]) -> float:
        """
        Parse and evaluate an expression from a list of tokens.
        
        Args:
            tokens: The list of tokens to evaluate
            
        Returns:
            The result of evaluating the expression
            
        Raises:
            Various exceptions based on calculation errors
        """
        pos = [0]  # Using list to allow modification in nested functions
        
        def parse_expression() -> float:
            """Parse and evaluate an expression."""
            left = parse_term()
            
            while pos[0] < len(tokens) and tokens[pos[0]] in ['+', '-']:
                op = tokens[pos[0]]
                pos[0] += 1
                right = parse_term()
                
                if op == '+':
                    left += right
                else:  # op == '-'
                    left -= right
                    
            return left
        
        def parse_term() -> float:
            """Parse and evaluate a term."""
            left = parse_factor()
            
            while pos[0] < len(tokens) and tokens[pos[0]] in ['*', '/']:
                op = tokens[pos[0]]
                pos[0] += 1
                right = parse_factor()
                
                if op == '*':
                    left *= right
                else:  # op == '/'
                    if right == 0:
                        raise ZeroDivisionError("Division by zero is not allowed")
                    left /= right
                    
            return left
        
        def parse_factor() -> float:
            """Parse and evaluate a factor."""
            token = tokens[pos[0]]
            pos[0] += 1
            
            if token == '(':
                result = parse_expression()
                if pos[0] >= len(tokens) or tokens[pos[0]] != ')':
                    raise SyntaxError("Missing closing parenthesis")
                pos[0] += 1  # Skip over the closing parenthesis
                return result
            
            # Handle numeric values
            if re.match(self.number_pattern, token):
                return float(token)
            
            # If we reached here, it's an unexpected token
            raise SyntaxError(f"Unexpected token: {token}")
        
        # Start parsing the expression
        result = parse_expression()
        
        # If we haven't consumed all tokens, there might be extra content
        if pos[0] < len(tokens):
            raise SyntaxError(f"Unexpected token at position {pos[0]}: {tokens[pos[0]]}")
        
        return result


def main():
    """Main function to run the calculator from command line."""
    calculator = Calculator()
    print("Console Arithmetic Calculator")
    print("Enter 'q' or 'quit' to exit")
    print("Examples: 2+3*4, (5+3)*2, 10/2-3")
    
    while True:
        try:
            expression = input("\nEnter an expression: ")
            if expression.lower() in ['q', 'quit', 'exit']:
                break
                
            result = calculator.calculate(expression)
            
            # Display integer result without decimal if it's a whole number
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except (ValueError, ZeroDivisionError, SyntaxError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
