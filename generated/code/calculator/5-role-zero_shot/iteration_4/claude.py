class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    This calculator supports:
    - Basic arithmetic operations: addition (+), subtraction (-), multiplication (*), division (/)
    - Parentheses for grouping expressions
    - Integers and floating-point numbers, including negative values
    - Proper operator precedence
    """
    
    def __init__(self):
        """Initialize the Calculator with supported operators and their precedence."""
        # Define operators and their precedence (higher value means higher precedence)
        self.operators = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression: A string containing a mathematical expression
                        (e.g., "2 + 3 * (4 - 1)")
        
        Returns:
            float: The result of evaluating the expression
            
        Raises:
            ValueError: If the expression contains invalid characters or has syntax errors
            ZeroDivisionError: If the expression attempts division by zero
            SyntaxError: If the expression has unbalanced parentheses
        """
        # Remove all whitespace from the expression
        expression = expression.replace(" ", "")
        
        if not expression:
            raise ValueError("Expression cannot be empty")
            
        # Validate the expression
        self._validate_expression(expression)
        
        # Parse and evaluate the expression
        return self._evaluate_expression(expression)
    
    def _validate_expression(self, expression: str) -> None:
        """
        Validate that the expression is well-formed.
        
        Args:
            expression: The expression to validate
            
        Raises:
            ValueError: If the expression contains invalid characters
            SyntaxError: If the expression has unbalanced parentheses or other syntax errors
        """
        # Check for balanced parentheses
        parentheses_count = 0
        for char in expression:
            if char == '(':
                parentheses_count += 1
            elif char == ')':
                parentheses_count -= 1
                if parentheses_count < 0:
                    raise SyntaxError("Unbalanced parentheses: too many closing parentheses")
                
        if parentheses_count > 0:
            raise SyntaxError("Unbalanced parentheses: too many opening parentheses")
            
        # Validate characters in the expression
        valid_chars = set("0123456789.+-*/() ")
        for char in expression:
            if char not in valid_chars:
                raise ValueError(f"Invalid character in expression: '{char}'")
                
        # Check for syntax errors like consecutive operators
        for i in range(len(expression) - 1):
            if (expression[i] in self.operators and expression[i+1] in self.operators):
                raise SyntaxError(f"Invalid syntax: consecutive operators at position {i}")
                
        # Check for empty parentheses
        if "()" in expression:
            raise SyntaxError("Empty parentheses are not allowed")
    
    def _evaluate_expression(self, expression: str) -> float:
        """
        Evaluate the given expression using the Shunting Yard algorithm.
        
        Args:
            expression: The expression to evaluate
            
        Returns:
            float: The result of evaluating the expression
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression cannot be evaluated
        """
        # Implement Shunting Yard algorithm
        # Convert infix notation to postfix notation, then evaluate
        output_queue = []  # Output queue for the postfix expression
        operator_stack = []  # Stack for operators and parentheses
        
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # Process numbers (including multi-digit and decimal numbers)
            if char.isdigit() or (char == '.' and i + 1 < len(expression) and expression[i + 1].isdigit()):
                # Handle negative numbers
                if char == '-' and (i == 0 or expression[i-1] == '('):
                    start = i
                    i += 1
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        i += 1
                    try:
                        output_queue.append(float(expression[start:i]))
                    except ValueError:
                        raise ValueError(f"Invalid number format: {expression[start:i]}")
                    continue
                
                # Handle regular numbers
                start = i
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    i += 1
                try:
                    output_queue.append(float(expression[start:i]))
                except ValueError:
                    raise ValueError(f"Invalid number format: {expression[start:i]}")
                continue
            
            # Process negative numbers at the beginning or after an open parenthesis
            if char == '-' and (i == 0 or expression[i-1] == '('):
                start = i
                i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    i += 1
                if i > start + 1:  # Make sure we have digits after the minus sign
                    try:
                        output_queue.append(float(expression[start:i]))
                    except ValueError:
                        raise ValueError(f"Invalid number format: {expression[start:i]}")
                    continue
                # If not followed by digits, treat as a unary operator
                # (handled as binary operator with 0 as first operand)
                output_queue.append(0.0)
                operator_stack.append(char)
                i += 1
                continue
            
            # Process operators
            if char in self.operators:
                while (operator_stack and operator_stack[-1] != '(' and 
                       self.operators.get(operator_stack[-1], 0) >= self.operators.get(char, 0)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(char)
            
            # Process open parenthesis
            elif char == '(':
                operator_stack.append(char)
            
            # Process close parenthesis
            elif char == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Remove the open parenthesis
                else:
                    raise SyntaxError("Unbalanced parentheses")
            
            i += 1
        
        # Process remaining operators
        while operator_stack:
            if operator_stack[-1] == '(':
                raise SyntaxError("Unbalanced parentheses")
            output_queue.append(operator_stack.pop())
        
        # Evaluate the postfix expression
        return self._evaluate_postfix(output_queue)
    
    def _evaluate_postfix(self, postfix_queue: list) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix_queue: A queue of tokens in postfix notation
            
        Returns:
            float: The result of evaluating the postfix expression
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression cannot be evaluated
        """
        if not postfix_queue:
            raise ValueError("Empty expression")
            
        evaluation_stack = []
        
        for token in postfix_queue:
            if isinstance(token, float):
                evaluation_stack.append(token)
            else:
                # It's an operator, so pop two values and perform the operation
                if len(evaluation_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                
                b = evaluation_stack.pop()
                a = evaluation_stack.pop()
                
                if token == '+':
                    evaluation_stack.append(a + b)
                elif token == '-':
                    evaluation_stack.append(a - b)
                elif token == '*':
                    evaluation_stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero is not allowed")
                    evaluation_stack.append(a / b)
        
        if len(evaluation_stack) != 1:
            raise ValueError("Invalid expression: too many operands")
            
        return evaluation_stack[0]


def main():
    """Main function to demonstrate the calculator in action."""
    calculator = Calculator()
    
    print("Console-based Arithmetic Calculator")
    print("Enter 'q' to quit")
    
    while True:
        try:
            expression = input("\nEnter an expression: ")
            if expression.lower() == 'q':
                break
                
            result = calculator.calculate(expression)
            
            # Check if the result is an integer (no decimal part)
            if result.is_integer():
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    print("Goodbye!")


if __name__ == "__main__":
    main()
