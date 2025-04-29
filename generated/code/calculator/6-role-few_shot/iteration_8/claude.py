from typing import List, Union, Optional
import re
from enum import Enum


class TokenType(Enum):
    """Enum representing the types of tokens in an expression."""
    NUMBER = 0
    PLUS = 1
    MINUS = 2
    MULTIPLY = 3
    DIVIDE = 4
    LEFT_PAREN = 5
    RIGHT_PAREN = 6


class Token:
    """Class representing a token in a mathematical expression."""
    
    def __init__(self, token_type: TokenType, value: Optional[Union[float, str]] = None):
        """
        Initialize a token with its type and value.
        
        Args:
            token_type: The type of the token.
            value: The value of the token (for numbers).
        """
        self.type = token_type
        self.value = value
        
    def __repr__(self) -> str:
        if self.value is not None:
            return f"Token({self.type}, {self.value})"
        return f"Token({self.type})"


class Lexer:
    """
    Class responsible for breaking down the input expression into tokens.
    """
    
    def __init__(self, expression: str):
        """
        Initialize the lexer with an expression.
        
        Args:
            expression: The mathematical expression to tokenize.
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
        result = ''
        # Handle the decimal point
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
            
        try:
            return float(result)
        except ValueError:
            raise ValueError(f"Invalid number format: {result}")
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the expression into a list of tokens.
        
        Returns:
            A list of Token objects.
            
        Raises:
            ValueError: If an invalid character is encountered.
        """
        tokens = []
        
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
                
            if self.current_char.isdigit() or self.current_char == '.':
                tokens.append(Token(TokenType.NUMBER, self.number()))
                continue
                
            if self.current_char == '+':
                tokens.append(Token(TokenType.PLUS))
                self.advance()
                continue
                
            if self.current_char == '-':
                # Check if it's a negative number
                if not tokens or tokens[-1].type in (TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, 
                                                    TokenType.DIVIDE, TokenType.LEFT_PAREN):
                    # It's a negative number
                    self.advance()
                    if self.current_char is None or not (self.current_char.isdigit() or self.current_char == '.'):
                        raise ValueError("Expected number after negative sign")
                    value = -self.number()
                    tokens.append(Token(TokenType.NUMBER, value))
                else:
                    tokens.append(Token(TokenType.MINUS))
                    self.advance()
                continue
                
            if self.current_char == '*':
                tokens.append(Token(TokenType.MULTIPLY))
                self.advance()
                continue
                
            if self.current_char == '/':
                tokens.append(Token(TokenType.DIVIDE))
                self.advance()
                continue
                
            if self.current_char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN))
                self.advance()
                continue
                
            if self.current_char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN))
                self.advance()
                continue
                
            # If none of the above, it's an invalid character
            raise ValueError(f"Invalid character: '{self.current_char}'")
        
        return tokens


class Parser:
    """Class responsible for parsing tokens into an Abstract Syntax Tree (AST)."""
    
    def __init__(self, tokens: List[Token]):
        """
        Initialize the parser with tokens.
        
        Args:
            tokens: A list of tokens to parse.
        """
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
        
    def advance(self) -> None:
        """Move to the next token."""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def parse(self) -> float:
        """
        Parse the tokens and evaluate the expression.
        
        Returns:
            The result of the expression.
            
        Raises:
            ValueError: If there is a syntax error in the expression.
        """
        if not self.tokens:
            raise ValueError("Empty expression")
            
        result = self.expr()
        
        if self.current_token is not None:
            raise ValueError(f"Unexpected token: {self.current_token}")
            
        return result
        
    def expr(self) -> float:
        """
        Parse an expression (addition and subtraction).
        
        Returns:
            The result of the expression.
        """
        result = self.term()
        
        while self.current_token is not None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.advance()
                result += self.term()
            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                result -= self.term()
                
        return result
        
    def term(self) -> float:
        """
        Parse a term (multiplication and division).
        
        Returns:
            The result of the term.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
        """
        result = self.factor()
        
        while self.current_token is not None and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
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
        Parse a factor (number or parenthesized expression).
        
        Returns:
            The result of the factor.
            
        Raises:
            ValueError: If there is a syntax error.
        """
        token = self.current_token
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return token.value
            
        elif token.type == TokenType.LEFT_PAREN:
            self.advance()
            result = self.expr()
            
            if self.current_token is None or self.current_token.type != TokenType.RIGHT_PAREN:
                raise ValueError("Missing closing parenthesis")
                
            self.advance()
            return result
            
        raise ValueError(f"Unexpected token: {token}")


class Calculator:
    """Class implementing the calculator functionality."""
    
    @staticmethod
    def validate_expression(expression: str) -> None:
        """
        Validate the expression for syntax errors.
        
        Args:
            expression: The mathematical expression to validate.
            
        Raises:
            ValueError: If the expression has syntax errors.
        """
        # Check for allowed characters
        allowed_pattern = r'^[\d\s\+\-\*\/\(\)\.]+$'
        if not re.match(allowed_pattern, expression):
            invalid_chars = [c for c in expression if not re.match(r'[\d\s\+\-\*\/\(\)\.]', c)]
            raise ValueError(f"Expression contains invalid characters: {', '.join(invalid_chars)}")
        
        # Check for balanced parentheses
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise ValueError("Unbalanced parentheses: extra closing parenthesis")
                stack.pop()
        if stack:
            raise ValueError("Unbalanced parentheses: missing closing parenthesis")
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: A string containing the mathematical expression to evaluate.
            
        Returns:
            The result of the expression as a float.
            
        Raises:
            ValueError: If the expression has syntax errors.
            ZeroDivisionError: If division by zero is attempted.
        """
        if not expression.strip():
            raise ValueError("Empty expression")
            
        # Validate the expression
        self.validate_expression(expression)
        
        # Tokenize
        lexer = Lexer(expression)
        tokens = lexer.tokenize()
        
        # Parse and evaluate
        parser = Parser(tokens)
        result = parser.parse()
        
        return result


if __name__ == "__main__":
    calculator = Calculator()
    
    try:
        while True:
            user_input = input("Enter an expression (or 'exit' to quit): ")
            if user_input.lower() in ('exit', 'quit'):
                break
                
            try:
                result = calculator.calculate(user_input)
                print(f"Result: {result}")
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error: {e}")
    
    except KeyboardInterrupt:
        print("\nCalculator exited.")
