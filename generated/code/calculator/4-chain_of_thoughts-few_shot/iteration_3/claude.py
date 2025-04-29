class Calculator:
    """
    A console-based arithmetic calculator that supports basic mathematical operations.
    
    This calculator evaluates mathematical expressions following the standard order of
    operations (PEMDAS) and supports parentheses for grouping operations.
    
    Attributes:
        None
    """
    
    def __init__(self):
        """Initialize the Calculator instance."""
        # Dictionary mapping operators to their precedence
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
            expression (str): The mathematical expression to evaluate.
            
        Returns:
            float: The result of the evaluated expression.
            
        Raises:
            ValueError: If the expression contains invalid characters or has syntax errors.
            ZeroDivisionError: If the expression involves division by zero.
            Exception: For other calculation errors.
        """
        # Validate and normalize the input expression
        normalized_expr = self._normalize_expression(expression)
        
        # Check for balanced parentheses
        if not self._is_balanced_parentheses(normalized_expr):
            raise ValueError("Unbalanced parentheses in the expression")
        
        # Convert infix notation to postfix (Reverse Polish Notation)
        postfix = self._infix_to_postfix(normalized_expr)
        
        # Evaluate the postfix expression
        result = self._evaluate_postfix(postfix)
        
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
        allowed_chars = set("0123456789+-*/().e ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters")
        
        # Handle unary operations at the beginning of expression or after open parenthesis
        # Replace "-X" with "0-X" for proper handling of negative numbers
        expression = expression.replace(" ", "")
        
        # Handle negative numbers at the beginning
        if expression.startswith('-'):
            expression = '0' + expression
            
        # Handle negative numbers after open parenthesis
        expression = expression.replace('(-', '(0-')
        
        return expression
    
    def _is_balanced_parentheses(self, expression: str) -> bool:
        """
        Checks whether a mathematical expression has properly balanced parentheses.
        
        Args:
            expression (str): The expression to check.
            
        Returns:
            bool: True if parentheses are properly balanced, False otherwise.
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
    
    def _is_operator(self, char: str) -> bool:
        """
        Checks if a character is an operator.
        
        Args:
            char (str): The character to check.
            
        Returns:
            bool: True if the character is an operator, False otherwise.
        """
        return char in self.operators
    
    def _infix_to_postfix(self, expression: str) -> list:
        """
        Converts an infix expression to postfix notation (Reverse Polish Notation).
        
        Args:
            expression (str): The normalized infix expression.
            
        Returns:
            list: The expression in postfix notation as a list of tokens.
        """
        output = []
        operator_stack = []
        i = 0
        
        while i < len(expression):
            # If the character is a digit or decimal point, extract the full number
            if expression[i].isdigit() or expression[i] == '.':
                num = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num += expression[i]
                    i += 1
                output.append(float(num))
                continue
                
            # If the character is an opening parenthesis, push it to the stack
            elif expression[i] == '(':
                operator_stack.append(expression[i])
                
            # If the character is a closing parenthesis, pop operators until matching opening parenthesis is found
            elif expression[i] == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                    
                # Pop the opening parenthesis
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
                else:
                    raise ValueError("Mismatched parentheses")
                    
            # If the character is an operator, handle based on precedence
            elif self._is_operator(expression[i]):
                while (operator_stack and operator_stack[-1] != '(' and 
                       (self.operators.get(operator_stack[-1], 0) >= 
                        self.operators.get(expression[i], 0))):
                    output.append(operator_stack.pop())
                operator_stack.append(expression[i])
                
            i += 1
            
        # Pop any remaining operators from the stack to the output
        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())
            
        return output
    
    def _evaluate_postfix(self, postfix: list) -> float:
        """
        Evaluates a postfix expression and returns the result.
        
        Args:
            postfix (list): The postfix expression as a list of tokens.
            
        Returns:
            float: The result of the evaluated expression.
            
        Raises:
            ZeroDivisionError: If the expression involves division by zero.
            Exception: For other calculation errors.
        """
        stack = []
        
        for token in postfix:
            # If the token is a number, push it to the stack
            if isinstance(token, (int, float)):
                stack.append(token)
            # If the token is an operator, pop two values from the stack, perform the operation, and push the result back
            elif self._is_operator(token):
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                
                b = stack.pop()
                a = stack.pop()
                
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero is not allowed")
                    stack.append(a / b)
        
        # The final result should be the only value left on the stack
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands")
            
        return stack[0]
