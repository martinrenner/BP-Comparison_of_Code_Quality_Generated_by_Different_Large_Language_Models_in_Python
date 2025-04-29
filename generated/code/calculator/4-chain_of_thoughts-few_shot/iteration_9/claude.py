class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    This calculator supports:
    - Basic arithmetic operations: addition (+), subtraction (-), multiplication (*), division (/)
    - Parentheses for controlling order of operations
    - Decimal and negative numbers
    
    Example usage:
        calc = Calculator()
        result = calc.calculate("3 + 4 * 2")  # Returns 11.0
        result = calc.calculate("(3 + 4) * 2")  # Returns 14.0
    """
    
    def __init__(self):
        """Initialize the Calculator."""
        self.operators = {
            '+': (1, lambda x, y: x + y),
            '-': (1, lambda x, y: x - y),
            '*': (2, lambda x, y: x * y),
            '/': (2, lambda x, y: x / y)
        }
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression (str): A string containing a mathematical expression with 
                             numbers, operators (+, -, *, /), and parentheses.
        
        Returns:
            float: The calculated result of the expression.
        
        Raises:
            ValueError: If the expression contains invalid characters or syntax.
            ZeroDivisionError: If the expression involves division by zero.
            SyntaxError: If the expression has unbalanced parentheses or invalid syntax.
        """
        # Normalize and validate the expression
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise SyntaxError("Unbalanced parentheses in the expression")
        
        # Parse and evaluate the expression
        return self._evaluate(normalized_expr)
    
    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.
        
        Args:
            expression (str): The input mathematical expression.
            
        Returns:
            str: Normalized expression without spaces.
            
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().e ")  # 'e' for scientific notation
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters")
        
        # Handle unary minus at the beginning of expression or after opening parenthesis
        processed = ""
        for i, char in enumerate(expression.replace(" ", "")):
            if char == '-' and (i == 0 or expression[i-1] == '('):
                processed += "0-"
            else:
                processed += char
                
        return processed
    
    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether the parentheses in the expression are properly balanced.
        
        Args:
            expression (str): The normalized mathematical expression.
            
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
    
    def _tokenize(self, expression: str) -> list:
        """
        Converts an expression string into a list of tokens (numbers and operators).
        
        Args:
            expression (str): The normalized mathematical expression.
            
        Returns:
            list: A list of tokens extracted from the expression.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # Handle operators
            if char in self.operators or char in '()':
                tokens.append(char)
                i += 1
            # Handle numbers (including decimals and scientific notation)
            elif char.isdigit() or char == '.':
                num = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.' or expression[i] == 'e'):
                    num += expression[i]
                    i += 1
                    # Handle scientific notation with possible + or - after e
                    if i < len(expression) and num[-1] == 'e' and (expression[i] == '+' or expression[i] == '-'):
                        num += expression[i]
                        i += 1
                try:
                    tokens.append(float(num))
                except ValueError:
                    raise ValueError(f"Invalid number format: {num}")
            else:
                i += 1
                
        return tokens
    
    def _evaluate(self, expression: str) -> float:
        """
        Evaluates the mathematical expression using the shunting yard algorithm.
        
        Args:
            expression (str): The normalized mathematical expression.
            
        Returns:
            float: The calculated result.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
            SyntaxError: If the expression has invalid syntax.
        """
        # Tokenize the expression
        tokens = self._tokenize(expression)
        
        # Shunting yard algorithm implementation
        output_queue = []  # For numbers and final calculation
        operator_stack = []  # For operators
        
        for token in tokens:
            # If token is a number, add it to the output queue
            if isinstance(token, float):
                output_queue.append(token)
            
            # If token is an operator
            elif token in self.operators:
                # Get precedence of current operator
                current_precedence = self.operators[token][0]
                
                # While there's an operator on the stack with higher/equal precedence, pop it
                while (operator_stack and operator_stack[-1] in self.operators and
                       self.operators[operator_stack[-1]][0] >= current_precedence):
                    output_queue.append(operator_stack.pop())
                
                # Push current operator onto the stack
                operator_stack.append(token)
            
            # If token is a left parenthesis, push onto operator stack
            elif token == '(':
                operator_stack.append(token)
            
            # If token is a right parenthesis
            elif token == ')':
                # Pop operators onto output queue until left parenthesis is found
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                # Remove the left parenthesis
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
                else:
                    raise SyntaxError("Mismatched parentheses")
        
        # Pop any remaining operators onto the output queue
        while operator_stack:
            if operator_stack[-1] == '(':
                raise SyntaxError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
        
        # Evaluate the RPN expression
        evaluation_stack = []
        
        for token in output_queue:
            if isinstance(token, float):
                evaluation_stack.append(token)
            else:  # token is an operator
                if len(evaluation_stack) < 2:
                    raise SyntaxError("Invalid expression syntax")
                
                # Pop operands in the correct order (b is first popped, then a)
                b = evaluation_stack.pop()
                a = evaluation_stack.pop()
                
                # Perform the operation
                operation = self.operators[token][1]
                try:
                    result = operation(a, b)
                    evaluation_stack.append(result)
                except ZeroDivisionError:
                    raise ZeroDivisionError("Division by zero is not allowed")
        
        if len(evaluation_stack) != 1:
            raise SyntaxError("Invalid expression syntax")
        
        return evaluation_stack[0]
