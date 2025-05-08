class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    This calculator supports:
    - Basic arithmetic operations: addition, subtraction, multiplication, division
    - Parentheses for grouping expressions
    - Proper operator precedence
    - Integers and floating-point numbers (including negative values)
    
    Implementation follows the ISO/IEC 25010 quality standards.
    """
    
    def __init__(self):
        """Initialize the Calculator object."""
        # Define supported operators and their precedence
        self.operators = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression (str): A string containing a mathematical expression
                              (e.g., "3 + 4 * (2 - 1)")
                              
        Returns:
            float: The result of the evaluated expression
            
        Raises:
            ValueError: If the expression contains invalid characters, unbalanced parentheses,
                       or is malformed
            ZeroDivisionError: If the expression involves division by zero
        """
        # Validate and normalize the expression
        normalized_expr = self._normalize_expression(expression)
        
        # Check for balanced parentheses
        if not self._is_balanced(normalized_expr):
            raise ValueError("Unbalanced parentheses in the expression")
        
        # Convert infix to postfix notation and evaluate
        tokens = self._tokenize(normalized_expr)
        postfix = self._infix_to_postfix(tokens)
        return self._evaluate_postfix(postfix)
    
    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.
        
        Args:
            expression (str): A mathematical expression as a string
            
        Returns:
            str: The normalized expression without spaces
            
        Raises:
            ValueError: If the expression contains invalid characters or is empty
        """
        if not expression or expression.isspace():
            raise ValueError("Expression cannot be empty")
            
        # Define allowed characters
        allowed_chars = set("0123456789+-*/(). ")
        
        # Check for invalid characters
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters")
            
        return expression.replace(" ", "")
    
    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if the parentheses in the expression are balanced.
        
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
    
    def _tokenize(self, expression: str) -> list:
        """
        Converts a string expression into a list of tokens (numbers and operators).
        
        Args:
            expression (str): A normalized mathematical expression
            
        Returns:
            list: A list of tokens (numbers and operators)
            
        Raises:
            ValueError: If the expression is malformed
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Handle numbers (including decimal points)
            if char.isdigit() or (char == '.' and i + 1 < len(expression) and expression[i + 1].isdigit()):
                # Track start of number
                num_start = i
                
                # If number starts with a decimal point, ensure it has digits after it
                if char == '.':
                    if i + 1 >= len(expression) or not expression[i + 1].isdigit():
                        raise ValueError("Invalid number format: decimal point must be followed by digits")
                
                # Find the end of the number
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    i += 1
                
                # Extract the number string
                num_str = expression[num_start:i]
                
                # Validate the number (ensure only one decimal point)
                if num_str.count('.') > 1:
                    raise ValueError(f"Invalid number format: '{num_str}' contains multiple decimal points")
                
                try:
                    # Convert to float
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: '{num_str}'")
                
                # Continue to next iteration as i is already incremented in the inner loop
                continue
                
            # Handle operators and parentheses
            elif char in self.operators or char in '()':
                tokens.append(char)
                
            # Handle negative numbers
            elif char == '-' and (i == 0 or expression[i-1] in self.operators or expression[i-1] == '('):
                # This is a negative sign, not a subtraction operator
                # Find the end of the number
                num_start = i  # Include the negative sign
                i += 1  # Move past the negative sign
                
                # Skip any decimal point that might come after the negative sign
                if i < len(expression) and expression[i] == '.':
                    i += 1
                
                # Find the rest of the number
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    i += 1
                
                num_str = expression[num_start:i]
                
                # Validate the number
                if num_str.count('.') > 1:
                    raise ValueError(f"Invalid number format: '{num_str}' contains multiple decimal points")
                
                try:
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: '{num_str}'")
                
                # Continue to next iteration
                continue
            
            i += 1
        
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts an infix expression to postfix notation.
        
        Args:
            tokens (list): A list of tokens in infix notation
            
        Returns:
            list: A list of tokens in postfix notation
        """
        output = []
        operator_stack = []
        
        for token in tokens:
            # If the token is a number, add it to the output queue
            if isinstance(token, float):
                output.append(token)
            
            # If the token is an operator
            elif token in self.operators:
                # While there's an operator on the stack with higher precedence
                while (operator_stack and 
                       operator_stack[-1] != '(' and 
                       (operator_stack[-1] in self.operators) and
                       (self.operators[operator_stack[-1]] >= self.operators[token])):
                    output.append(operator_stack.pop())
                
                # Push the current operator onto the stack
                operator_stack.append(token)
            
            # If the token is a left parenthesis, push it onto the stack
            elif token == '(':
                operator_stack.append(token)
            
            # If the token is a right parenthesis
            elif token == ')':
                # Pop operators from the stack and add to output until we find the matching left parenthesis
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                
                # Remove the left parenthesis from the stack
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
        
        # Pop any remaining operators from the stack and add to output
        while operator_stack:
            output.append(operator_stack.pop())
        
        return output

    def _evaluate_postfix(self, postfix: list) -> float:
        """
        Evaluates a postfix expression.
        
        Args:
            postfix (list): A list of tokens in postfix notation
            
        Returns:
            float: The result of evaluating the expression
            
        Raises:
            ZeroDivisionError: If the expression involves division by zero
            ValueError: If the expression is malformed
        """
        if not postfix:
            raise ValueError("Empty expression")
            
        operand_stack = []
        
        for token in postfix:
            # If the token is a number, push it onto the stack
            if isinstance(token, float):
                operand_stack.append(token)
            
            # If the token is an operator, apply it to the top two items on the stack
            elif token in self.operators:
                # Need at least two operands for an operation
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                
                # Pop the operands (in reverse order)
                b = operand_stack.pop()
                a = operand_stack.pop()
                
                # Apply the operation
                if token == '+':
                    operand_stack.append(a + b)
                elif token == '-':
                    operand_stack.append(a - b)
                elif token == '*':
                    operand_stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    operand_stack.append(a / b)
        
        # The final result should be the only item on the stack
        if len(operand_stack) != 1:
            raise ValueError("Invalid expression: too many operands")
        
        return operand_stack[0]


# Example usage:
if __name__ == "__main__":
    calculator = Calculator()
    
    # Test expressions
    test_expressions = [
        "3 + 4",
        "10 - 5",
        "3 * (4 + 2)",
        "10 / 2",
        "(4 + 5) * (10 - 8)",
        "3.5 + 2.1",
        "-5 + 3",
        "10 / (2 + 3)"
    ]
    
    print("Calculator Test Results:")
    print("-----------------------")
    
    for expr in test_expressions:
        try:
            result = calculator.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} → Error: {str(e)}")
    
    # Interactive mode
    print("\nInteractive Calculator (type 'exit' to quit):")
    print("--------------------------------------------")
    
    while True:
        expr = input("Enter expression: ")
        if expr.lower() == 'exit':
            break
        
        try:
            result = calculator.calculate(expr)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {str(e)}")
