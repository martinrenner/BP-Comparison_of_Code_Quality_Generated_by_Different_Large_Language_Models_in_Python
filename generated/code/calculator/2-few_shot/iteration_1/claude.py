class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    This calculator supports:
    - Basic operations: addition (+), subtraction (-), multiplication (*), division (/)
    - Parentheses for controlling operation order
    - Both integer and floating-point numbers (including negative values)
    - Proper operator precedence
    
    The implementation follows a recursive descent parsing approach for efficient
    and accurate expression evaluation.
    """
    
    def __init__(self):
        """Initialize the Calculator object."""
        # Allowed characters in a mathematical expression
        self.allowed_chars = set("0123456789+-*/().e ")
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression (str): The mathematical expression to evaluate.
            
        Returns:
            float: The result of the evaluation.
            
        Raises:
            ValueError: If the expression contains invalid characters or syntax.
            ZeroDivisionError: If the expression includes division by zero.
        """
        # Check if expression is empty
        if not expression or expression.isspace():
            raise ValueError("Expression cannot be empty")
        
        # Validate characters in the expression
        self._validate_characters(expression)
        
        # Remove spaces from the expression
        normalized_expr = expression.replace(" ", "")
        
        # Check for balanced parentheses
        if not self._is_balanced(normalized_expr):
            raise ValueError("Unbalanced parentheses in expression")
            
        # Parse and evaluate the expression
        result, _ = self._parse_expression(normalized_expr, 0)
        return result
    
    def _validate_characters(self, expression: str) -> None:
        """
        Validates that the expression contains only allowed characters.
        
        Args:
            expression (str): The expression to validate.
            
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        if not all(char in self.allowed_chars for char in expression):
            invalid_chars = [char for char in expression if char not in self.allowed_chars]
            raise ValueError(f"Expression contains invalid characters: {invalid_chars}")
    
    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether the expression has properly balanced parentheses.
        
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
        return not stack
    
    def _parse_expression(self, expression: str, index: int) -> tuple:
        """
        Recursively parses and evaluates the expression.
        
        This method implements a recursive descent parser for mathematical expressions.
        
        Args:
            expression (str): The expression being parsed.
            index (int): Current position in the expression.
            
        Returns:
            tuple: (result, new_index) where result is the evaluation result
                  and new_index is the position after parsing.
                  
        Raises:
            ValueError: If the expression has invalid syntax.
            ZeroDivisionError: If division by zero is attempted.
        """
        result, index = self._parse_term(expression, index)
        
        while index < len(expression):
            if expression[index] == '+':
                # Handle addition
                right_term, index = self._parse_term(expression, index + 1)
                result += right_term
            elif expression[index] == '-':
                # Handle subtraction
                right_term, index = self._parse_term(expression, index + 1)
                result -= right_term
            else:
                # If not + or -, we're done with this expression
                break
        
        return result, index
    
    def _parse_term(self, expression: str, index: int) -> tuple:
        """
        Parses and evaluates a term in the expression (multiplication/division).
        
        Args:
            expression (str): The expression being parsed.
            index (int): Current position in the expression.
            
        Returns:
            tuple: (result, new_index) where result is the evaluation result
                  and new_index is the position after parsing.
                  
        Raises:
            ValueError: If the expression has invalid syntax.
            ZeroDivisionError: If division by zero is attempted.
        """
        result, index = self._parse_factor(expression, index)
        
        while index < len(expression):
            if expression[index] == '*':
                # Handle multiplication
                right_factor, index = self._parse_factor(expression, index + 1)
                result *= right_factor
            elif expression[index] == '/':
                # Handle division
                right_factor, index = self._parse_factor(expression, index + 1)
                
                # Check for division by zero
                if right_factor == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                    
                result /= right_factor
            else:
                # If not * or /, we're done with this term
                break
        
        return result, index
    
    def _parse_factor(self, expression: str, index: int) -> tuple:
        """
        Parses and evaluates a factor in the expression (number or parenthesized expression).
        
        Args:
            expression (str): The expression being parsed.
            index (int): Current position in the expression.
            
        Returns:
            tuple: (result, new_index) where result is the evaluation result
                  and new_index is the position after parsing.
                  
        Raises:
            ValueError: If the expression has invalid syntax.
        """
        if index >= len(expression):
            raise ValueError("Unexpected end of expression")
            
        char = expression[index]
        
        if char == '(':
            # Handle parenthesized expression
            result, index = self._parse_expression(expression, index + 1)
            
            # Ensure the closing parenthesis is present
            if index < len(expression) and expression[index] == ')':
                return result, index + 1
            else:
                raise ValueError("Expected closing parenthesis")
                
        elif char.isdigit() or char == '.' or (char == '-' and (index == 0 or expression[index-1] in '(+-*/')):
            # Handle number (including negative numbers)
            return self._parse_number(expression, index)
            
        else:
            raise ValueError(f"Unexpected character '{char}' at position {index}")
    
    def _parse_number(self, expression: str, index: int) -> tuple:
        """
        Parses a numeric value from the expression.
        
        Args:
            expression (str): The expression being parsed.
            index (int): Current position in the expression.
            
        Returns:
            tuple: (number, new_index) where number is the parsed numeric value
                  and new_index is the position after the number.
                  
        Raises:
            ValueError: If the number format is invalid.
        """
        # Check if the number is negative
        is_negative = False
        if index < len(expression) and expression[index] == '-':
            is_negative = True
            index += 1
            
        # Extract digits before decimal point
        start_index = index
        while index < len(expression) and (expression[index].isdigit() or expression[index] == '.'):
            index += 1
            
        # If we didn't find any digits, this is an error
        if index == start_index and not is_negative:
            raise ValueError(f"Expected a number at position {start_index}")
            
        # If we only found a negative sign with no digits, this is an error
        if index == start_index and is_negative:
            raise ValueError(f"Expected a number after '-' at position {start_index - 1}")
            
        # Parse the number
        try:
            number = float(expression[start_index - (1 if is_negative else 0):index])
            return number, index
        except ValueError:
            raise ValueError(f"Invalid number format at position {start_index}")


def main():
    """
    Main function to demonstrate the calculator functionality.
    
    This provides a simple interface for testing the calculator.
    """
    calculator = Calculator()
    
    print("Console Calculator")
    print("Type 'exit' to quit")
    print("Enter expressions to calculate")
    print("Example: (2 + 3) * 4 - 5 / 2.5")
    
    while True:
        try:
            expression = input("\nEnter an expression: ")
            
            if expression.lower() == 'exit':
                print("Goodbye!")
                break
                
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
