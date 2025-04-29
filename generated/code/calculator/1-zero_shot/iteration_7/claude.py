class Calculator:
    """
    A calculator class that evaluates arithmetic expressions.
    
    This calculator handles addition, subtraction, multiplication, division,
    and supports parentheses while maintaining proper operator precedence.
    """
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression.
        
        Args:
            expression: A string containing an arithmetic expression
                        (e.g., "3 + 4 * (2 - 1)")
        
        Returns:
            float: The calculated result of the expression
            
        Raises:
            ValueError: If the expression contains invalid characters or has syntax errors
            ZeroDivisionError: If the expression attempts division by zero
            SyntaxError: If the expression has unbalanced parentheses
        """
        # Input validation and preparation
        self._validate_expression(expression)
        
        # Remove all spaces from the expression
        expression = expression.replace(" ", "")
        
        # Parse and evaluate the expression
        result, index = self._parse_expression(expression, 0)
        
        # Check if the entire expression was consumed
        if index < len(expression):
            raise ValueError(f"Invalid syntax at position {index}: '{expression[index:]}'")
            
        return result

    def _validate_expression(self, expression: str) -> None:
        """
        Validates the expression for proper syntax and characters.
        
        Args:
            expression: The arithmetic expression to validate
            
        Raises:
            ValueError: If the expression contains invalid characters
            SyntaxError: If the expression has unbalanced parentheses
        """
        # Check if the expression is empty
        if not expression or expression.isspace():
            raise ValueError("Expression cannot be empty")
            
        # Check for balanced parentheses
        open_count = 0
        for char in expression:
            if char == '(':
                open_count += 1
            elif char == ')':
                open_count -= 1
                if open_count < 0:
                    raise SyntaxError("Unbalanced parentheses: too many closing parentheses")
        
        if open_count > 0:
            raise SyntaxError("Unbalanced parentheses: missing closing parentheses")
            
        # Check for valid characters
        valid_chars = set("0123456789.+-*/() ")
        invalid_chars = []
        for char in expression:
            if char not in valid_chars:
                invalid_chars.append(char)
        
        if invalid_chars:
            raise ValueError(f"Invalid characters in expression: {', '.join(repr(c) for c in invalid_chars)}")

    def _parse_expression(self, expression: str, index: int) -> tuple:
        """
        Recursively parses and evaluates an arithmetic expression.
        
        Args:
            expression: The arithmetic expression to evaluate
            index: The current position in the expression
            
        Returns:
            tuple: (result, new_index) where result is the calculated value
                  and new_index is the position after the evaluated expression
        """
        return self._parse_addition_subtraction(expression, index)
    
    def _parse_addition_subtraction(self, expression: str, index: int) -> tuple:
        """
        Parses and evaluates addition and subtraction operations.
        
        Args:
            expression: The arithmetic expression
            index: The current position in the expression
            
        Returns:
            tuple: (result, new_index)
        """
        # Handle the left side (which may be multiplication/division)
        left_value, index = self._parse_multiplication_division(expression, index)
        
        # Continue parsing if we find + or -
        while index < len(expression) and expression[index] in ['+', '-']:
            operator = expression[index]
            index += 1
            
            # Handle the right side
            right_value, index = self._parse_multiplication_division(expression, index)
            
            # Apply the operation
            if operator == '+':
                left_value += right_value
            else:  # operator == '-'
                left_value -= right_value
                
        return left_value, index
    
    def _parse_multiplication_division(self, expression: str, index: int) -> tuple:
        """
        Parses and evaluates multiplication and division operations.
        
        Args:
            expression: The arithmetic expression
            index: The current position in the expression
            
        Returns:
            tuple: (result, new_index)
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
        """
        # Handle the left side (which may be a number or parenthesized expression)
        left_value, index = self._parse_factor(expression, index)
        
        # Continue parsing if we find * or /
        while index < len(expression) and expression[index] in ['*', '/']:
            operator = expression[index]
            index += 1
            
            # Handle the right side
            right_value, index = self._parse_factor(expression, index)
            
            # Apply the operation
            if operator == '*':
                left_value *= right_value
            else:  # operator == '/'
                if right_value == 0:
                    raise ZeroDivisionError("Division by zero")
                left_value /= right_value
                
        return left_value, index
    
    def _parse_factor(self, expression: str, index: int) -> tuple:
        """
        Parses and evaluates a factor, which can be a number, 
        a parenthesized expression, or a unary operation.
        
        Args:
            expression: The arithmetic expression
            index: The current position in the expression
            
        Returns:
            tuple: (result, new_index)
            
        Raises:
            ValueError: If an invalid number or expression is encountered
        """
        # Skip whitespace
        while index < len(expression) and expression[index].isspace():
            index += 1
            
        # Check for end of expression
        if index >= len(expression):
            raise ValueError("Unexpected end of expression")
            
        # Handle unary plus or minus
        if expression[index] in ['+', '-']:
            sign = -1 if expression[index] == '-' else 1
            index += 1
            value, index = self._parse_factor(expression, index)
            return sign * value, index
            
        # Handle parenthesized expressions
        if expression[index] == '(':
            index += 1  # Skip the opening parenthesis
            value, index = self._parse_expression(expression, index)
            
            # Ensure we have a closing parenthesis
            if index >= len(expression) or expression[index] != ')':
                raise ValueError("Missing closing parenthesis")
                
            index += 1  # Skip the closing parenthesis
            return value, index
            
        # Handle numbers
        start = index
        # Parse the integer part
        while index < len(expression) and expression[index].isdigit():
            index += 1
            
        # Handle decimal point and decimal part
        if index < len(expression) and expression[index] == '.':
            index += 1  # Skip the decimal point
            if not (index < len(expression) and expression[index].isdigit()):
                raise ValueError(f"Invalid decimal number at position {start}")
                
            while index < len(expression) and expression[index].isdigit():
                index += 1
                
        # Convert the substring to a number
        if start == index:
            raise ValueError(f"Expected a number at position {index}")
            
        try:
            return float(expression[start:index]), index
        except ValueError:
            raise ValueError(f"Invalid number format at position {start}: {expression[start:index]}")


def main():
    """
    Main function to run the calculator as a console application.
    """
    calculator = Calculator()
    
    print("Console-based Arithmetic Calculator")
    print("Type 'exit' or 'quit' to end the program")
    print("Enter an expression to calculate (e.g., '3 + 4 * (2 - 1)')")
    
    while True:
        try:
            expression = input("\n> ")
            
            if expression.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            if not expression:
                continue
                
            result = calculator.calculate(expression)
            
            # Format the output to remove unnecessary decimal places
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
