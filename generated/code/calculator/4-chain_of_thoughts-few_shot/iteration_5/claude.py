class Calculator:
    """
    A calculator class that evaluates arithmetic expressions as strings.
    
    Supports operations:
    - Addition (+)
    - Subtraction (-)
    - Multiplication (*)
    - Division (/)
    - Parentheses for grouping
    
    Follows standard order of operations (PEMDAS).
    """
    
    def __init__(self):
        """Initialize the Calculator with no state."""
        pass

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression (str): The mathematical expression to evaluate.
            
        Returns:
            float: The result of the expression evaluation.
            
        Raises:
            ValueError: If the expression contains invalid characters or syntax.
            ZeroDivisionError: If the expression attempts division by zero.
            SyntaxError: If parentheses are unbalanced or expression is malformed.
        """
        # Normalize and validate the expression
        normalized_expr = self._normalize_expression(expression)
        
        # Check for balanced parentheses
        if not self._is_balanced_parentheses(normalized_expr):
            raise SyntaxError("Unbalanced parentheses in the expression")
        
        # Evaluate the expression
        result, remaining = self._evaluate_expression(normalized_expr)
        
        # Check if there's any remaining part of the expression that wasn't processed
        if remaining.strip():
            raise SyntaxError(f"Invalid syntax in expression: '{remaining}' couldn't be processed")
            
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.
        
        Args:
            expression (str): A mathematical expression as a string.
            
        Returns:
            str: The normalized expression without spaces.
            
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/()., ")
        if not all(char in allowed_chars for char in expression):
            invalid_chars = set(char for char in expression if char not in allowed_chars)
            raise ValueError(f"Expression contains invalid characters: {invalid_chars}")
        
        return expression.replace(" ", "")
    
    def _is_balanced_parentheses(self, expression: str) -> bool:
        """
        Checks whether a mathematical expression has properly paired parentheses.
        
        Args:
            expression (str): A string containing the mathematical expression.
            
        Returns:
            bool: True if parentheses are correctly paired, otherwise False.
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
    
    def _evaluate_expression(self, expression: str) -> tuple[float, str]:
        """
        Evaluates an arithmetic expression following order of operations.
        
        Args:
            expression (str): The normalized expression to evaluate.
            
        Returns:
            tuple: (result as float, remaining expression as string)
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ValueError: If the expression contains syntax errors.
        """
        return self._parse_addition_subtraction(expression)
    
    def _parse_addition_subtraction(self, expression: str) -> tuple[float, str]:
        """
        Parses and evaluates addition and subtraction operations.
        
        Args:
            expression (str): The expression to parse.
            
        Returns:
            tuple: (result as float, remaining expression as string)
        """
        left_value, expression = self._parse_multiplication_division(expression)
        
        while expression and expression[0] in ('+', '-'):
            operator = expression[0]
            expression = expression[1:]  # Consume the operator
            
            right_value, expression = self._parse_multiplication_division(expression)
            
            if operator == '+':
                left_value += right_value
            else:  # operator == '-'
                left_value -= right_value
                
        return left_value, expression
    
    def _parse_multiplication_division(self, expression: str) -> tuple[float, str]:
        """
        Parses and evaluates multiplication and division operations.
        
        Args:
            expression (str): The expression to parse.
            
        Returns:
            tuple: (result as float, remaining expression as string)
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
        """
        left_value, expression = self._parse_number_or_parenthesis(expression)
        
        while expression and expression[0] in ('*', '/'):
            operator = expression[0]
            expression = expression[1:]  # Consume the operator
            
            right_value, expression = self._parse_number_or_parenthesis(expression)
            
            if operator == '*':
                left_value *= right_value
            else:  # operator == '/'
                if right_value == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                left_value /= right_value
                
        return left_value, expression
    
    def _parse_number_or_parenthesis(self, expression: str) -> tuple[float, str]:
        """
        Parses a number or a parenthesized expression.
        
        Args:
            expression (str): The expression to parse.
            
        Returns:
            tuple: (result as float, remaining expression as string)
            
        Raises:
            ValueError: If the expression starts with an invalid token.
        """
        if not expression:
            raise ValueError("Unexpected end of expression")
            
        # Handle parenthesized expressions
        if expression[0] == '(':
            expression = expression[1:]  # Consume the opening parenthesis
            value, expression = self._parse_addition_subtraction(expression)
            
            if not expression or expression[0] != ')':
                raise SyntaxError("Missing closing parenthesis")
                
            expression = expression[1:]  # Consume the closing parenthesis
            return value, expression
            
        # Handle negative numbers
        if expression[0] == '-':
            expression = expression[1:]  # Consume the negative sign
            value, expression = self._parse_number_or_parenthesis(expression)
            return -value, expression
            
        # Parse a number
        return self._parse_number(expression)
    
    def _parse_number(self, expression: str) -> tuple[float, str]:
        """
        Parses a number from the beginning of an expression.
        
        Args:
            expression (str): The expression to parse.
            
        Returns:
            tuple: (number as float, remaining expression as string)
            
        Raises:
            ValueError: If the expression doesn't start with a valid number.
        """
        if not expression or not (expression[0].isdigit() or expression[0] == '.'):
            raise ValueError(f"Expected number, got '{expression}'")
            
        i = 0
        has_decimal = False
        
        # Handle digit part before decimal point
        while i < len(expression) and expression[i].isdigit():
            i += 1
            
        # Handle decimal point and digits after it
        if i < len(expression) and expression[i] == '.':
            has_decimal = True
            i += 1
            
            # Consume digits after decimal point
            while i < len(expression) and expression[i].isdigit():
                i += 1
        
        if i == 0 or (i == 1 and has_decimal):
            raise ValueError(f"Invalid number format in '{expression}'")
            
        number_str = expression[:i]
        remaining = expression[i:]
        
        try:
            return float(number_str), remaining
        except ValueError:
            raise ValueError(f"Invalid number format: '{number_str}'")
