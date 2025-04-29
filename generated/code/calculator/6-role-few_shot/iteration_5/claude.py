from enum import Enum
from typing import List, Optional, Union, Tuple
import re


class TokenType(Enum):
    """Enum representing the different types of tokens in an expression."""
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"


class Token:
    """Class representing a token in the expression."""
    
    def __init__(self, token_type: TokenType, value: Optional[Union[str, float]] = None):
        """
        Initialize a new token.
        
        Args:
            token_type: The type of the token.
            value: The value of the token (only for NUMBER tokens).
        """
        self.type = token_type
        self.value = value
        
    def __str__(self) -> str:
        if self.value is not None:
            return f"{self.type.value}({self.value})"
        return self.type.value


class Lexer:
    """Class to tokenize an arithmetic expression."""
    
    def __init__(self, expression: str):
        """
        Initialize a new lexer.
        
        Args:
            expression: The arithmetic expression to tokenize.
        """
        self.expression = expression
        self.position = 0
        self.current_char = self.expression[0] if expression else None
    
    def advance(self) -> None:
        """Move to the next character in the expression."""
        self.position += 1
        if self.position < len(self.expression):
            self.current_char = self.expression[self.position]
        else:
            self.current_char = None
    
    def skip_whitespace(self) -> None:
        """Skip any whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def number(self) -> float:
        """
        Parse a number from the expression.
        
        Returns:
            The parsed number as a float.
        """
        result = ""
        # Process digits before decimal point
        while (self.current_char is not None and 
               (self.current_char.isdigit() or self.current_char == '.')):
            result += self.current_char
            self.advance()
        
        # Validate the number format
        if result.count('.') > 1:
            raise ValueError(f"Invalid number format: '{result}'")
        
        return float(result)
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the expression.
        
        Returns:
            A list of Token objects representing the expression.
            
        Raises:
            ValueError: If invalid characters are found in the expression.
        """
        tokens = []
        
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit() or self.current_char == '.':
                tokens.append(Token(TokenType.NUMBER, self.number()))
            elif self.current_char == '+':
                tokens.append(Token(TokenType.PLUS))
                self.advance()
            elif self.current_char == '-':
                # Check if it's a negative number or a subtraction operation
                if (not tokens or tokens[-1].type in 
                    [TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, 
                     TokenType.DIVIDE, TokenType.LEFT_PAREN]):
                    self.advance()
                    if self.current_char is None or not (self.current_char.isdigit() or self.current_char == '.'):
                        raise ValueError("Invalid negative number format")
                    number = self.number()
                    tokens.append(Token(TokenType.NUMBER, -number))
                else:
                    tokens.append(Token(TokenType.MINUS))
                    self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TokenType.MULTIPLY))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TokenType.DIVIDE))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN))
                self.advance()
            else:
                raise ValueError(f"Invalid character: '{self.current_char}'")
        
        return tokens


class Parser:
    """Class to parse tokenized arithmetic expressions."""
    
    def __init__(self, tokens: List[Token]):
        """
        Initialize a new parser.
        
        Args:
            tokens: The list of tokens to parse.
        """
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def advance(self) -> None:
        """Move to the next token in the list."""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def parse(self) -> float:
        """
        Parse the expression and evaluate it.
        
        Returns:
            The result of the expression evaluation.
            
        Raises:
            ValueError: If the expression is invalid.
        """
        return self.expression()
    
    def expression(self) -> float:
        """
        Parse and evaluate an expression.
        
        Grammar rule: expression -> term ((PLUS | MINUS) term)*
        
        Returns:
            The result of the expression evaluation.
        """
        result = self.term()
        
        while (self.current_token is not None and 
               self.current_token.type in [TokenType.PLUS, TokenType.MINUS]):
            if self.current_token.type == TokenType.PLUS:
                self.advance()
                result += self.term()
            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                result -= self.term()
        
        return result
    
    def term(self) -> float:
        """
        Parse and evaluate a term.
        
        Grammar rule: term -> factor ((MULTIPLY | DIVIDE) factor)*
        
        Returns:
            The result of the term evaluation.
        """
        result = self.factor()
        
        while (self.current_token is not None and 
               self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE]):
            if self.current_token.type == TokenType.MULTIPLY:
                self.advance()
                result *= self.factor()
            elif self.current_token.type == TokenType.DIVIDE:
                self.advance()
                divisor = self.factor()
                if divisor == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= divisor
        
        return result
    
    def factor(self) -> float:
        """
        Parse and evaluate a factor.
        
        Grammar rule: factor -> NUMBER | (PLUS | MINUS) factor | LEFT_PAREN expression RIGHT_PAREN
        
        Returns:
            The result of the factor evaluation.
        """
        if self.current_token.type == TokenType.NUMBER:
            result = self.current_token.value
            self.advance()
            return result
        elif self.current_token.type == TokenType.LEFT_PAREN:
            self.advance()
            result = self.expression()
            
            if self.current_token is None or self.current_token.type != TokenType.RIGHT_PAREN:
                raise ValueError("Unbalanced parentheses")
            
            self.advance()
            return result
        else:
            raise ValueError(f"Unexpected token: {self.current_token}")


class Calculator:
    """Class that implements the calculator functionality."""
    
    @staticmethod
    def validate_expression(expression: str) -> None:
        """
        Validate the expression for proper syntax.
        
        Args:
            expression: The expression to validate.
            
        Raises:
            ValueError: If the expression has invalid syntax.
        """
        # Check for valid characters
        allowed_chars = set("0123456789+-*/().e ")
        if not all(char in allowed_chars for char in expression):
            invalid_chars = [char for char in expression if char not in allowed_chars]
            raise ValueError(f"Expression contains invalid characters: {invalid_chars}")
        
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
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return the result.
        
        Args:
            expression: The arithmetic expression as a string.
            
        Returns:
            The result of the evaluation as a float.
            
        Raises:
            ValueError: If the expression is invalid.
            ZeroDivisionError: If division by zero is attempted.
        """
        if not expression:
            raise ValueError("Expression cannot be empty")
        
        # Validate the expression
        self.validate_expression(expression)
        
        # Tokenize the expression
        lexer = Lexer(expression)
        tokens = lexer.tokenize()
        
        if not tokens:
            raise ValueError("No valid tokens found in expression")
        
        # Parse and evaluate the expression
        parser = Parser(tokens)
        result = parser.parse()
        
        return result


if __name__ == "__main__":
    calculator = Calculator()
    
    print("Arithmetic Calculator")
    print("Enter an expression (or 'quit' to exit):")
    
    while True:
        expression = input("> ")
        
        if expression.lower() in ("quit", "exit", "q"):
            break
        
        try:
            result = calculator.calculate(expression)
            
            # Format the result to remove trailing zeros for integer values
            if result == int(result):
                formatted_result = int(result)
            else:
                formatted_result = result
                
            print(f"Result: {formatted_result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
