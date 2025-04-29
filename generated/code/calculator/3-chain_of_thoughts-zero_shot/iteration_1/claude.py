class Calculator:
    """
    A calculator class that evaluates arithmetic expressions following standard order of operations.
    
    Supported operations:
    - Addition (+)
    - Subtraction (-)
    - Multiplication (*)
    - Division (/)
    - Parentheses for grouping

    The calculator handles both integers and decimals, including negative numbers.
    """
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression and returns the result.
        
        Args:
            expression (str): The arithmetic expression to evaluate.
            
        Returns:
            float: The result of the evaluated expression.
            
        Raises:
            ValueError: If the expression contains invalid characters or has syntax errors.
            ZeroDivisionError: If the expression involves division by zero.
            SyntaxError: If the expression has unbalanced parentheses.
        """
        # Validate and preprocess the expression
        cleaned_expression = self._preprocess_expression(expression)
        
        # Parse and evaluate the expression
        result, remaining = self._parse_expression(cleaned_expression, 0)
        
        if remaining < len(cleaned_expression):
            raise ValueError(f"Unexpected character at position {remaining}: '{cleaned_expression[remaining]}'")
            
        return result
    
    def _preprocess_expression(self, expression: str) -> str:
        """
        Validates and preprocesses the expression by removing spaces and checking for invalid characters.
        
        Args:
            expression (str): The input expression.
            
        Returns:
            str: The preprocessed expression.
            
        Raises:
            ValueError: If the expression contains invalid characters.
            SyntaxError: If the expression has unbalanced parentheses.
        """
        # Remove all whitespace
        expression = expression.replace(" ", "")
        
        if not expression:
            raise ValueError("Expression cannot be empty")
        
        # Check for invalid characters
        valid_chars = set("0123456789.+-*/().")
        for i, char in enumerate(expression):
            if char not in valid_chars:
                raise ValueError(f"Invalid character at position {i}: '{char}'")
        
        # Check for balanced parentheses
        open_count = 0
        for i, char in enumerate(expression):
            if char == '(':
                open_count += 1
            elif char == ')':
                open_count -= 1
                if open_count < 0:
                    raise SyntaxError(f"Unbalanced parentheses: unexpected closing parenthesis at position {i}")
        
        if open_count > 0:
            raise SyntaxError("Unbalanced parentheses: missing closing parenthesis")
        
        return expression
    
    def _parse_expression(self, expression: str, start_pos: int) -> tuple[float, int]:
        """
        Recursively parses and evaluates an arithmetic expression from left to right.
        
        Args:
            expression (str): The expression to parse.
            start_pos (int): The starting position for parsing.
            
        Returns:
            tuple[float, int]: A tuple containing the result and the next position to parse.
        """
        left_value, current_pos = self._parse_term(expression, start_pos)
        
        while current_pos < len(expression):
            if expression[current_pos] == '+':
                right_value, current_pos = self._parse_term(expression, current_pos + 1)
                left_value += right_value
            elif expression[current_pos] == '-':
                right_value, current_pos = self._parse_term(expression, current_pos + 1)
                left_value -= right_value
            else:
                # Not an addition or subtraction operator, so we're done with this expression
                break
        
        return left_value, current_pos
    
    def _parse_term(self, expression: str, start_pos: int) -> tuple[float, int]:
        """
        Parses and evaluates a term (product or quotient) within an expression.
        
        Args:
            expression (str): The expression to parse.
            start_pos (int): The starting position for parsing.
            
        Returns:
            tuple[float, int]: A tuple containing the result and the next position to parse.
        """
        left_value, current_pos = self._parse_factor(expression, start_pos)
        
        while current_pos < len(expression):
            if expression[current_pos] == '*':
                right_value, current_pos = self._parse_factor(expression, current_pos + 1)
                left_value *= right_value
            elif expression[current_pos] == '/':
                right_value, current_pos = self._parse_factor(expression, current_pos + 1)
                if right_value == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                left_value /= right_value
            else:
                # Not a multiplication or division operator, so we're done with this term
                break
        
        return left_value, current_pos
    
    def _parse_factor(self, expression: str, start_pos: int) -> tuple[float, int]:
        """
        Parses and evaluates a factor (number, parenthesized expression, or unary operator) within an expression.
        
        Args:
            expression (str): The expression to parse.
            start_pos (int): The starting position for parsing.
            
        Returns:
            tuple[float, int]: A tuple containing the result and the next position to parse.
            
        Raises:
            ValueError: If there's an invalid number format.
        """
        current_pos = start_pos
        
        # Handle unary operators
        if current_pos < len(expression) and expression[current_pos] in '+-':
            sign = -1 if expression[current_pos] == '-' else 1
            value, current_pos = self._parse_factor(expression, current_pos + 1)
            return sign * value, current_pos
            
        # Handle parentheses
        if current_pos < len(expression) and expression[current_pos] == '(':
            value, current_pos = self._parse_expression(expression, current_pos + 1)
            
            # Ensure we have a closing parenthesis
            if current_pos >= len(expression) or expression[current_pos] != ')':
                raise SyntaxError(f"Missing closing parenthesis at position {current_pos}")
            
            return value, current_pos + 1
        
        # Handle numbers
        start_of_number = current_pos
        decimal_point_seen = False

        # Parse the number character by character
        while current_pos < len(expression):
            if expression[current_pos].isdigit():
                current_pos += 1
            elif expression[current_pos] == '.' and not decimal_point_seen:
                decimal_point_seen = True
                current_pos += 1
            else:
                break
                
        # Ensure we extracted a valid number
        if start_of_number == current_pos:
            raise ValueError(f"Expected a number at position {start_pos}")
            
        try:
            value = float(expression[start_of_number:current_pos])
            return value, current_pos
        except ValueError:
            raise ValueError(f"Invalid number format at position {start_of_number}")


def main():
    """
    Main function to demonstrate the Calculator class.
    """
    calculator = Calculator()
    
    try:
        # Example expressions
        expressions = [
            "2+3",
            "2.5 * 3",
            "10 / 2",
            "10 / (2 + 3)",
            "(2+3) * (4-1)",
            "-5 + 10",
            "3 * (2 + (-1))"
        ]
        
        for expr in expressions:
            result = calculator.calculate(expr)
            print(f"{expr} = {result}")
            
    except (ValueError, ZeroDivisionError, SyntaxError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
