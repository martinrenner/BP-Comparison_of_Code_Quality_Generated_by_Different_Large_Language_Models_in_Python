class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions
    with support for basic operations and parentheses.
    
    Features:
    - Addition (+), subtraction (-), multiplication (*), and division (/)
    - Support for parentheses to alter order of operations
    - Decimal and negative number support
    - Input validation and appropriate error handling
    """

    def __init__(self):
        """Initialize the calculator."""
        self.valid_chars = set("0123456789+-*/().e ")

    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression (str): A mathematical expression as a string
                              (e.g., "3 + 4 * (2 - 1)")
        
        Returns:
            float: The calculated result of the expression
            
        Raises:
            ValueError: If the expression contains invalid characters,
                        has unbalanced parentheses, or has syntax errors
            ZeroDivisionError: If the expression attempts division by zero
        """
        # Validate and normalize the expression
        normalized_expr = self._normalize_expression(expression)
        
        # Evaluate the expression
        result = self._evaluate(normalized_expr)
        
        return result
    
    def _normalize_expression(self, expression: str) -> str:
        """
        Normalize a mathematical expression by removing spaces and validating characters.
        
        Args:
            expression (str): A mathematical expression as a string
            
        Returns:
            str: The normalized expression
            
        Raises:
            ValueError: If the expression contains invalid characters or has
                       unbalanced parentheses
        """
        # Validate characters
        if not all(char in self.valid_chars for char in expression):
            invalid_chars = set(char for char in expression 
                               if char not in self.valid_chars)
            raise ValueError(f"Expression contains invalid characters: {invalid_chars}")
        
        # Check for balanced parentheses
        if not self._is_balanced(expression):
            raise ValueError("Expression has unbalanced parentheses")
        
        # Remove spaces
        normalized = expression.replace(" ", "")
        
        # Validate the expression is not empty
        if not normalized:
            raise ValueError("Expression cannot be empty")
            
        return normalized
    
    def _is_balanced(self, expression: str) -> bool:
        """
        Check if parentheses are properly balanced in the expression.
        
        Args:
            expression (str): A mathematical expression
            
        Returns:
            bool: True if parentheses are balanced, False otherwise
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
    
    def _evaluate(self, expression: str) -> float:
        """
        Recursively evaluate a normalized mathematical expression.
        
        Args:
            expression (str): A normalized mathematical expression
            
        Returns:
            float: The calculated result
            
        Raises:
            ValueError: If the expression has syntax errors
            ZeroDivisionError: If the expression attempts division by zero
        """
        # If expression is empty, return 0
        if not expression:
            return 0
        
        # Handle parentheses first
        if '(' in expression:
            return self._handle_parentheses(expression)
        
        # Handle addition and subtraction
        return self._handle_addition_subtraction(expression)
    
    def _handle_parentheses(self, expression: str) -> float:
        """
        Handle expressions with parentheses by evaluating the innermost
        parenthesized expressions first.
        
        Args:
            expression (str): A mathematical expression
            
        Returns:
            float: The calculated result
        """
        # Find the position of the first closing parenthesis
        close_index = expression.find(')')
        if close_index == -1:
            raise ValueError("Invalid expression: missing closing parenthesis")
        
        # Find the matching opening parenthesis
        open_index = expression.rfind('(', 0, close_index)
        if open_index == -1:
            raise ValueError("Invalid expression: missing opening parenthesis")
        
        # Evaluate the sub-expression within the parentheses
        sub_result = self._evaluate(expression[open_index + 1:close_index])
        
        # Replace the parenthesized expression with its result and continue evaluation
        new_expression = (expression[:open_index] + 
                          str(sub_result) + 
                          expression[close_index + 1:])
        
        return self._evaluate(new_expression)
    
    def _handle_addition_subtraction(self, expression: str) -> float:
        """
        Handle addition and subtraction operations in the expression.
        
        Args:
            expression (str): A mathematical expression without parentheses
            
        Returns:
            float: The calculated result
        """
        # Skip if there are no addition or subtraction operators
        if '+' not in expression and '-' not in expression:
            return self._handle_multiplication_division(expression)
        
        # Process the expression from left to right, following order of operations
        result = 0
        i = 0
        current_term = ""
        current_op = "+"  # Default operation for the first term
        
        # Handle edge case where expression starts with a negative number
        if expression[0] == '-':
            current_term = "-"
            i = 1
        
        while i < len(expression):
            char = expression[i]
            
            # If we encounter an operator at the outer level
            if (char in ['+', '-'] and 
                not (i > 0 and expression[i-1] in ['e', 'E'])):  # Handle scientific notation
                
                # Evaluate the term based on the previous operation
                term_value = self._handle_multiplication_division(current_term)
                
                if current_op == "+":
                    result += term_value
                elif current_op == "-":
                    result -= term_value
                
                # Reset for the next term
                current_term = ""
                current_op = char
                
            else:
                current_term += char
                
            i += 1
        
        # Process the last term
        if current_term:
            term_value = self._handle_multiplication_division(current_term)
            if current_op == "+":
                result += term_value
            elif current_op == "-":
                result -= term_value
        
        return result
    
    def _handle_multiplication_division(self, expression: str) -> float:
        """
        Handle multiplication and division operations in the expression.
        
        Args:
            expression (str): A term without addition or subtraction
            
        Returns:
            float: The calculated result
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
        """
        # Skip if there are no multiplication or division operators
        if '*' not in expression and '/' not in expression:
            return self._parse_number(expression)
        
        # Split the expression into factors
        factors = []
        operations = []
        current_factor = ""
        
        i = 0
        while i < len(expression):
            char = expression[i]
            
            if char in ['*', '/']:
                if current_factor:
                    factors.append(current_factor)
                    current_factor = ""
                operations.append(char)
            else:
                current_factor += char
                
            i += 1
        
        # Add the last factor
        if current_factor:
            factors.append(current_factor)
        
        # Parse the first number
        result = self._parse_number(factors[0])
        
        # Apply operations in order
        for i, op in enumerate(operations):
            next_value = self._parse_number(factors[i + 1])
            
            if op == '*':
                result *= next_value
            elif op == '/':
                if next_value == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                result /= next_value
        
        return result
    
    def _parse_number(self, s: str) -> float:
        """
        Parse a string into a floating-point number.
        
        Args:
            s (str): A string representing a number
            
        Returns:
            float: The parsed number
            
        Raises:
            ValueError: If the string cannot be parsed as a number
        """
        if not s:
            raise ValueError("Expected a number but found an empty string")
            
        try:
            return float(s)
        except ValueError:
            raise ValueError(f"'{s}' is not a valid number")


# Example usage
if __name__ == "__main__":
    calc = Calculator()
    
    # Test cases
    test_expressions = [
        "2 + 3",              # Basic addition
        "5 - 2",              # Basic subtraction
        "3 * 4",              # Basic multiplication
        "10 / 2",             # Basic division
        "2 * (3 + 4)",        # Parentheses
        "10 / (2 * 5)",       # Division with parentheses
        "-5 + 10",            # Negative numbers
        "2.5 * 4",            # Decimal numbers
        "((2 + 3) * 4) / 5",  # Nested parentheses
        "1 + 2 + 3 + 4 + 5"   # Multiple operations
    ]
    
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"Error evaluating {expr}: {str(e)}")
