import re
from typing import List, Union, Tuple, Optional
from enum import Enum, auto


class TokenType(Enum):
    """Enum representing the types of tokens in an arithmetic expression."""
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()


class Token:
    """Represents a token in an arithmetic expression."""
    
    def __init__(self, token_type: TokenType, value: Optional[Union[int, float]] = None):
        """
        Initialize a token with a type and optional value.
        
        Args:
            token_type: The type of the token.
            value: The numeric value (only for NUMBER tokens).
        """
        self.type = token_type
        self.value = value
        
    def __str__(self) -> str:
        if self.type == TokenType.NUMBER:
            return f"NUMBER({self.value})"
        else:
            return f"{self.type.name}"


class Lexer:
    """
    Converts a string expression into tokens that can be parsed.
    """
    
    def __init__(self, expression: str):
        """
        Initialize the lexer with an expression string.
        
        Args:
            expression: The string arithmetic expression to tokenize.
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
        """Skip any whitespace characters in the expression."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
            
    def number(self) -> Token:
        """
        Parse a number from the expression.
        
        Returns:
            A NUMBER token with the parsed value.
            
        Raises:
            ValueError: If the number format is invalid.
        """
        result = ''
        has_dot = False
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_dot:
                    raise ValueError("Invalid number format: multiple decimal points")
                has_dot = True
                
            result += self.current_char
            self.advance()
            
        try:
            value = float(result)
            # Convert to int if the value is a whole number
            if value.is_integer():
                value = int(value)
            return Token(TokenType.NUMBER, value)
        except ValueError:
            raise ValueError(f"Invalid number format: {result}")
            
    def tokenize(self) -> List[Token]:
        """
        Convert the expression string into a list of tokens.
        
        Returns:
            A list of Token objects representing the expression.
            
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        tokens = []
        
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
                
            if self.current_char.isdigit() or self.current_char == '.':
                tokens.append(self.number())
                continue
                
            if self.current_char == '+':
                tokens.append(Token(TokenType.PLUS))
                self.advance()
                continue
                
            if self.current_char == '-':
                # Check if it's a negative number (unary minus)
                is_unary_minus = (not tokens or 
                                 tokens[-1].type in (TokenType.PLUS, TokenType.MINUS, 
                                                   TokenType.MULTIPLY, TokenType.DIVIDE,
                                                   TokenType.LEFT_PAREN))
                
                if is_unary_minus and (self.position + 1 < len(self.expression) and 
                                     (self.expression[self.position + 1].isdigit() or 
                                      self.expression[self.position + 1] == '.')):
                    self.advance()
                    if self.current_char is None:
                        raise ValueError("Expected number after negative sign")
                        
                    if self.current_char.isdigit() or self.current_char == '.':
                        num_token = self.number()
                        num_token.value = -num_token.value
                        tokens.append(num_token)
                    continue
                
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
                
            # If we get here, we have an invalid character
            raise ValueError(f"Invalid character: {self.current_char}")
            
        return tokens


class Parser:
    """
    Parses tokens into an Abstract Syntax Tree (AST).
    Implements a recursive descent parser for arithmetic expressions.
    """
    
    def __init__(self, tokens: List[Token]):
        """
        Initialize the parser with a list of tokens.
        
        Args:
            tokens: The list of tokens to parse.
        """
        self.tokens = tokens
        self.current_token_index = 0
        
    def current_token(self) -> Token:
        """Get the current token."""
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        raise IndexError("Unexpected end of expression")
        
    def advance(self) -> None:
        """Move to the next token."""
        self.current_token_index += 1
        
    def parse(self) -> float:
        """
        Parse the tokens and evaluate the expression.
        
        Returns:
            The result of the evaluated expression.
            
        Raises:
            ValueError: If the expression is invalid.
        """
        return self.expr()
        
    def expr(self) -> float:
        """
        Parse an expression: term ((PLUS|MINUS) term)*
        
        Returns:
            The evaluated expression value.
        """
        result = self.term()
        
        while (self.current_token_index < len(self.tokens) and 
               self.current_token().type in (TokenType.PLUS, TokenType.MINUS)):
            token = self.current_token()
            self.advance()
            
            if token.type == TokenType.PLUS:
                result += self.term()
            elif token.type == TokenType.MINUS:
                result -= self.term()
                
        return result
        
    def term(self) -> float:
        """
        Parse a term: factor ((MULTIPLY|DIVIDE) factor)*
        
        Returns:
            The evaluated term value.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
        """
        result = self.factor()
        
        while (self.current_token_index < len(self.tokens) and 
               self.current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE)):
            token = self.current_token()
            self.advance()
            
            if token.type == TokenType.MULTIPLY:
                result *= self.factor()
            elif token.type == TokenType.DIVIDE:
                divisor = self.factor()
                if divisor == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= divisor
                
        return result
        
    def factor(self) -> float:
        """
        Parse a factor: NUMBER | LEFT_PAREN expr RIGHT_PAREN
        
        Returns:
            The evaluated factor value.
            
        Raises:
            ValueError: If parentheses are unbalanced or the syntax is invalid.
        """
        token = self.current_token()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return token.value
        
        elif token.type == TokenType.LEFT_PAREN:
            self.advance()
            result = self.expr()
            
            # Ensure we have a matching closing parenthesis
            if (self.current_token_index >= len(self.tokens) or 
                self.current_token().type != TokenType.RIGHT_PAREN):
                raise ValueError("Unbalanced parentheses: missing closing parenthesis")
                
            self.advance()  # Consume the right parenthesis
            return result
            
        else:
            raise ValueError(f"Unexpected token: {token}")


class Calculator:
    """
    A calculator that evaluates arithmetic expressions.
    Supports addition, subtraction, multiplication, division, parentheses,
    and respects operator precedence.
    """
    
    def validate_expression(self, expression: str) -> None:
        """
        Validate the expression for balanced parentheses and other issues.
        
        Args:
            expression: The arithmetic expression to validate.
            
        Raises:
            ValueError: If the expression has unbalanced parentheses or is empty.
        """
        if not expression or expression.strip() == "":
            raise ValueError("Expression cannot be empty")
            
        # Check for balanced parentheses
        paren_count = 0
        for char in expression:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: unexpected closing parenthesis")
                    
        if paren_count > 0:
            raise ValueError("Unbalanced parentheses: missing closing parenthesis")
            
        # Check for invalid characters
        valid_chars = set("0123456789+-*/().e ")  # Include 'e' for scientific notation
        for char in expression:
            if char not in valid_chars:
                raise ValueError(f"Invalid character in expression: '{char}'")
        
        # Check for consecutive operation characters
        if re.search(r'[+\-*/]{2,}', expression.replace(' ', '')):
            raise ValueError("Invalid expression: consecutive operators")
            
    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression.
        
        Args:
            expression: The arithmetic expression to evaluate.
            
        Returns:
            The result of the calculation.
            
        Raises:
            ValueError: If the expression is invalid.
            ZeroDivisionError: If division by zero is attempted.
        """
        # Validate the expression
        self.validate_expression(expression)
        
        # Tokenize the expression
        lexer = Lexer(expression)
        tokens = lexer.tokenize()
        
        # Parse and evaluate the expression
        parser = Parser(tokens)
        result = parser.parse()
        
        return result


def main() -> None:
    """
    Main function to run the calculator interactively.
    """
    calculator = Calculator()
    print("Calculator (type 'exit' to quit)")
    
    while True:
        try:
            expression = input("Enter an expression: ")
            
            if expression.lower() == 'exit':
                break
                
            result = calculator.calculate(expression)
            
            # Format the output - display as integer if it's a whole number
            if isinstance(result, float) and result.is_integer():
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
            
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
