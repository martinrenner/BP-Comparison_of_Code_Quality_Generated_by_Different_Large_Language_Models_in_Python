class Calculator:
    """
    A calculator that evaluates arithmetic expressions with proper operator precedence.
    
    Supports:
    - Addition, subtraction, multiplication, and division
    - Parentheses for expression grouping
    - Negative and decimal numbers
    - Proper error handling without using eval()
    """
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression and returns the result.
        
        Args:
            expression: A string containing a valid arithmetic expression
            
        Returns:
            The calculated result as a float
            
        Raises:
            ValueError: If the expression contains invalid characters or syntax
            ZeroDivisionError: If the expression attempts division by zero
            SyntaxError: If the expression has unbalanced parentheses
        """
        # Remove all whitespace from the expression
        expression = expression.replace(" ", "")
        
        if not expression:
            raise ValueError("Expression cannot be empty")
            
        # Validate the expression contains only valid characters
        self._validate_characters(expression)
        
        # Check for balanced parentheses
        self._validate_parentheses(expression)
        
        # Perform the actual calculation
        return self._evaluate_expression(expression)
    
    def _validate_characters(self, expression: str) -> None:
        """
        Validates that the expression only contains allowed characters.
        
        Args:
            expression: The expression to validate
            
        Raises:
            ValueError: If the expression contains invalid characters
        """
        valid_chars = set("0123456789.+-*/() ")
        invalid_chars = [char for char in expression if char not in valid_chars]
        
        if invalid_chars:
            raise ValueError(f"Expression contains invalid characters: {''.join(invalid_chars)}")
            
        # Check for syntax errors like consecutive operators
        self._validate_syntax(expression)
    
    def _validate_syntax(self, expression: str) -> None:
        """
        Validates the syntax of the expression.
        
        Args:
            expression: The expression to validate
            
        Raises:
            ValueError: If the expression has syntax errors
        """
        # Check for consecutive operators (except when - is used for negative numbers)
        for i in range(1, len(expression)):
            if (expression[i] in "+-*/") and (expression[i-1] in "+-*/") and not (
                    expression[i] == '-' and (expression[i-1] in "+-*/(" or i == 0)):
                raise ValueError(f"Invalid syntax: consecutive operators at position {i}")
                
        # Check for proper decimal point usage
        self._validate_decimal_points(expression)
    
    def _validate_decimal_points(self, expression: str) -> None:
        """
        Validates proper usage of decimal points in numbers.
        
        Args:
            expression: The expression to validate
            
        Raises:
            ValueError: If decimal points are used incorrectly
        """
        i = 0
        while i < len(expression):
            if expression[i] == '.':
                # Check if the decimal point has digits before or after it
                has_digit_before = i > 0 and expression[i-1].isdigit()
                has_digit_after = i < len(expression) - 1 and expression[i+1].isdigit()
                
                if not (has_digit_before or has_digit_after):
                    raise ValueError(f"Invalid decimal point at position {i}")
                
                # Check for multiple decimal points in a number
                if has_digit_before:
                    j = i - 1
                    while j >= 0 and expression[j].isdigit():
                        j -= 1
                    if j >= 0 and expression[j] == '.':
                        raise ValueError(f"Multiple decimal points in a number near position {i}")
            i += 1
    
    def _validate_parentheses(self, expression: str) -> None:
        """
        Validates that parentheses in the expression are balanced.
        
        Args:
            expression: The expression to validate
            
        Raises:
            SyntaxError: If parentheses are unbalanced
        """
        stack = []
        
        for i, char in enumerate(expression):
            if char == '(':
                stack.append(i)
            elif char == ')':
                if not stack:
                    raise SyntaxError(f"Unbalanced closing parenthesis at position {i}")
                stack.pop()
                
        if stack:
            raise SyntaxError(f"Unbalanced opening parenthesis at position {stack[0]}")
    
    def _evaluate_expression(self, expression: str) -> float:
        """
        Evaluates the expression using a recursive descent parser.
        
        Args:
            expression: The validated expression to evaluate
            
        Returns:
            The result of the expression
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: For other calculation errors
        """
        # Parse the expression
        result, _ = self._parse_addition(expression, 0)
        return result
    
    def _parse_addition(self, expression: str, index: int) -> tuple[float, int]:
        """
        Parses addition and subtraction operations.
        
        Args:
            expression: The expression to parse
            index: The current index in the expression
            
        Returns:
            A tuple containing (result, new_index)
        """
        left, index = self._parse_multiplication(expression, index)
        
        while index < len(expression) and expression[index] in ['+', '-']:
            operator = expression[index]
            index += 1
            right, index = self._parse_multiplication(expression, index)
            
            if operator == '+':
                left += right
            else:  # operator == '-'
                left -= right
                
        return left, index
    
    def _parse_multiplication(self, expression: str, index: int) -> tuple[float, int]:
        """
        Parses multiplication and division operations.
        
        Args:
            expression: The expression to parse
            index: The current index in the expression
            
        Returns:
            A tuple containing (result, new_index)
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
        """
        left, index = self._parse_unary(expression, index)
        
        while index < len(expression) and expression[index] in ['*', '/']:
            operator = expression[index]
            index += 1
            right, index = self._parse_unary(expression, index)
            
            if operator == '*':
                left *= right
            else:  # operator == '/'
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                left /= right
                
        return left, index
    
    def _parse_unary(self, expression: str, index: int) -> tuple[float, int]:
        """
        Parses unary operations (+ and -).
        
        Args:
            expression: The expression to parse
            index: The current index in the expression
            
        Returns:
            A tuple containing (result, new_index)
        """
        if index < len(expression) and expression[index] == '+':
            # Unary plus does nothing
            return self._parse_primary(expression, index + 1)
        elif index < len(expression) and expression[index] == '-':
            # Unary minus negates the value
            value, new_index = self._parse_primary(expression, index + 1)
            return -value, new_index
        else:
            return self._parse_primary(expression, index)
    
    def _parse_primary(self, expression: str, index: int) -> tuple[float, int]:
        """
        Parses primary expressions (numbers or parenthesized expressions).
        
        Args:
            expression: The expression to parse
            index: The current index in the expression
            
        Returns:
            A tuple containing (result, new_index)
            
        Raises:
            ValueError: If the expression is invalid
        """
        if index >= len(expression):
            raise ValueError("Unexpected end of expression")
            
        # Handle parentheses
        if expression[index] == '(':
            result, index = self._parse_addition(expression, index + 1)
            
            if index >= len(expression) or expression[index] != ')':
                raise ValueError("Expected closing parenthesis")
                
            return result, index + 1
            
        # Handle numbers
        start = index
        decimal_point = False
        
        # Handle sign as part of the number if it's at the beginning
        if index < len(expression) and expression[index] in ['+', '-']:
            index += 1
            
        # Parse the rest of the number
        while index < len(expression) and (expression[index].isdigit() or expression[index] == '.'):
            if expression[index] == '.':
                if decimal_point:
                    raise ValueError(f"Multiple decimal points in a number at position {index}")
                decimal_point = True
            index += 1
            
        if index == start:
            raise ValueError(f"Expected number at position {index}")
            
        try:
            return float(expression[start:index]), index
        except ValueError:
            raise ValueError(f"Invalid number format: {expression[start:index]}")


def main():
    """
    Main function to run the calculator interactively.
    """
    calculator = Calculator()
    
    print("Console Calculator")
    print("Enter 'exit' to quit")
    
    while True:
        try:
            expression = input("\nEnter an expression: ")
            
            if expression.lower() == 'exit':
                break
                
            result = calculator.calculate(expression)
            
            # Format the result to remove trailing zeros for whole numbers
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except (ValueError, SyntaxError, ZeroDivisionError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
