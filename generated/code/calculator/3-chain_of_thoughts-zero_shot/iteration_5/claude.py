class Calculator:
    """
    A calculator class that evaluates arithmetic expressions following the order of operations.
    
    Supports:
    - Basic operations: addition (+), subtraction (-), multiplication (*), division (/)
    - Parentheses for grouping
    - Decimal and negative numbers
    
    Implements proper validation and error handling without using eval().
    """
    
    def __init__(self):
        """Initialize the Calculator class."""
        # Define operators and their precedence
        self.operators = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate the given arithmetic expression and return the result.
        
        Args:
            expression (str): The arithmetic expression to evaluate
            
        Returns:
            float: The result of the evaluation
            
        Raises:
            ValueError: If the expression contains invalid characters or is malformed
            ZeroDivisionError: If the expression attempts to divide by zero
            SyntaxError: If the expression has unbalanced parentheses
        """
        # Remove all whitespaces
        expression = expression.replace(' ', '')
        
        if not expression:
            raise ValueError("Expression cannot be empty")
            
        # Validate the expression
        self._validate_expression(expression)
        
        # Convert infix notation to postfix notation and evaluate
        return self._evaluate_postfix(self._infix_to_postfix(expression))
    
    def _validate_expression(self, expression: str) -> None:
        """
        Validate the expression for correctness.
        
        Args:
            expression (str): The expression to validate
            
        Raises:
            ValueError: If the expression contains invalid characters
            SyntaxError: If the expression has unbalanced parentheses
        """
        # Check for balanced parentheses
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack or stack.pop() != '(':
                    raise SyntaxError("Unbalanced parentheses in expression")
        
        if stack:
            raise SyntaxError("Unbalanced parentheses in expression")
        
        # Check for valid characters
        valid_chars = set('0123456789.()+-*/') 
        for char in expression:
            if char not in valid_chars:
                raise ValueError(f"Invalid character '{char}' in expression")
        
        # Check for consecutive operators
        prev_char = None
        for i, char in enumerate(expression):
            # Allow minus after operator or at beginning (for negative numbers)
            if char in '+-*/' and prev_char in '+-*/' and not (char == '-' and prev_char in '(+-*/'):
                raise ValueError(f"Invalid consecutive operators at position {i}")
            prev_char = char
            
    def _is_number(self, s: str) -> bool:
        """
        Check if a string is a valid number.
        
        Args:
            s (str): The string to check
            
        Returns:
            bool: True if the string is a valid number, False otherwise
        """
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    def _infix_to_postfix(self, expression: str) -> list:
        """
        Convert infix notation to postfix notation.
        
        Args:
            expression (str): The expression in infix notation
            
        Returns:
            list: The expression in postfix notation
        """
        postfix = []
        stack = []
        
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # Handle negative numbers at the beginning or after an operator/opening parenthesis
            if (char == '-' and (i == 0 or expression[i-1] in '(+-*/')):
                # Find the end of the number
                j = i + 1
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                
                # Extract the negative number
                if j > i + 1:
                    number = expression[i:j]
                    postfix.append(number)
                    i = j
                    continue
                else:
                    # It's a unary minus, but not followed by a number
                    # Handle as an operator with special precedence
                    while (stack and stack[-1] != '(' and 
                           self.operators.get(stack[-1], 0) >= self.operators.get(char, 0)):
                        postfix.append(stack.pop())
                    stack.append(char)
                    i += 1
                    continue
            
            # If the character is a digit or decimal, find the complete number
            if char.isdigit() or char == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                postfix.append(expression[i:j])
                i = j
                continue
                
            # If the character is an opening parenthesis, push to stack
            if char == '(':
                stack.append(char)
                
            # If the character is a closing parenthesis, pop from stack until opening parenthesis
            elif char == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                # Remove the opening parenthesis
                if stack and stack[-1] == '(':
                    stack.pop()
                    
            # If the character is an operator
            elif char in self.operators:
                while (stack and stack[-1] != '(' and 
                       self.operators.get(stack[-1], 0) >= self.operators.get(char, 0)):
                    postfix.append(stack.pop())
                stack.append(char)
                
            i += 1
                
        # Pop all remaining operators from the stack
        while stack:
            postfix.append(stack.pop())
            
        return postfix
    
    def _evaluate_postfix(self, postfix: list) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix (list): The expression in postfix notation
            
        Returns:
            float: The result of the evaluation
            
        Raises:
            ZeroDivisionError: If the expression attempts to divide by zero
            ValueError: If the expression is invalid
        """
        stack = []
        
        for token in postfix:
            # If the token is a number, push it to the stack
            if self._is_number(token):
                stack.append(float(token))
            # If the token is an operator
            elif token in self.operators:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                
                # Pop the top two elements from the stack
                b = stack.pop()
                a = stack.pop()
                
                # Perform the operation
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
        
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands")
            
        return stack.pop()


def main():
    """Main function to run the calculator interactively."""
    calculator = Calculator()
    
    print("Console-based Arithmetic Calculator")
    print("Type 'exit' to quit")
    print("Supported operations: +, -, *, /, and parentheses ()")
    
    while True:
        try:
            expression = input("\nEnter an expression: ")
            
            if expression.lower() == 'exit':
                print("Exiting calculator. Goodbye!")
                break
                
            result = calculator.calculate(expression)
            
            # Format the result to avoid unnecessary trailing zeros
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
