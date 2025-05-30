class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    This calculator supports:
    - Basic operations: addition (+), subtraction (-), multiplication (*), division (/)
    - Parentheses for specifying operation order
    - Decimal and negative numbers
    """
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result.
        
        Args:
            expression: A string containing a mathematical expression
            
        Returns:
            The calculated result as a float
            
        Raises:
            ValueError: If the expression contains invalid characters or syntax
            ZeroDivisionError: If the expression attempts to divide by zero
            SyntaxError: If the expression has unbalanced parentheses
        """
        # Remove all whitespace from the expression
        expression = expression.replace(" ", "")
        
        # Basic validation
        if not expression:
            raise ValueError("Empty expression")
            
        self._validate_characters(expression)
        self._validate_parentheses(expression)
        
        # Evaluate the expression
        result, _ = self._evaluate_expression(expression, 0)
        return result
        
    def _validate_characters(self, expression: str) -> None:
        """
        Validates that the expression only contains allowed characters.
        
        Args:
            expression: The expression to validate
            
        Raises:
            ValueError: If invalid characters are detected
        """
        allowed_chars = "0123456789.+-*/() "
        for char in expression:
            if char not in allowed_chars:
                raise ValueError(f"Invalid character in expression: '{char}'")
        
    def _validate_parentheses(self, expression: str) -> None:
        """
        Validates that parentheses are balanced in the expression.
        
        Args:
            expression: The expression to validate
            
        Raises:
            SyntaxError: If parentheses are unbalanced
        """
        stack = 0
        for char in expression:
            if char == '(':
                stack += 1
            elif char == ')':
                stack -= 1
                if stack < 0:
                    raise SyntaxError("Unbalanced parentheses: too many closing parentheses")
        
        if stack > 0:
            raise SyntaxError("Unbalanced parentheses: missing closing parentheses")
            
    def _evaluate_expression(self, expression: str, start_index: int) -> tuple[float, int]:
        """
        Recursively evaluates an expression.
        
        Args:
            expression: The expression to evaluate
            start_index: The starting index for evaluation
            
        Returns:
            A tuple containing (result, ending_index)
            
        Raises:
            ValueError: For invalid expressions
            ZeroDivisionError: When dividing by zero
        """
        operators = []  # Stores operators (+, -, *, /)
        values = []     # Stores numeric values and subexpression results
        
        i = start_index
        # Value holder for multi-digit number processing
        current_number = ""
        # Flag indicating if we're expecting an operand
        expecting_operand = True
        
        while i < len(expression):
            char = expression[i]
            
            # Handle different character types
            if char.isdigit() or char == '.':
                # Build up a number (can be multi-digit or decimal)
                current_number += char
                i += 1
                expecting_operand = False
                
            elif char in '+-' and expecting_operand:
                # Handle unary operators (+ or - at the beginning or after another operator)
                current_number += char
                i += 1
                
            elif char in '+-*/':
                # Process any built-up number before handling the operator
                if current_number:
                    try:
                        values.append(float(current_number))
                        current_number = ""
                    except ValueError:
                        raise ValueError(f"Invalid number format: {current_number}")
                
                # Process operators based on precedence
                while (operators and
                      ((char in '+-' and operators[-1] in '+-*/') or 
                       (char in '*/' and operators[-1] in '*/'))
                      ):
                    self._apply_operator(operators, values)
                
                operators.append(char)
                i += 1
                expecting_operand = True
                
            elif char == '(':
                # Recursively evaluate the subexpression inside parentheses
                subexpr_value, next_idx = self._evaluate_expression(expression, i + 1)
                values.append(subexpr_value)
                i = next_idx
                expecting_operand = False
                
            elif char == ')':
                # End of the current subexpression
                break
                
            else:
                i += 1
        
        # Process any remaining number
        if current_number:
            try:
                values.append(float(current_number))
            except ValueError:
                raise ValueError(f"Invalid number format: {current_number}")
        
        # Apply any remaining operators
        while operators:
            self._apply_operator(operators, values)
        
        # If no values were processed, raise an error
        if not values:
            raise ValueError("Invalid expression: no values found")
            
        # Return the result and the ending index
        return values[0], i + 1
    
    def _apply_operator(self, operators: list, values: list) -> None:
        """
        Applies an operation to the last two values in the values list.
        
        Args:
            operators: List of operators
            values: List of values
            
        Raises:
            ZeroDivisionError: When dividing by zero
            ValueError: When there are not enough operands for an operation
        """
        if len(values) < 2:
            raise ValueError("Invalid expression: not enough operands")
            
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        
        if operator == '+':
            values.append(left + right)
        elif operator == '-':
            values.append(left - right)
        elif operator == '*':
            values.append(left * right)
        elif operator == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            values.append(left / right)


# Example usage:
if __name__ == "__main__":
    calculator = Calculator()
    
    try:
        # Test cases
        test_cases = [
            "2+3",
            "3.5 * 2",
            "10 - (4 + 2)",
            "3 * (4 + 2) / 3",
            "-5 + 10",
            "2 * (-3 + 4)",
            "10 / (2 * 5)",
            "(2 + 3) * (4 - 2)",
        ]
        
        for expr in test_cases:
            result = calculator.calculate(expr)
            print(f"{expr} = {result}")
            
    except (ValueError, ZeroDivisionError, SyntaxError) as e:
        print(f"Error: {e}")
