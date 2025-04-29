from typing import List, Union, Optional
from enum import Enum
import re


class TokenType(Enum):
    """Token types for the lexical analysis."""
    NUMBER = 1
    PLUS = 2
    MINUS = 3
    MULTIPLY = 4
    DIVIDE = 5
    LEFT_PAREN = 6
    RIGHT_PAREN = 7
    EOF = 8


class Token:
    """Represents a token in the expression."""
    
    def __init__(self, token_type: TokenType, value: Optional[Union[float, str]] = None):
        """
        Initialize a token with type and optional value.
        
        Args:
            token_type (TokenType): The type of the token.
            value (Optional[Union[float, str]]): The value of the token (for numbers).
        """
        self.type = token_type
        self.value = value
        
    def __str__(self) -> str:
        """String representation of the token."""
        if self.value is not None:
            return f"Token({self.type}, {self.value})"
        return f"Token({self.type})"


class Lexer:
    """
    Lexical analyzer that converts an expression string into tokens.
    """
    
    def __init__(self, text: str):
        """
        Initialize the lexer with an expression string.
        
        Args:
            text (str): The expression to tokenize.
        """
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None
    
    def advance(self) -> None:
        """Move to the next character in the input."""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self) -> None:
        """Skip whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def number(self) -> float:
        """
        Parse a number from the input.
        
        Returns:
            float: The parsed number.
        """
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        
        try:
            return float(result)
        except ValueError:
            raise ValueError(f"Invalid number format: {result}")
    
    def get_next_token(self) -> Token:
        """
        Get the next token from the input.
        
        Returns:
            Token: The next token.
            
        Raises:
            ValueError: If an invalid character is encountered.
        """
        while self.current_char is not None:
            
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit() or self.current_char == '.':
                return Token(TokenType.NUMBER, self.number())
            
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS)
            
            if self.current_char == '-':
                self.advance()
                # Check if it's a negative number
                if self.pos == 1 or self.text[self.pos-2] in '(+-*/':
                    if self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
                        num = self.number()
                        return Token(TokenType.NUMBER, -num)
                return Token(TokenType.MINUS)
            
            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY)
            
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE)
            
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LEFT_PAREN)
            
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RIGHT_PAREN)
            
            raise ValueError(f"Invalid character: {self.current_char}")
        
        return Token(TokenType.EOF)


class Parser:
    """
    Parser that converts tokens into an abstract syntax tree.
    """
    
    def __init__(self, lexer: Lexer):
        """
        Initialize the parser with a lexer.
        
        Args:
            lexer (Lexer): The lexer that provides tokens.
        """
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type: TokenType) -> None:
        """
        Consume the current token if it matches the expected type.
        
        Args:
            token_type (TokenType): The expected token type.
            
        Raises:
            SyntaxError: If the current token doesn't match the expected type.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token.type}")
    
    def factor(self) -> float:
        """
        Parse a factor in the expression grammar.
        
        factor : NUMBER | LPAREN expr RPAREN
        
        Returns:
            float: The value of the factor.
        """
        token = self.current_token
        
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return token.value
        elif token.type == TokenType.LEFT_PAREN:
            self.eat(TokenType.LEFT_PAREN)
            result = self.expr()
            self.eat(TokenType.RIGHT_PAREN)
            return result
        
        raise SyntaxError(f"Unexpected token: {token}")
    
    def term(self) -> float:
        """
        Parse a term in the expression grammar.
        
        term : factor ((MUL | DIV) factor)*
        
        Returns:
            float: The value of the term.
        """
        result = self.factor()
        
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
                result *= self.factor()
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
                divisor = self.factor()
                if divisor == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= divisor
        
        return result
    
    def expr(self) -> float:
        """
        Parse an expression in the expression grammar.
        
        expr : term ((PLUS | MINUS) term)*
        
        Returns:
            float: The value of the expression.
        """
        result = self.term()
        
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result += self.term()
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result -= self.term()
        
        return result


class Calculator:
    """
    A calculator that evaluates arithmetic expressions with support for parentheses
    and operator precedence.
    """
    
    def __init__(self):
        """Initialize the calculator."""
        pass
    
    def validate_expression(self, expression: str) -> None:
        """
        Validate the expression for balanced parentheses and allowed characters.
        
        Args:
            expression (str): The expression to validate.
            
        Raises:
            ValueError: If the expression contains invalid characters or has unbalanced parentheses.
        """
        # Check for valid characters
        allowed_chars = set("0123456789+-*/().\t\n ")
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
        
        # Check for empty expression or only whitespace
        if not expression.strip():
            raise ValueError("Expression cannot be empty")
            
        # Check for invalid sequences of operators
        if re.search(r'[+\-*/]{2,}', expression.replace(" ", "")):
            raise ValueError("Invalid sequence of operators")

    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression.
        
        Args:
            expression (str): The arithmetic expression to evaluate.
            
        Returns:
            float: The result of the expression evaluation.
            
        Raises:
            ValueError: If the expression contains invalid characters or has unbalanced parentheses.
            SyntaxError: If the expression has a syntax error.
            ZeroDivisionError: If there is a division by zero.
        """
        # Validate the expression
        self.validate_expression(expression)
        
        # Create lexer and parser and evaluate the expression
        lexer = Lexer(expression)
        parser = Parser(lexer)
        result = parser.expr()
        
        # Ensure we've processed the entire expression
        if parser.current_token.type != TokenType.EOF:
            raise SyntaxError("Unexpected tokens after expression")
            
        return result


def main():
    """Main function for testing the calculator in console."""
    calculator = Calculator()
    
    print("Console-based Arithmetic Calculator")
    print("Type 'exit' to quit")
    
    while True:
        try:
            expression = input("\nEnter an expression: ")
            if expression.lower() == 'exit':
                break
                
            result = calculator.calculate(expression)
            
            # Format output based on whether result is effectively an integer
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
