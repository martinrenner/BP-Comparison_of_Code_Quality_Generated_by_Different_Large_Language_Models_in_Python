from typing import List, Dict, Tuple, Optional
import re


class Calculator:
    """
    A calculator class that evaluates arithmetic expressions.
    Supports addition, subtraction, multiplication, division, and parentheses.
    """
    
    def __init__(self):
        """Initialize the Calculator with operators and their precedence."""
        # Define operators and their precedence (higher value = higher precedence)
        self.operators: Dict[str, int] = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result.
        
        Args:
            expression (str): The arithmetic expression as a string
            
        Returns:
            float: The result of the evaluated expression
            
        Raises:
            ValueError: If the expression contains invalid characters or syntax
            ZeroDivisionError: If division by zero is attempted
            SyntaxError: If the expression has unbalanced parentheses
        """
        # Validate and normalize the expression
        processed_expression = self._normalize_expression(expression)
        
        # Check for balanced parentheses
        if not self._is_parentheses_balanced(processed_expression):
            raise SyntaxError("Unbalanced parentheses in the expression")
        
        # Tokenize the expression
        tokens = self._tokenize(processed_expression)
        
        # Convert to postfix notation and evaluate
        result = self._evaluate_postfix(self._infix_to_postfix(tokens))
        
        return result
    
    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression by removing spaces and validating characters.
        
        Args:
            expression (str): The arithmetic expression
            
        Returns:
            str: The normalized expression
            
        Raises:
            ValueError: If the expression contains invalid characters
        """
        # Remove all whitespace
        normalized = expression.replace(" ", "")
        
        # Validate characters
        allowed_chars = set("0123456789+-*/().eE")
        if not all(char in allowed_chars for char in normalized):
            raise ValueError("Expression contains invalid characters")
            
        # Check for empty expression
        if not normalized:
            raise ValueError("Expression cannot be empty")
        
        return normalized
    
    def _is_parentheses_balanced(self, expression: str) -> bool:
        """
        Checks if parentheses in the expression are balanced.
        
        Args:
            expression (str): The arithmetic expression
            
        Returns:
            bool: True if parentheses are balanced, False otherwise
        """
        stack = []
        
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
                
        return len(stack) == 0
    
    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts the expression string into a list of tokens.
        
        Args:
            expression (str): The normalized arithmetic expression
            
        Returns:
            List[str]: List of tokens representing numbers and operators
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Handle operators and parentheses
            if char in self.operators or char in '()':
                # Handle negative numbers at start or after operators/opening parenthesis
                if (char == '-' and (i == 0 or expression[i-1] in '(+*-/')):
                    # Look ahead to collect the negative number
                    num_str = char
                    i += 1
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        num_str += expression[i]
                        i += 1
                    tokens.append(num_str)
                else:
                    tokens.append(char)
                    i += 1
            # Handle numbers
            elif char.isdigit() or char == '.':
                num_str = ''
                # Collect all digits and decimal points
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.' or 
                                               expression[i] in 'eE' or
                                               (expression[i] in '+-' and i > 0 and expression[i-1] in 'eE')):
                    num_str += expression[i]
                    i += 1
                tokens.append(num_str)
            else:
                i += 1
                
        return tokens
    
    def _infix_to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Converts infix notation to postfix (Reverse Polish Notation).
        
        Args:
            tokens (List[str]): List of tokens in infix notation
            
        Returns:
            List[str]: List of tokens in postfix notation
        """
        output = []
        operator_stack = []
        
        for token in tokens:
            # If token is a number
            if token not in self.operators and token not in '()':
                output.append(token)
            # If token is an opening parenthesis
            elif token == '(':
                operator_stack.append(token)
            # If token is a closing parenthesis
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Discard the opening parenthesis
                else:
                    raise SyntaxError("Mismatched parentheses")
            # If token is an operator
            else:
                while (operator_stack and operator_stack[-1] != '(' and 
                       self.operators.get(operator_stack[-1], 0) >= self.operators.get(token, 0)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
        
        # Pop any remaining operators from the stack
        while operator_stack:
            if operator_stack[-1] == '(':
                raise SyntaxError("Mismatched parentheses")
            output.append(operator_stack.pop())
            
        return output
    
    def _evaluate_postfix(self, tokens: List[str]) -> float:
        """
        Evaluates a postfix expression.
        
        Args:
            tokens (List[str]): List of tokens in postfix notation
            
        Returns:
            float: Result of the evaluation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is invalid
        """
        if not tokens:
            raise ValueError("Empty expression")
            
        value_stack = []
        
        for token in tokens:
            # If token is a number
            if token not in self.operators:
                try:
                    value_stack.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid number format: {token}")
            # If token is an operator
            else:
                if len(value_stack) < 2:
                    raise ValueError("Invalid expression format")
                
                b = value_stack.pop()
                a = value_stack.pop()
                
                if token == '+':
                    value_stack.append(a + b)
                elif token == '-':
                    value_stack.append(a - b)
                elif token == '*':
                    value_stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero is not allowed")
                    value_stack.append(a / b)
        
        if len(value_stack) != 1:
            raise ValueError("Invalid expression format")
            
        return value_stack[0]


def main():
    calculator = Calculator()
    
    try:
        # Examples with different operations
        expressions = [
            "2 + 3",                     # Basic addition
            "5 - 3",                     # Basic subtraction
            "2 * 3",                     # Basic multiplication
            "6 / 3",                     # Basic division
            "2 + 3 * 4",                 # Operator precedence
            "(2 + 3) * 4",               # Parentheses
            "2 + 3 * (4 - 1)",           # Mixed operations
            "-5 + 3",                    # Negative numbers
            "2.5 * 3.5",                 # Floating point
            "1 / 0",                     # Division by zero (will raise error)
            "1e3 + 2",                   # Scientific notation
            "((2 + 3) * 4) / (1 + 1)"    # Nested parentheses
        ]
        
        for expr in expressions:
            try:
                result = calculator.calculate(expr)
                print(f"{expr} = {result}")
            except Exception as e:
                print(f"{expr} => Error: {str(e)}")
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
