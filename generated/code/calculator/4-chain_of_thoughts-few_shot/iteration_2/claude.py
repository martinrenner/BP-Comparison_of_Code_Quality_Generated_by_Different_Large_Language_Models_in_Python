class Calculator:
    """
    A calculator that evaluates arithmetic expressions with support for
    addition, subtraction, multiplication, division, and parentheses.
    
    The calculator implements proper order of operations (PEMDAS) and
    handles both integers and decimal numbers (including negative numbers).
    """
    
    def __init__(self):
        """Initialize the calculator."""
        # Valid characters in expressions
        self.allowed_chars = set("0123456789+-*/().e ")
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression (str): The arithmetic expression to evaluate.
            
        Returns:
            float: The calculated result.
            
        Raises:
            ValueError: If the expression contains invalid characters or is malformed.
            ZeroDivisionError: If the expression attempts division by zero.
        """
        # Validate and normalize the expression
        normalized_expr = self._normalize_expression(expression)
        
        # Check for balanced parentheses
        if not self._is_balanced_parentheses(normalized_expr):
            raise ValueError("Unbalanced parentheses in the expression.")
        
        # Evaluate the expression
        result = self._evaluate_expression(normalized_expr)
        return result
    
    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes an expression by removing spaces and validating characters.
        
        Args:
            expression (str): The expression to normalize.
            
        Returns:
            str: The normalized expression.
            
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Check for invalid characters
        if not all(char in self.allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")
        
        # Replace spaces and handle unary minus operations
        normalized = expression.replace(" ", "")
        
        # Handle cases like "(-5)" or "5*(-3)" by replacing them with "(0-5)" or "5*(0-3)"
        i = 0
        result = ""
        while i < len(normalized):
            if normalized[i] == '(' and i + 1 < len(normalized) and normalized[i+1] == '-':
                result += "(0"
                i += 1  # Skip the opening parenthesis, next iteration will handle the minus
            elif i > 0 and normalized[i] == '-' and normalized[i-1] in "*/+(":
                result += "0"  # Insert a 0 before a negative number when it follows an operator or opening parenthesis
                result += normalized[i]
                i += 1
            else:
                result += normalized[i]
                i += 1
        
        return result
    
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
    
    def _evaluate_expression(self, expression: str) -> float:
        """
        Recursively evaluates an arithmetic expression.
        
        Args:
            expression (str): The expression to evaluate.
            
        Returns:
            float: The result of the evaluation.
            
        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If division by zero is attempted.
        """
        # Base case: empty expression
        if not expression:
            raise ValueError("Empty expression or subexpression.")
            
        return self._parse_addition_subtraction(expression, 0)[0]
    
    def _parse_addition_subtraction(self, expression: str, index: int) -> tuple[float, int]:
        """
        Parses addition and subtraction operations.
        
        Args:
            expression (str): The expression to parse.
            index (int): The current position in the expression.
            
        Returns:
            tuple[float, int]: The result and the new position in the expression.
        """
        left_value, index = self._parse_multiplication_division(expression, index)
        
        while index < len(expression):
            if expression[index] == '+':
                right_value, index = self._parse_multiplication_division(expression, index + 1)
                left_value += right_value
            elif expression[index] == '-':
                right_value, index = self._parse_multiplication_division(expression, index + 1)
                left_value -= right_value
            else:
                break
                
        return left_value, index
    
    def _parse_multiplication_division(self, expression: str, index: int) -> tuple[float, int]:
        """
        Parses multiplication and division operations.
        
        Args:
            expression (str): The expression to parse.
            index (int): The current position in the expression.
            
        Returns:
            tuple[float, int]: The result and the new position in the expression.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
        """
        left_value, index = self._parse_term(expression, index)
        
        while index < len(expression):
            if expression[index] == '*':
                right_value, index = self._parse_term(expression, index + 1)
                left_value *= right_value
            elif expression[index] == '/':
                right_value, index = self._parse_term(expression, index + 1)
                if right_value == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                left_value /= right_value
            else:
                break
                
        return left_value, index
    
    def _parse_term(self, expression: str, index: int) -> tuple[float, int]:
        """
        Parses a term (number or parenthesized expression).
        
        Args:
            expression (str): The expression to parse.
            index (int): The current position in the expression.
            
        Returns:
            tuple[float, int]: The value of the term and the new position.
            
        Raises:
            ValueError: If the term is invalid.
        """
        # Skip whitespace
        while index < len(expression) and expression[index].isspace():
            index += 1
            
        # Check if we're at the end of the expression
        if index >= len(expression):
            raise ValueError("Unexpected end of expression.")
            
        # Handle opening parenthesis
        if expression[index] == '(':
            value, index = self._parse_addition_subtraction(expression, index + 1)
            
            # Skip the closing parenthesis
            if index < len(expression) and expression[index] == ')':
                return value, index + 1
            else:
                raise ValueError("Missing closing parenthesis.")
                
        # Handle numbers (including decimals and scientific notation)
        if expression[index].isdigit() or expression[index] == '.':
            # Extract the numeric string
            start = index
            has_decimal = expression[index] == '.'
            has_exponent = False
            
            index += 1
            while index < len(expression):
                if expression[index].isdigit():
                    index += 1
                elif expression[index] == '.' and not has_decimal:
                    has_decimal = True
                    index += 1
                elif expression[index].lower() == 'e' and not has_exponent:
                    # Handle scientific notation
                    has_exponent = True
                    index += 1
                    # Allow for +/- after the 'e'
                    if index < len(expression) and (expression[index] == '+' or expression[index] == '-'):
                        index += 1
                else:
                    break
            
            try:
                value = float(expression[start:index])
                return value, index
            except ValueError:
                raise ValueError(f"Invalid number format: {expression[start:index]}")
        
        raise ValueError(f"Unexpected character at position {index}: '{expression[index]}'")


def main():
    """Main function to run the calculator interactively."""
    calculator = Calculator()
    
    print("Console Calculator")
    print("Enter 'quit' or 'exit' to terminate")
    print("Example: 2 * (3 + 4) - 5 / 2.5")
    
    while True:
        expression = input("\nEnter an expression: ")
        
        if expression.lower() in ['quit', 'exit']:
            print("Calculator terminated.")
            break
            
        try:
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
