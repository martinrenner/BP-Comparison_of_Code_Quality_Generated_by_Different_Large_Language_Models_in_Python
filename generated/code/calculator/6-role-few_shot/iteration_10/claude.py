class Calculator:
    """
    A calculator that evaluates arithmetic expressions with support for basic operations,
    parentheses, and proper operator precedence.
    
    Supported operations:
    - Addition (+)
    - Subtraction (-)
    - Multiplication (*)
    - Division (/)
    - Parentheses for grouping
    
    Examples:
        >>> calc = Calculator()
        >>> calc.calculate("2 + 3 * 4")
        14.0
        >>> calc.calculate("(2 + 3) * 4")
        20.0
        >>> calc.calculate("-5 + 10 / 2")
        0.0
    """
    
    def __init__(self):
        """Initialize the Calculator."""
        self.position = 0
        self.current_token = None
        self.expression = ""
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression.
        
        Args:
            expression (str): The arithmetic expression to evaluate.
            
        Returns:
            float: The result of the evaluated expression.
            
        Raises:
            ValueError: If the expression contains invalid characters or has syntax errors.
            ZeroDivisionError: If the expression attempts to divide by zero.
        """
        if not expression:
            raise ValueError("Expression cannot be empty.")
            
        self.expression = self._normalize_expression(expression)
        self.position = 0
        self._get_next_token()
        
        result = self._parse_addition()
        
        # Check if there are any remaining tokens
        if self.current_token is not None:
            raise ValueError(f"Unexpected token '{self.current_token}' at position {self.position}.")
        
        return result
    
    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression by removing spaces and validating characters.
        
        Args:
            expression (str): The expression to normalize.
            
        Returns:
            str: The normalized expression.
            
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().e ")
        if not all(char.lower() in allowed_chars for char in expression):
            invalid_chars = [char for char in expression if char.lower() not in allowed_chars]
            raise ValueError(f"Expression contains invalid characters: {invalid_chars}")
        
        # Replace spaces, handle negative sign at start or after operators/parenthesis
        return expression.replace(" ", "")
    
    def _is_balanced(self, expression: str) -> bool:
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
        return len(stack) == 0
    
    def _get_next_token(self) -> None:
        """
        Advances to the next token in the expression.
        Sets the current_token to None if the end of the expression is reached.
        """
        if self.position >= len(self.expression):
            self.current_token = None
            return
            
        char = self.expression[self.position]
        if char in "+-*/()":
            self.current_token = char
            self.position += 1
        elif char.isdigit() or char == '.':
            # Parse a number (integer or float)
            start = self.position
            while (self.position < len(self.expression) and 
                   (self.expression[self.position].isdigit() or 
                    self.expression[self.position] == '.' or
                    self.expression[self.position].lower() == 'e' or
                    (self.expression[self.position] in '+-' and 
                     self.position > 0 and 
                     self.expression[self.position-1].lower() == 'e'))):
                self.position += 1
                
            number_str = self.expression[start:self.position]
            try:
                self.current_token = float(number_str)
                # Convert to int if it's a whole number
                if self.current_token.is_integer():
                    self.current_token = int(self.current_token)
            except ValueError:
                raise ValueError(f"Invalid number format: {number_str}")
        else:
            raise ValueError(f"Unexpected character '{char}' at position {self.position}")
    
    def _parse_addition(self) -> float:
        """
        Parses addition and subtraction operations.
        
        Returns:
            float: The result of the addition/subtraction operations.
        """
        result = self._parse_multiplication()
        
        while self.current_token in ('+', '-'):
            if self.current_token == '+':
                self._get_next_token()
                result += self._parse_multiplication()
            else:  # self.current_token == '-'
                self._get_next_token()
                result -= self._parse_multiplication()
                
        return result
    
    def _parse_multiplication(self) -> float:
        """
        Parses multiplication and division operations.
        
        Returns:
            float: The result of the multiplication/division operations.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
        """
        result = self._parse_factor()
        
        while self.current_token in ('*', '/'):
            if self.current_token == '*':
                self._get_next_token()
                result *= self._parse_factor()
            else:  # self.current_token == '/'
                self._get_next_token()
                divisor = self._parse_factor()
                if divisor == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                result /= divisor
                
        return result
    
    def _parse_factor(self) -> float:
        """
        Parses a factor (number, parenthesized expression, or unary operation).
        
        Returns:
            float: The value of the factor.
            
        Raises:
            ValueError: If the expression has invalid syntax.
        """
        # Handle unary plus and minus
        if self.current_token == '+':
            self._get_next_token()
            return self._parse_factor()
        elif self.current_token == '-':
            self._get_next_token()
            return -self._parse_factor()
        
        # Handle numbers
        if isinstance(self.current_token, (int, float)):
            value = self.current_token
            self._get_next_token()
            return float(value)
        
        # Handle parentheses
        elif self.current_token == '(':
            self._get_next_token()  # Skip '('
            result = self._parse_addition()
            
            if self.current_token != ')':
                raise ValueError("Missing closing parenthesis.")
                
            self._get_next_token()  # Skip ')'
            return result
            
        else:
            if self.current_token is None:
                raise ValueError("Unexpected end of expression.")
            else:
                raise ValueError(f"Unexpected token: {self.current_token}")


def main():
    """
    Main function to run the calculator interactively.
    """
    calculator = Calculator()
    print("Calculator (type 'exit' to quit)")
    print("Enter expression to calculate:")
    
    while True:
        try:
            expression = input("> ")
            if expression.lower() in ('exit', 'quit'):
                break
                
            if not expression:
                continue
                
            result = calculator.calculate(expression)
            print(f"= {result}")
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
