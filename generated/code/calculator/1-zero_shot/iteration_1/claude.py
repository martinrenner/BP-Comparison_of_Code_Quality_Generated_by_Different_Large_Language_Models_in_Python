class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    This calculator supports:
    - Basic operations: addition (+), subtraction (-), multiplication (*), division (/)
    - Parentheses for operation precedence
    - Integer and floating-point numbers (including negative values)
    
    The calculator follows standard mathematical precedence rules.
    """
    
    def __init__(self):
        """Initialize the calculator."""
        # Defined token types for parsing
        self.TOKEN_NUMBER = 'NUMBER'
        self.TOKEN_PLUS = 'PLUS'
        self.TOKEN_MINUS = 'MINUS'
        self.TOKEN_MULTIPLY = 'MULTIPLY'
        self.TOKEN_DIVIDE = 'DIVIDE'
        self.TOKEN_LPAREN = 'LPAREN'
        self.TOKEN_RPAREN = 'RPAREN'
        self.TOKEN_EOF = 'EOF'  # End of formula
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result.
        
        Args:
            expression (str): A string containing a mathematical expression
                              (e.g., "3 + 4 * (2 - 1)")
        
        Returns:
            float: The result of the evaluated expression
            
        Raises:
            ValueError: If the expression contains invalid characters or is malformed
            ZeroDivisionError: If the expression involves division by zero
            SyntaxError: If the expression has unbalanced parentheses or invalid syntax
        """
        # Input validation and sanitization
        if not expression or not isinstance(expression, str):
            raise ValueError("Expression must be a non-empty string")
        
        # Remove all whitespace
        expression = expression.replace(" ", "")
        
        # Tokenize the expression
        tokens = self._tokenize(expression)
        
        # Parse and evaluate the expression
        result = self._parse_expression(tokens)
        
        return result
    
    def _tokenize(self, expression: str) -> list:
        """
        Converts the input expression string into a list of tokens.
        
        Args:
            expression (str): The input mathematical expression
            
        Returns:
            list: A list of token dictionaries, each with 'type' and 'value' keys
            
        Raises:
            ValueError: If the expression contains invalid characters
        """
        tokens = []
        position = 0
        
        while position < len(expression):
            char = expression[position]
            
            # Handle numbers (including decimals and negative numbers)
            if char.isdigit() or (char == '.' and position + 1 < len(expression) and expression[position + 1].isdigit()):
                # Collect all digits and at most one decimal point
                number_str = ""
                decimal_point_count = 0
                
                while (position < len(expression) and 
                       (expression[position].isdigit() or expression[position] == '.')):
                    if expression[position] == '.':
                        decimal_point_count += 1
                        if decimal_point_count > 1:
                            raise ValueError("Invalid number format: multiple decimal points")
                    
                    number_str += expression[position]
                    position += 1
                
                try:
                    # Convert to float or int depending on decimal point
                    if '.' in number_str:
                        value = float(number_str)
                    else:
                        value = int(number_str)
                    
                    tokens.append({'type': self.TOKEN_NUMBER, 'value': value})
                except ValueError:
                    raise ValueError(f"Invalid number format: {number_str}")
                
                continue  # Skip the position increment at the end
            
            # Process operators and parentheses
            if char == '+':
                tokens.append({'type': self.TOKEN_PLUS, 'value': '+'})
            elif char == '-':
                # Check if it's a negative number (unary minus)
                if (not tokens or 
                    tokens[-1]['type'] in [self.TOKEN_PLUS, self.TOKEN_MINUS, 
                                         self.TOKEN_MULTIPLY, self.TOKEN_DIVIDE, 
                                         self.TOKEN_LPAREN]):
                    # It's a negative number, not a subtraction operation
                    # Read the number that follows
                    position += 1  # Skip the minus sign
                    
                    if position >= len(expression) or not (expression[position].isdigit() or expression[position] == '.'):
                        raise ValueError("Expected a number after the negative sign")
                    
                    number_str = "-"  # Start with negative sign
                    decimal_point_count = 0
                    
                    while (position < len(expression) and 
                           (expression[position].isdigit() or expression[position] == '.')):
                        if expression[position] == '.':
                            decimal_point_count += 1
                            if decimal_point_count > 1:
                                raise ValueError("Invalid number format: multiple decimal points")
                        
                        number_str += expression[position]
                        position += 1
                    
                    try:
                        # Convert to float or int depending on decimal point
                        if '.' in number_str:
                            value = float(number_str)
                        else:
                            value = int(number_str)
                        
                        tokens.append({'type': self.TOKEN_NUMBER, 'value': value})
                    except ValueError:
                        raise ValueError(f"Invalid number format: {number_str}")
                    
                    continue  # Skip the position increment at the end
                else:
                    # It's a subtraction operation
                    tokens.append({'type': self.TOKEN_MINUS, 'value': '-'})
            elif char == '*':
                tokens.append({'type': self.TOKEN_MULTIPLY, 'value': '*'})
            elif char == '/':
                tokens.append({'type': self.TOKEN_DIVIDE, 'value': '/'})
            elif char == '(':
                tokens.append({'type': self.TOKEN_LPAREN, 'value': '('})
            elif char == ')':
                tokens.append({'type': self.TOKEN_RPAREN, 'value': ')'})
            else:
                raise ValueError(f"Invalid character in expression: {char}")
            
            position += 1
        
        # Add EOF token to signify the end of the expression
        tokens.append({'type': self.TOKEN_EOF, 'value': None})
        
        return tokens
    
    def _parse_expression(self, tokens: list) -> float:
        """
        Parse and evaluate the tokenized expression using recursive descent parsing.
        
        Args:
            tokens (list): List of tokens from the _tokenize method
            
        Returns:
            float: The result of the evaluated expression
            
        Raises:
            SyntaxError: If the expression has unbalanced parentheses or invalid syntax
            ZeroDivisionError: If the expression involves division by zero
        """
        # Create a position tracker for the tokens
        self.current_token_index = 0
        self.tokens = tokens
        self.current_token = self.tokens[self.current_token_index]
        
        # Start the parsing process
        result = self._expression()
        
        # Check that we consumed all tokens
        if self.current_token['type'] != self.TOKEN_EOF:
            raise SyntaxError("Invalid syntax: unexpected tokens at the end")
        
        return result
    
    def _advance(self):
        """Advance to the next token."""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
    
    def _expression(self) -> float:
        """
        Parse and evaluate an expression (addition and subtraction).
        
        Returns:
            float: The result of the evaluated expression
        """
        result = self._term()  # Start with higher precedence operations
        
        while self.current_token['type'] in [self.TOKEN_PLUS, self.TOKEN_MINUS]:
            token = self.current_token
            if token['type'] == self.TOKEN_PLUS:
                self._advance()
                result += self._term()
            elif token['type'] == self.TOKEN_MINUS:
                self._advance()
                result -= self._term()
        
        return result
    
    def _term(self) -> float:
        """
        Parse and evaluate a term (multiplication and division).
        
        Returns:
            float: The result of the evaluated term
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
        """
        result = self._factor()  # Start with highest precedence operations
        
        while self.current_token['type'] in [self.TOKEN_MULTIPLY, self.TOKEN_DIVIDE]:
            token = self.current_token
            if token['type'] == self.TOKEN_MULTIPLY:
                self._advance()
                result *= self._factor()
            elif token['type'] == self.TOKEN_DIVIDE:
                self._advance()
                divisor = self._factor()
                if divisor == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                result /= divisor
        
        return result
    
    def _factor(self) -> float:
        """
        Parse and evaluate a factor (numbers and parenthesized expressions).
        
        Returns:
            float: The value of the factor
            
        Raises:
            SyntaxError: If the expression has unbalanced parentheses
            ValueError: If the token is unexpected
        """
        token = self.current_token
        
        if token['type'] == self.TOKEN_NUMBER:
            # Simple number
            self._advance()
            return token['value']
        elif token['type'] == self.TOKEN_LPAREN:
            # Handle parenthesized expressions
            self._advance()  # Consume '('
            result = self._expression()  # Calculate the expression inside parentheses
            
            # Ensure we have a closing parenthesis
            if self.current_token['type'] != self.TOKEN_RPAREN:
                raise SyntaxError("Missing closing parenthesis")
            
            self._advance()  # Consume ')'
            return result
        else:
            raise ValueError(f"Unexpected token: {token['type']}")


if __name__ == "__main__":
    calculator = Calculator()
    
    print("Console-based Arithmetic Calculator")
    print("Enter mathematical expressions to calculate or 'exit' to quit")
    print("Supported operations: +, -, *, / and parentheses ()")
    
    while True:
        # Get user input
        user_input = input("\nEnter expression: ")
        
        # Check if user wants to exit
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("Calculator exiting. Goodbye!")
            break
        
        # Skip empty inputs
        if not user_input.strip():
            continue
        
        try:
            # Calculate the result
            result = calculator.calculate(user_input)
            
            # Format the output (show as integer if it's a whole number)
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except (ValueError, SyntaxError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
