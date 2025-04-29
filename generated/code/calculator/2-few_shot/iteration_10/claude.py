class Calculator:
    """
    A calculator for evaluating mathematical expressions with support for
    basic arithmetic operations and parentheses.
    
    This implementation handles:
    - Addition (+), subtraction (-), multiplication (*), and division (/)
    - Parentheses for operation precedence
    - Both integers and floating-point numbers (including negative values)
    - Input validation
    """
    
    def __init__(self):
        """Initialize the Calculator object."""
        self.position = 0  # Current position in the expression
        self.expression = ""  # Expression to be evaluated
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression (str): The mathematical expression to evaluate.
            
        Returns:
            float: The result of the evaluated expression.
            
        Raises:
            ValueError: If the expression contains invalid characters, unbalanced parentheses,
                        or is syntactically incorrect.
            ZeroDivisionError: If the expression attempts a division by zero.
        """
        if not expression:
            raise ValueError("Expression cannot be empty")
        
        # Normalize and validate the expression
        self.expression = self._normalize_expression(expression)
        
        # Check for balanced parentheses
        if not self._is_balanced_parentheses(self.expression):
            raise ValueError("Unbalanced parentheses in the expression")
        
        # Parse and evaluate the expression
        self.position = 0
        result = self._parse_expression()
        
        # Check if the entire expression was processed
        if self.position < len(self.expression):
            raise ValueError(f"Unexpected character at position {self.position}: '{self.expression[self.position]}'")
        
        return result
    
    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression by removing spaces and validating characters.
        
        Args:
            expression (str): The original expression.
            
        Returns:
            str: The normalized expression.
            
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Remove all whitespace
        normalized = expression.replace(" ", "")
        
        # Check for allowed characters
        allowed_chars = set("0123456789+-*/().e")
        if not all(char in allowed_chars for char in normalized):
            invalid_chars = [char for char in normalized if char not in allowed_chars]
            raise ValueError(f"Expression contains invalid characters: {', '.join(invalid_chars)}")
        
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
        return len(stack) == 0
    
    def _peek(self) -> str:
        """
        Returns the current character without advancing the position.
        
        Returns:
            str: The current character, or an empty string if at the end.
        """
        if self.position >= len(self.expression):
            return ''
        return self.expression[self.position]
    
    def _consume(self) -> str:
        """
        Returns the current character and advances the position.
        
        Returns:
            str: The current character.
        """
        char = self._peek()
        self.position += 1
        return char
    
    def _parse_expression(self) -> float:
        """
        Parses an expression according to the grammar.
        
        Returns:
            float: The value of the expression.
        """
        return self._parse_add_sub()
    
    def _parse_add_sub(self) -> float:
        """
        Parses addition and subtraction operations.
        
        Returns:
            float: The result of the calculations.
        """
        left = self._parse_mul_div()
        
        while self._peek() in ('+', '-'):
            operator = self._consume()
            right = self._parse_mul_div()
            
            if operator == '+':
                left += right
            else:  # operator == '-'
                left -= right
                
        return left
    
    def _parse_mul_div(self) -> float:
        """
        Parses multiplication and division operations.
        
        Returns:
            float: The result of the calculations.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
        """
        left = self._parse_unary()
        
        while self._peek() in ('*', '/'):
            operator = self._consume()
            right = self._parse_unary()
            
            if operator == '*':
                left *= right
            else:  # operator == '/'
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                left /= right
                
        return left
    
    def _parse_unary(self) -> float:
        """
        Parses unary operations (+ and -).
        
        Returns:
            float: The result after applying the unary operation.
        """
        # Handle unary plus and minus
        if self._peek() == '+':
            self._consume()
            return self._parse_unary()
        elif self._peek() == '-':
            self._consume()
            return -self._parse_unary()
            
        return self._parse_parentheses()
    
    def _parse_parentheses(self) -> float:
        """
        Parses expressions in parentheses.
        
        Returns:
            float: The result of the parenthesized expression or number.
        """
        if self._peek() == '(':
            self._consume()  # Consume '('
            result = self._parse_expression()
            
            # Expect closing parenthesis
            if self._peek() != ')':
                raise ValueError(f"Expected ')', found '{self._peek()}' at position {self.position}")
            
            self._consume()  # Consume ')'
            return result
            
        return self._parse_number()
    
    def _parse_number(self) -> float:
        """
        Parses a number from the expression.
        
        Returns:
            float: The parsed number.
            
        Raises:
            ValueError: If no valid number is found at the current position.
        """
        # Check if we have a valid digit
        if not (self._peek().isdigit() or self._peek() == '.'):
            raise ValueError(f"Expected number, found '{self._peek()}' at position {self.position}")
        
        # Extract the number
        start_pos = self.position
        has_decimal = False
        has_exponent = False
        
        while (self._peek().isdigit() or 
               self._peek() == '.' and not has_decimal or
               self._peek().lower() == 'e' and not has_exponent):
               
            if self._peek() == '.':
                has_decimal = True
            elif self._peek().lower() == 'e':
                has_exponent = True
                self._consume()  # Consume 'e'
                
                # Handle potential sign after 'e'
                if self._peek() in ('+', '-'):
                    self._consume()
                
                # Must have at least one digit after exponent
                if not self._peek().isdigit():
                    raise ValueError(f"Expected digit after exponent at position {self.position}")
                
                continue  # Skip the increment since we've already consumed a character
                
            self._consume()
            
        # Convert the substring to a number
        number_str = self.expression[start_pos:self.position]
        try:
            return float(number_str)
        except ValueError:
            raise ValueError(f"Invalid number format: '{number_str}'")


def main():
    """
    Main function to run the calculator in interactive mode.
    """
    calculator = Calculator()
    
    print("Console-based Arithmetic Calculator")
    print("Enter a mathematical expression or type 'exit' to quit.")
    
    while True:
        try:
            expression = input("> ")
            if expression.lower() in ('exit', 'quit'):
                break
                
            result = calculator.calculate(expression)
            
            # Format the output (show as integer if it's a whole number)
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print("Calculator terminated.")


if __name__ == "__main__":
    main()
