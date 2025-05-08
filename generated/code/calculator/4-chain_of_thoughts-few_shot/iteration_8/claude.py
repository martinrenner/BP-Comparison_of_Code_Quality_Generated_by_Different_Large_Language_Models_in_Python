class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    This calculator supports basic arithmetic operations (+, -, *, /),
    parentheses, and follows the correct order of operations.
    """
    
    def __init__(self):
        """Initialize the Calculator object."""
        # Define the supported operators and their precedence
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
            ValueError: If the expression contains invalid characters or syntax
            ZeroDivisionError: If the expression attempts to divide by zero
            SyntaxError: If the expression has unbalanced parentheses
        """
        # Normalize and validate the expression
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise SyntaxError("Unbalanced parentheses in the expression")
        
        # Parse the expression and compute the result
        tokens = self._tokenize(normalized_expr)
        return self._evaluate_expression(tokens)
    
    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.
        
        Args:
            expression (str): A mathematical expression as a string
            
        Returns:
            str: The normalized expression
            
        Raises:
            ValueError: If the expression contains invalid characters
        """
        allowed_chars = set("0123456789+-*/().e ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters")
        
        # Replace multiple spaces with a single space
        normalized = ' '.join(expression.split())
        
        # Handle unary minus by replacing "-" with "0-" at the beginning or after an open parenthesis
        normalized = normalized.replace('(-', '(0-')
        if normalized.startswith('-'):
            normalized = '0' + normalized
            
        return normalized
    
    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether a mathematical expression has properly paired parentheses.
        
        Args:
            expression (str): A string containing the mathematical expression
            
        Returns:
            bool: True if parentheses are correctly paired, otherwise False
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
    
    def _tokenize(self, expression: str) -> list:
        """
        Converts a string expression into a list of tokens.
        
        Args:
            expression (str): A normalized mathematical expression
            
        Returns:
            list: A list of tokens (numbers, operators, and parentheses)
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # Skip spaces
            if char.isspace():
                i += 1
                continue
            
            # Handle operators and parentheses
            if char in self.operators or char in '()':
                tokens.append(char)
                i += 1
                continue
            
            # Handle numbers (including decimals)
            if char.isdigit() or char == '.':
                num_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.' or expression[i].lower() == 'e'):
                    num_str += expression[i]
                    i += 1
                    
                    # Handle scientific notation (e.g., 1e-3)
                    if i < len(expression) and expression[i-1].lower() == 'e' and (expression[i] == '-' or expression[i] == '+'):
                        num_str += expression[i]
                        i += 1
                        
                try:
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: {num_str}")
                continue
                
            # If we reach here, there's an unexpected character
            raise ValueError(f"Unexpected character: {char}")
        
        return tokens
    
    def _evaluate_expression(self, tokens: list) -> float:
        """
        Evaluates an expression represented as a list of tokens.
        
        Args:
            tokens (list): A list of tokens (numbers, operators, and parentheses)
            
        Returns:
            float: The result of evaluating the expression
            
        Raises:
            ZeroDivisionError: If the expression attempts to divide by zero
            ValueError: If the expression has invalid syntax
        """
        # Define helper functions for the shunting yard algorithm
        def apply_operator(operators_stack, output_queue):
            op = operators_stack.pop()
            if len(output_queue) < 2:
                raise ValueError("Invalid expression: not enough operands")
            
            b = output_queue.pop()
            a = output_queue.pop()
            
            if op == '+':
                output_queue.append(a + b)
            elif op == '-':
                output_queue.append(a - b)
            elif op == '*':
                output_queue.append(a * b)
            elif op == '/':
                if b == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                output_queue.append(a / b)
        
        # Implementation of the shunting yard algorithm
        output_queue = []
        operators_stack = []
        
        for token in tokens:
            # If the token is a number, push it to the output queue
            if isinstance(token, (int, float)):
                output_queue.append(token)
            
            # If the token is an operator
            elif token in self.operators:
                while (operators_stack and operators_stack[-1] in self.operators and
                       self.operators[operators_stack[-1]] >= self.operators[token]):
                    apply_operator(operators_stack, output_queue)
                operators_stack.append(token)
            
            # If the token is a left parenthesis, push it onto the stack
            elif token == '(':
                operators_stack.append(token)
            
            # If the token is a right parenthesis
            elif token == ')':
                while operators_stack and operators_stack[-1] != '(':
                    apply_operator(operators_stack, output_queue)
                
                if not operators_stack or operators_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses")
                operators_stack.pop()  # Remove the left parenthesis
        
        # Apply any remaining operators
        while operators_stack:
            if operators_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            apply_operator(operators_stack, output_queue)
        
        if len(output_queue) != 1:
            raise ValueError("Invalid expression")
            
        return output_queue[0]


# Example usage
if __name__ == "__main__":
    calc = Calculator()
    
    # Test cases
    test_expressions = [
        "3 + 4",
        "2 * (3 + 4)",
        "10 / 2",
        "2.5 * 3",
        "2 * -3",
        "(7 + 3) * (5 - 2)",
        "2 + 3 * 4",
        "1e3 + 5",
        "(2 + 3) * 4 / 2 - 5"
    ]
    
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"Error evaluating '{expr}': {e}")
