class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    This calculator supports basic arithmetic operations:
    - Addition (+)
    - Subtraction (-)
    - Multiplication (*)
    - Division (/)
    
    It also handles parentheses and respects operator precedence.
    """
    
    def __init__(self):
        """Initialize the Calculator."""
        # Define the operators and their precedence
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
        
        # Check if parentheses are balanced
        if not self._is_balanced(normalized_expr):
            raise SyntaxError("Expression has unbalanced parentheses")
        
        # Convert to postfix and evaluate
        tokens = self._tokenize(normalized_expr)
        postfix = self._to_postfix(tokens)
        return self._evaluate_postfix(postfix)
    
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
        
        return expression.replace(" ", "")
    
    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if the parentheses in the expression are properly balanced.
        
        Args:
            expression (str): A mathematical expression as a string.
            
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
        Converts a string expression into a list of tokens.
        
        Args:
            expression (str): A normalized mathematical expression.
            
        Returns:
            list: A list of tokens (numbers and operators).
            
        Raises:
            ValueError: If the expression contains invalid syntax.
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Handle operators and parentheses
            if char in self.operators or char in "()":
                tokens.append(char)
                i += 1
            
            # Handle numbers (integers and floating point)
            elif char.isdigit() or char == '.':
                num_str = ""
                
                # Handle negative numbers at the beginning or after an open parenthesis
                if char == '-' and (i == 0 or expression[i-1] == '('):
                    num_str += '-'
                    i += 1
                
                # Build the number string
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.' or expression[i].lower() == 'e'):
                    # Handle scientific notation
                    if expression[i].lower() == 'e':
                        num_str += expression[i]
                        i += 1
                        # Check for positive or negative exponent
                        if i < len(expression) and (expression[i] == '+' or expression[i] == '-'):
                            num_str += expression[i]
                            i += 1
                    else:
                        num_str += expression[i]
                        i += 1
                
                try:
                    # Convert to float and add to tokens
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: {num_str}")
            else:
                i += 1
        
        return tokens
    
    def _to_postfix(self, tokens: list) -> list:
        """
        Converts an infix expression to postfix notation using the Shunting Yard algorithm.
        
        Args:
            tokens (list): A list of tokens in infix notation.
            
        Returns:
            list: A list of tokens in postfix notation.
        """
        output = []
        operator_stack = []
        
        for token in tokens:
            # If token is a number, add it to the output
            if isinstance(token, float):
                output.append(token)
            
            # If token is an operator
            elif token in self.operators:
                # Pop operators with higher or equal precedence and add them to output
                while (operator_stack and operator_stack[-1] != '(' and
                       self.operators.get(operator_stack[-1], 0) >= self.operators.get(token, 0)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            
            # If token is an open parenthesis, push it to the stack
            elif token == '(':
                operator_stack.append(token)
            
            # If token is a close parenthesis
            elif token == ')':
                # Pop operators and add to output until reaching the matching open parenthesis
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                
                # Remove the open parenthesis
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
        
        # Add any remaining operators to the output
        while operator_stack:
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, postfix: list) -> float:
        """
        Evaluates a postfix expression.
        
        Args:
            postfix (list): A list of tokens in postfix notation.
            
        Returns:
            float: The result of the evaluated expression.
            
        Raises:
            ZeroDivisionError: If the expression attempts to divide by zero.
            ValueError: If the expression is invalid.
        """
        if not postfix:
            raise ValueError("Empty expression")
        
        stack = []
        
        for token in postfix:
            # If token is a number, push it to the stack
            if isinstance(token, float):
                stack.append(token)
            
            # If token is an operator, pop two values, apply the operator, and push the result
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid expression")
                
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
                        raise ZeroDivisionError("Division by zero")
                    stack.append(a / b)
        
        # The final result should be the only value left in the stack
        if len(stack) != 1:
            raise ValueError("Invalid expression")
        
        return stack[0]


def main():
    """Main function to demonstrate the calculator functionality."""
    calculator = Calculator()
    
    print("Console Calculator (type 'exit' to quit)")
    print("Supported operations: +, -, *, / and parentheses")
    
    while True:
        try:
            expression = input("\nEnter an expression: ").strip().lower()
            
            if expression == 'exit':
                print("Goodbye!")
                break
            
            if not expression:
                continue
            
            result = calculator.calculate(expression)
            
            # Display result as an integer if it's a whole number
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
