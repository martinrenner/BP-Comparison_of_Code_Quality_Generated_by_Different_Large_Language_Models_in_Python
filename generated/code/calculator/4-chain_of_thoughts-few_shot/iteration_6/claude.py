class Calculator:
    """
    A calculator class that evaluates arithmetic expressions following the order of operations.
    Supports addition, subtraction, multiplication, division, and parentheses.
    """
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression (str): A string containing the mathematical expression to evaluate.
            
        Returns:
            float: The result of the evaluated expression.
            
        Raises:
            ValueError: If the expression contains invalid characters or has syntax errors.
            ZeroDivisionError: If the expression attempts to divide by zero.
            SyntaxError: If the expression has unbalanced parentheses or other syntax issues.
        """
        # Validate and normalize the expression
        normalized_expr = self._normalize_expression(expression)
        
        # Check if parentheses are balanced
        if not self._is_balanced_parentheses(normalized_expr):
            raise SyntaxError("Unbalanced parentheses in the expression")
        
        # Evaluate the expression
        result, remaining = self._evaluate_expression(normalized_expr)
        
        # Check if the entire expression was processed
        if remaining and remaining.strip():
            raise SyntaxError(f"Invalid syntax: unable to process '{remaining}'")
            
        return result
    
    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.
        
        Args:
            expression (str): The expression to normalize.
            
        Returns:
            str: The normalized expression.
            
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/()., ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters")
            
        # Replace commas with dots for decimal points
        normalized = expression.replace(',', '.')
        
        # Remove spaces
        normalized = normalized.replace(' ', '')
        
        # Handle cases like "5(" to become "5*("
        result = ""
        for i in range(len(normalized)):
            result += normalized[i]
            if i < len(normalized) - 1:
                if (normalized[i].isdigit() or normalized[i] == ')') and normalized[i+1] == '(':
                    result += '*'
        
        return result
    
    def _is_balanced_parentheses(self, expression: str) -> bool:
        """
        Checks if the parentheses in the expression are correctly balanced.
        
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
    
    def _evaluate_expression(self, expression: str) -> tuple[float, str]:
        """
        Evaluates a mathematical expression following the order of operations (PEMDAS).
        
        Args:
            expression (str): The expression to evaluate.
            
        Returns:
            tuple[float, str]: The result of the evaluation and any remaining part of the expression.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ValueError: If the expression contains syntax errors.
        """
        # Parse and evaluate the terms (addition and subtraction)
        return self._parse_addition_subtraction(expression)
    
    def _parse_addition_subtraction(self, expression: str) -> tuple[float, str]:
        """
        Parses and evaluates terms in an expression (addition and subtraction).
        
        Args:
            expression (str): The expression to evaluate.
            
        Returns:
            tuple[float, str]: The result of the evaluation and any remaining part of the expression.
        """
        # First, parse multiplication and division
        left_val, remaining = self._parse_multiplication_division(expression)
        
        while remaining and remaining[0] in ('+', '-'):
            operator = remaining[0]
            right_expr = remaining[1:]
            
            # Evaluate the right side of the operator
            right_val, remaining = self._parse_multiplication_division(right_expr)
            
            # Apply the operator
            if operator == '+':
                left_val += right_val
            else:  # operator == '-'
                left_val -= right_val
        
        return left_val, remaining
    
    def _parse_multiplication_division(self, expression: str) -> tuple[float, str]:
        """
        Parses and evaluates factors in an expression (multiplication and division).
        
        Args:
            expression (str): The expression to evaluate.
            
        Returns:
            tuple[float, str]: The result of the evaluation and any remaining part of the expression.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
        """
        # First, parse individual factors (numbers, parenthesized expressions)
        left_val, remaining = self._parse_factor(expression)
        
        while remaining and remaining[0] in ('*', '/'):
            operator = remaining[0]
            right_expr = remaining[1:]
            
            # Evaluate the right side of the operator
            right_val, remaining = self._parse_factor(right_expr)
            
            # Apply the operator
            if operator == '*':
                left_val *= right_val
            else:  # operator == '/'
                if right_val == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                left_val /= right_val
        
        return left_val, remaining
    
    def _parse_factor(self, expression: str) -> tuple[float, str]:
        """
        Parses and evaluates a factor in the expression (number or parenthesized expression).
        
        Args:
            expression (str): The expression to evaluate.
            
        Returns:
            tuple[float, str]: The value of the factor and the remaining expression.
            
        Raises:
            ValueError: If the factor has an invalid format.
        """
        if not expression:
            raise ValueError("Empty expression or term")
        
        # Check for parenthesized expressions
        if expression[0] == '(':
            # Find the matching closing parenthesis
            result, remaining = self._evaluate_expression(expression[1:])
            
            # Ensure the next character is the closing parenthesis
            if not remaining or remaining[0] != ')':
                raise SyntaxError("Missing closing parenthesis")
            
            return result, remaining[1:]
        
        # Check for negative numbers indicated by leading minus
        if expression[0] == '-':
            # Handle negative number
            value, remaining = self._parse_factor(expression[1:])
            return -value, remaining
        
        # Parse a number
        return self._parse_number(expression)
    
    def _parse_number(self, expression: str) -> tuple[float, str]:
        """
        Parses a numeric value from the beginning of the expression.
        
        Args:
            expression (str): The expression to parse.
            
        Returns:
            tuple[float, str]: The numeric value and the remaining expression.
            
        Raises:
            ValueError: If no valid number is found at the beginning of the expression.
        """
        if not expression or not (expression[0].isdigit() or expression[0] == '.'):
            raise ValueError(f"Expected a number, but got '{expression}'")
        
        i = 0
        has_decimal = False
        
        # Handle the integer part and/or decimal point
        while i < len(expression) and (expression[i].isdigit() or (expression[i] == '.' and not has_decimal)):
            if expression[i] == '.':
                has_decimal = True
            i += 1
        
        if i == 0 or (i == 1 and expression[0] == '.'):
            raise ValueError(f"Invalid number format in '{expression}'")
        
        number_str = expression[:i]
        remaining = expression[i:]
        
        try:
            return float(number_str), remaining
        except ValueError:
            raise ValueError(f"Invalid number format: '{number_str}'")


def main():
    """
    Main function to run the calculator interactively.
    """
    calculator = Calculator()
    print("Console Calculator - Type 'exit' to quit")
    print("Supported operations: +, -, *, /, and parentheses")
    
    while True:
        expression = input("\nEnter an expression: ")
        if expression.lower() == 'exit':
            print("Goodbye!")
            break
        
        try:
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
