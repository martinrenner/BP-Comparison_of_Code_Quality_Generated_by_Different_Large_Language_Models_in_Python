class Calculator:
    """
    A calculator class that evaluates arithmetic expressions.
    
    Supports operations: addition (+), subtraction (-), multiplication (*), division (/)
    Handles parentheses and follows proper order of operations.
    """
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression and returns the result.
        
        Args:
            expression (str): The arithmetic expression to evaluate.
            
        Returns:
            float: The result of the expression.
            
        Raises:
            ValueError: If the expression contains invalid characters or is malformed.
            ZeroDivisionError: If the expression attempts to divide by zero.
            SyntaxError: If the parentheses in the expression are unbalanced.
        """
        # Remove all whitespace from the expression
        expression = expression.replace(" ", "")
        
        if not expression:
            raise ValueError("Expression cannot be empty")
            
        # Check for invalid characters
        valid_chars = set("0123456789.+-*/() ")
        if not all(c in valid_chars for c in expression):
            raise ValueError("Expression contains invalid characters")
            
        # Check for balanced parentheses
        if not self._are_parentheses_balanced(expression):
            raise SyntaxError("Unbalanced parentheses in expression")
        
        # Evaluate the expression
        result = self._evaluate_expression(expression)
        return result
    
    def _are_parentheses_balanced(self, expression: str) -> bool:
        """
        Check if parentheses in the expression are balanced.
        
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
        Evaluates an arithmetic expression following order of operations.
        
        Args:
            expression (str): The expression to evaluate.
            
        Returns:
            float: The result of the expression.
            
        Raises:
            ValueError: If the expression is invalid.
            ZeroDivisionError: If division by zero is attempted.
        """
        # Handle empty expression
        if not expression:
            return 0.0
        
        # First, handle expressions inside parentheses
        if '(' in expression:
            return self._handle_parentheses(expression)
        
        # Then, handle addition and subtraction
        return self._handle_addition_subtraction(expression)
    
    def _handle_parentheses(self, expression: str) -> float:
        """
        Handles expressions with parentheses by evaluating the innermost
        parentheses first and replacing them with their result.
        
        Args:
            expression (str): The expression containing parentheses.
            
        Returns:
            float: The result after evaluating all parenthesized expressions.
        """
        # Find the first closing parenthesis
        close_index = expression.find(')')
        if close_index == -1:
            raise SyntaxError("Unbalanced parentheses")
        
        # Find its matching opening parenthesis
        open_index = expression.rfind('(', 0, close_index)
        if open_index == -1:
            raise SyntaxError("Unbalanced parentheses")
        
        # Evaluate the expression inside these parentheses
        inner_result = self._evaluate_expression(expression[open_index + 1:close_index])
        
        # Replace the parenthesized expression with its result
        # Handle negative results carefully
        if inner_result < 0 and open_index > 0 and expression[open_index - 1] not in "+-*/(" and expression[close_index + 1:close_index + 2] not in "+-*/)":
            # If negative and not after an operator, wrap in parentheses to preserve order
            new_expression = (expression[:open_index] + 
                              str(inner_result) + 
                              expression[close_index + 1:])
        else:
            new_expression = (expression[:open_index] + 
                              str(inner_result) + 
                              expression[close_index + 1:])
            
        # Continue evaluating the modified expression
        return self._evaluate_expression(new_expression)
    
    def _handle_addition_subtraction(self, expression: str) -> float:
        """
        Handles addition and subtraction operations in the expression.
        
        Args:
            expression (str): The expression to evaluate.
            
        Returns:
            float: The result after applying addition and subtraction.
        """
        # First, evaluate all multiplication and division
        terms = self._split_by_operators(expression, "+-")
        
        # Process the first term (which might have a leading + or -)
        if expression.startswith('+'):
            result = self._handle_multiplication_division(terms[1])
            terms = terms[2:]
            operators = expression[1:2]  # Skip the first operator
        elif expression.startswith('-'):
            result = -self._handle_multiplication_division(terms[1])
            terms = terms[2:]
            operators = expression[1:2]  # Skip the first operator
        else:
            result = self._handle_multiplication_division(terms[0])
            terms = terms[1:]
            operators = expression  # Will be filtered to get just operators
        
        # Collect operators (+ or -) by scanning the expression
        operators = [op for op in operators if op in "+-"]
        
        # Apply each operation in sequence
        for i, term in enumerate(terms):
            if i < len(operators):
                if operators[i] == '+':
                    result += self._handle_multiplication_division(term)
                else:  # operators[i] == '-'
                    result -= self._handle_multiplication_division(term)
                    
        return result
    
    def _handle_multiplication_division(self, expression: str) -> float:
        """
        Handles multiplication and division operations in the expression.
        
        Args:
            expression (str): The expression to evaluate.
            
        Returns:
            float: The result after applying multiplication and division.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
        """
        if not expression:
            return 0.0
            
        # Split the expression by * and /
        terms = self._split_by_operators(expression, "*/")
        
        # If there's only one term, convert it to a number
        if len(terms) == 1:
            return self._parse_number(terms[0])
        
        # Start with the first term
        result = self._parse_number(terms[0])
        
        # Collect operators (* or /) by scanning the expression
        operators = [char for char in expression if char in "*/"]
        
        # Apply each operation in sequence
        for i in range(1, len(terms)):
            if i-1 < len(operators):
                if operators[i-1] == '*':
                    result *= self._parse_number(terms[i])
                else:  # operators[i-1] == '/'
                    divisor = self._parse_number(terms[i])
                    if divisor == 0:
                        raise ZeroDivisionError("Division by zero")
                    result /= divisor
                    
        return result
    
    def _split_by_operators(self, expression: str, operators: str) -> list:
        """
        Splits an expression by the specified operators while preserving the
        structure of the expression.
        
        Args:
            expression (str): The expression to split.
            operators (str): A string containing the operators to split by.
            
        Returns:
            list: List of subexpressions.
        """
        result = []
        current_term = ""
        
        i = 0
        while i < len(expression):
            current_char = expression[i]
            
            # If we found an operator (and it's not the first character or 
            # we're checking for +-)
            if current_char in operators and (i != 0 or operators not in "+-"):
                if current_term:
                    result.append(current_term)
                    current_term = ""
            else:
                current_term += current_char
            
            i += 1
            
        if current_term:
            result.append(current_term)
            
        return result
    
    def _parse_number(self, number_str: str) -> float:
        """
        Parses a string representation of a number into a float.
        
        Args:
            number_str (str): String representation of the number.
            
        Returns:
            float: The parsed number.
            
        Raises:
            ValueError: If the string cannot be parsed as a number.
        """
        try:
            return float(number_str)
        except ValueError:
            raise ValueError(f"Invalid number format: '{number_str}'")


def main():
    """
    Main function to run the calculator interactively.
    """
    calculator = Calculator()
    
    print("Console Calculator - Enter 'exit' to quit")
    print("Supported operations: +, -, *, / and parentheses")
    
    while True:
        try:
            expression = input("\nEnter an expression: ")
            
            if expression.lower() == 'exit':
                print("Exiting calculator. Goodbye!")
                break
                
            result = calculator.calculate(expression)
            
            # Display the result with or without decimal points as appropriate
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
