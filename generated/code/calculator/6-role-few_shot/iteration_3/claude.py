from typing import List, Union, Optional
import re
from enum import Enum


class TokenType(Enum):
    """Enum representing different types of tokens in an arithmetic expression."""
    NUMBER = 'NUMBER'
    OPERATOR = 'OPERATOR'
    LEFT_PAREN = 'LEFT_PAREN'
    RIGHT_PAREN = 'RIGHT_PAREN'


class Token:
    """Class representing a token in an arithmetic expression."""
    
    def __init__(self, token_type: TokenType, value: Optional[Union[float, str]] = None):
        """
        Initialize a token with a type and optional value.
        
        Args:
            token_type (TokenType): The type of the token.
            value (Optional[Union[float, str]]): The value of the token if applicable.
        """
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        """Return a string representation of the token."""
        return f"Token({self.type}, {self.value})"


class Calculator:
    """
    A calculator class that evaluates arithmetic expressions.
    Supports addition, subtraction, multiplication, division and parentheses.
    """
    
    def __init__(self):
        """Initialize the calculator with operator precedence."""
        self.operators = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression.
        
        Args:
            expression (str): The arithmetic expression to evaluate.
            
        Returns:
            float: The result of the expression.
            
        Raises:
            ValueError: If the expression contains invalid characters or is malformed.
            ZeroDivisionError: If the expression involves division by zero.
            SyntaxError: If the expression has unbalanced parentheses or other syntax errors.
        """
        # Validate and normalize the expression
        normalized_expr = self._normalize_expression(expression)
        
        # Tokenize the expression
        tokens = self._tokenize(normalized_expr)
        
        # Convert infix notation to postfix (Reverse Polish Notation)
        postfix = self._infix_to_postfix(tokens)
        
        # Evaluate the postfix expression
        return self._evaluate_postfix(postfix)
    
    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes an expression by removing spaces and validating characters.
        
        Args:
            expression (str): The arithmetic expression.
            
        Returns:
            str: The normalized expression.
            
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        if not expression:
            raise ValueError("Expression cannot be empty.")
        
        # Remove all spaces
        normalized = expression.replace(" ", "")
        
        # Check for valid characters
        allowed_chars = set("0123456789+-*/().eE")
        if not all(char in allowed_chars for char in normalized):
            raise ValueError("Expression contains invalid characters.")
        
        # Check for balanced parentheses
        if not self._is_balanced_parentheses(normalized):
            raise SyntaxError("Unbalanced parentheses in the expression.")
        
        return normalized
    
    def _is_balanced_parentheses(self, expression: str) -> bool:
        """
        Checks if parentheses in the expression are balanced.
        
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
                if not stack:
                    return False
                stack.pop()
        return not stack
    
    def _tokenize(self, expression: str) -> List[Token]:
        """
        Converts an expression string into a list of tokens.
        
        Args:
            expression (str): The normalized expression string.
            
        Returns:
            List[Token]: A list of tokens representing the expression.
            
        Raises:
            ValueError: If tokenization fails due to invalid syntax.
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Handle numbers (including decimals and scientific notation)
            if char.isdigit() or char == '.' or (char == '-' and (i == 0 or expression[i-1] in '(+-*/')):
                # For negative numbers or a decimal point starting a number
                start = i
                # Special handling for negative numbers
                if char == '-':
                    i += 1
                
                # Scan past digits, decimal point, and scientific notation
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.' or 
                                              expression[i].lower() == 'e' or 
                                              (expression[i] in '+-' and i > 0 and expression[i-1].lower() == 'e')):
                    i += 1
                
                num_str = expression[start:i]
                try:
                    value = float(num_str)
                    tokens.append(Token(TokenType.NUMBER, value))
                except ValueError:
                    raise ValueError(f"Invalid number format: {num_str}")
                continue
            
            # Handle operators
            elif char in self.operators:
                tokens.append(Token(TokenType.OPERATOR, char))
            
            # Handle parentheses
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN))
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN))
            
            # Move to the next character
            i += 1
        
        return tokens
    
    def _infix_to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Converts a list of tokens from infix notation to postfix notation.
        
        Args:
            tokens (List[Token]): List of tokens in infix notation.
            
        Returns:
            List[Token]: List of tokens in postfix notation.
        """
        output = []
        operator_stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                output.append(token)
            elif token.type == TokenType.OPERATOR:
                while (operator_stack and 
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self.operators[operator_stack[-1].value] >= self.operators[token.value]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            elif token.type == TokenType.RIGHT_PAREN:
                while operator_stack and operator_stack[-1].type != TokenType.LEFT_PAREN:
                    output.append(operator_stack.pop())
                
                if operator_stack and operator_stack[-1].type == TokenType.LEFT_PAREN:
                    operator_stack.pop()  # Discard the left parenthesis
                else:
                    raise SyntaxError("Mismatched parentheses.")
        
        # Pop any remaining operators to the output
        while operator_stack:
            if operator_stack[-1].type == TokenType.LEFT_PAREN:
                raise SyntaxError("Mismatched parentheses.")
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, postfix: List[Token]) -> float:
        """
        Evaluates a postfix expression.
        
        Args:
            postfix (List[Token]): The expression in postfix notation.
            
        Returns:
            float: The result of the evaluation.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ValueError: If the expression is malformed.
        """
        if not postfix:
            raise ValueError("Empty expression.")
        
        stack = []
        
        for token in postfix:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands.")
                
                b = stack.pop()
                a = stack.pop()
                
                if token.value == '+':
                    stack.append(a + b)
                elif token.value == '-':
                    stack.append(a - b)
                elif token.value == '*':
                    stack.append(a * b)
                elif token.value == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    stack.append(a / b)
        
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands.")
        
        return stack[0]


# Example usage
if __name__ == "__main__":
    calc = Calculator()
    
    # Test cases
    test_expressions = [
        "3 + 4",
        "2.5 * (3 + 4.2)",
        "10 / 2",
        "(7 - 3) * (2 + 1)",
        "1 + 2 * 3",
        "2 * -3 + 4",
        "1.5e2 + 3",  # Scientific notation
        "2 + (3 * 4)",
        "2 + 3 * 4"
    ]
    
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"Error evaluating '{expr}': {str(e)}")
