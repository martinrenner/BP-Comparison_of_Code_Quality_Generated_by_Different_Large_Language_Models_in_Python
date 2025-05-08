from typing import List, Dict, Callable, Union, Optional
import re
from enum import Enum


class TokenType(Enum):
    """Enum representing the types of tokens in mathematical expressions."""
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"


class Token:
    """Class representing a token in a mathematical expression."""
    def __init__(self, token_type: TokenType, value: str):
        """
        Initialize a token with a type and value.

        Args:
            token_type (TokenType): The type of the token.
            value (str): The string value of the token.
        """
        self.type = token_type
        self.value = value

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class Calculator:
    """
    A calculator that evaluates arithmetic expressions.
    Supports addition, subtraction, multiplication, division, and parentheses.
    """

    def __init__(self):
        """Initialize the calculator with operator precedence and functions."""
        # Define precedence for operators
        self.operators: Dict[str, Dict] = {
            '+': {'precedence': 1, 'function': lambda a, b: a + b},
            '-': {'precedence': 1, 'function': lambda a, b: a - b},
            '*': {'precedence': 2, 'function': lambda a, b: a * b},
            '/': {'precedence': 2, 'function': lambda a, b: a / b if b != 0 else self._handle_division_by_zero()}
        }

    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the expression evaluation.

        Raises:
            ValueError: If the expression is invalid or contains unsupported operations.
            ZeroDivisionError: If division by zero is attempted.
            SyntaxError: If the expression has unbalanced parentheses or invalid syntax.
        """
        # Validate and normalize the expression
        normalized_expr = self._normalize_expression(expression)
        
        # Check for balanced parentheses
        if not self._has_balanced_parentheses(normalized_expr):
            raise SyntaxError("Unbalanced parentheses in the expression")

        # Tokenize the expression
        tokens = self._tokenize(normalized_expr)
        
        # Convert infix to postfix notation
        postfix = self._infix_to_postfix(tokens)
        
        # Evaluate the postfix expression
        result = self._evaluate_postfix(postfix)
        
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalize an expression by removing spaces and validating characters.

        Args:
            expression (str): The expression to normalize.

        Returns:
            str: The normalized expression.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
            
        # Define allowed characters
        allowed_chars = set("0123456789+-*/(). ")
        
        # Check for invalid characters
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters")
        
        # Remove spaces
        return expression.replace(" ", "")

    def _has_balanced_parentheses(self, expression: str) -> bool:
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
                if not stack:
                    return False
                stack.pop()
        return not stack

    def _tokenize(self, expression: str) -> List[Token]:
        """
        Convert a string expression into a list of tokens.

        Args:
            expression (str): The expression to tokenize.

        Returns:
            List[Token]: A list of tokens representing the expression.

        Raises:
            SyntaxError: If there's an invalid token in the expression.
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Check for numbers (including decimal and negative)
            if char.isdigit() or (char == '.' and i + 1 < len(expression) and expression[i + 1].isdigit()):
                # Find the end of the number
                j = i
                decimal_point_seen = (char == '.')
                
                while j < len(expression) and (expression[j].isdigit() or (expression[j] == '.' and not decimal_point_seen)):
                    if expression[j] == '.':
                        decimal_point_seen = True
                    j += 1
                
                number_str = expression[i:j]
                try:
                    float(number_str)  # Validate that it's a proper number
                    tokens.append(Token(TokenType.NUMBER, number_str))
                except ValueError:
                    raise SyntaxError(f"Invalid number format: {number_str}")
                
                i = j
                continue
            
            # Check for operators
            if char in self.operators:
                tokens.append(Token(TokenType.OPERATOR, char))
            
            # Check for parentheses
            elif char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char))
            elif char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char))
            
            # Handle unary minus for negative numbers
            elif char == '-' and (i == 0 or expression[i-1] in self.operators or expression[i-1] == '('):
                if i + 1 < len(expression) and (expression[i+1].isdigit() or expression[i+1] == '.'):
                    j = i + 1
                    decimal_point_seen = (expression[j] == '.')
                    
                    while j < len(expression) and (expression[j].isdigit() or (expression[j] == '.' and not decimal_point_seen)):
                        if expression[j] == '.':
                            decimal_point_seen = True
                        j += 1
                    
                    number_str = '-' + expression[i+1:j]
                    try:
                        float(number_str)  # Validate that it's a proper number
                        tokens.append(Token(TokenType.NUMBER, number_str))
                    except ValueError:
                        raise SyntaxError(f"Invalid number format: {number_str}")
                    
                    i = j
                    continue
                else:
                    tokens.append(Token(TokenType.OPERATOR, char))
            
            # Skip characters that have been handled
            else:
                raise SyntaxError(f"Unexpected character: {char}")
            
            i += 1
        
        return tokens

    def _infix_to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Convert an infix expression to postfix notation (Shunting Yard algorithm).

        Args:
            tokens (List[Token]): Tokenized infix expression.

        Returns:
            List[Token]: Tokens in postfix notation.
        """
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                output_queue.append(token)
            elif token.type == TokenType.OPERATOR:
                while (operator_stack and
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self.operators[operator_stack[-1].value]['precedence'] >= self.operators[token.value]['precedence']):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)
            elif token.type == TokenType.RIGHT_PAREN:
                while operator_stack and operator_stack[-1].type != TokenType.LEFT_PAREN:
                    output_queue.append(operator_stack.pop())
                
                # Pop the left parenthesis
                if operator_stack and operator_stack[-1].type == TokenType.LEFT_PAREN:
                    operator_stack.pop()
                else:
                    # This shouldn't happen if parentheses are balanced
                    raise SyntaxError("Mismatched parentheses")
        
        # Pop any remaining operators
        while operator_stack:
            if operator_stack[-1].type == TokenType.LEFT_PAREN:
                raise SyntaxError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
        
        return output_queue

    def _evaluate_postfix(self, tokens: List[Token]) -> float:
        """
        Evaluate a postfix expression.

        Args:
            tokens (List[Token]): Tokens in postfix notation.

        Returns:
            float: The result of evaluating the expression.

        Raises:
            SyntaxError: If the expression is malformed.
            ZeroDivisionError: If division by zero is attempted.
        """
        if not tokens:
            raise SyntaxError("Empty expression")
        
        stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                stack.append(float(token.value))
            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise SyntaxError("Invalid expression: insufficient operands")
                
                # Pop the operands in reverse order
                b = stack.pop()
                a = stack.pop()
                
                # Apply the operator
                result = self.operators[token.value]['function'](a, b)
                stack.append(result)
        
        if len(stack) != 1:
            raise SyntaxError("Invalid expression: too many operands")
        
        return stack[0]

    def _handle_division_by_zero(self) -> None:
        """
        Handle division by zero by raising an appropriate exception.

        Raises:
            ZeroDivisionError: Always raised when this method is called.
        """
        raise ZeroDivisionError("Division by zero is not allowed")


if __name__ == "__main__":
    calc = Calculator()
    
    # Example usage
    try:
        result = calc.calculate("(2 + 3) * 4 / 2")
        print(f"Result: {result}")
    except (ValueError, SyntaxError, ZeroDivisionError) as e:
        print(f"Error: {e}")
