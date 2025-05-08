class Calculator:
    """
    A console-based arithmetic calculator supporting basic operations and parentheses.
    
    This calculator implements the Shunting Yard algorithm to parse and evaluate
    mathematical expressions while respecting the order of operations.
    """

    def __init__(self):
        """Initialize the calculator with operator precedence mapping."""
        # Define operator precedence
        self.precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            # Parentheses don't need precedence in this implementation
        }
        
        # Define supported operators
        self.operators = set(['+', '-', '*', '/'])
        
    def is_number(self, token):
        """
        Check if a token is a valid number (integer or decimal).
        
        Args:
            token (str): The token to check
            
        Returns:
            bool: True if the token is a valid number, False otherwise
        """
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def tokenize(self, expression):
        """
        Convert an expression string into tokens.
        
        Args:
            expression (str): The mathematical expression to tokenize
            
        Returns:
            list: A list of tokens (numbers, operators, parentheses)
            
        Raises:
            ValueError: If the expression contains invalid characters
        """
        # Remove all whitespace
        expression = expression.replace(' ', '')
        
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # Handle operators and parentheses
            if char in self.operators or char in '()':
                tokens.append(char)
                i += 1
            # Handle numbers (including decimals and negative numbers)
            elif char.isdigit() or char == '.':
                num = char
                i += 1
                
                # Continue building the number
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num += expression[i]
                    i += 1
                
                if not self.is_number(num):
                    raise ValueError(f"Invalid number format: {num}")
                
                tokens.append(num)
            # Handle negative numbers at the start or after an operator/open parenthesis
            elif char == '-' and (i == 0 or expression[i-1] in self.operators or expression[i-1] == '('):
                num = char
                i += 1
                
                # Continue building the number
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num += expression[i]
                    i += 1
                
                if len(num) == 1:  # Just a minus sign without a number
                    tokens.append(char)
                else:
                    if not self.is_number(num):
                        raise ValueError(f"Invalid number format: {num}")
                    tokens.append(num)
            else:
                raise ValueError(f"Invalid character in expression: {char}")
        
        return tokens

    def infix_to_postfix(self, tokens):
        """
        Convert infix notation tokens to postfix notation using the Shunting Yard algorithm.
        
        Args:
            tokens (list): The tokenized expression in infix notation
            
        Returns:
            list: The expression in postfix notation
            
        Raises:
            ValueError: If parentheses are unbalanced
        """
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            # If token is a number, add to output queue
            if self.is_number(token):
                output_queue.append(token)
            # If token is an operator
            elif token in self.operators:
                # Pop operators with higher or equal precedence
                while (operator_stack and 
                       operator_stack[-1] in self.operators and 
                       self.precedence[operator_stack[-1]] >= self.precedence[token]):
                    output_queue.append(operator_stack.pop())
                # Push the current operator to the stack
                operator_stack.append(token)
            # If token is an opening parenthesis, push to stack
            elif token == '(':
                operator_stack.append(token)
            # If token is a closing parenthesis
            elif token == ')':
                # Pop until the matching opening parenthesis is found
                while operator_stack and operator_stack[-1] != '(':
                    if not operator_stack:
                        raise ValueError("Unbalanced parentheses")
                    output_queue.append(operator_stack.pop())
                
                # Remove the opening parenthesis
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
                else:
                    raise ValueError("Unbalanced parentheses")
        
        # Pop any remaining operators
        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Unbalanced parentheses")
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def evaluate_postfix(self, postfix_tokens):
        """
        Evaluate a postfix notation expression.
        
        Args:
            postfix_tokens (list): The expression in postfix notation
            
        Returns:
            float: The result of the calculation
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is malformed
        """
        stack = []
        
        for token in postfix_tokens:
            if self.is_number(token):
                stack.append(float(token))
            elif token in self.operators:
                if len(stack) < 2:
                    raise ValueError("Invalid expression format")
                
                # Pop the two operands (notice the order - important for subtraction and division)
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
        
        if len(stack) != 1:
            raise ValueError("Invalid expression format")
        
        return stack[0]
    
    def calculate(self, expression):
        """
        Evaluate a mathematical expression.
        
        Args:
            expression (str): The mathematical expression to evaluate
            
        Returns:
            float: The result of the calculation
            
        Raises:
            ValueError: If the expression is invalid
            ZeroDivisionError: If division by zero is attempted
        """
        if not expression or not expression.strip():
            raise ValueError("Empty expression")
        
        # Tokenize the expression
        tokens = self.tokenize(expression)
        
        # Convert to postfix notation
        postfix = self.infix_to_postfix(tokens)
        
        # Evaluate the postfix expression
        result = self.evaluate_postfix(postfix)
        
        return result


# Example usage:
if __name__ == "__main__":
    calc = Calculator()
    
    # Test cases
    test_expressions = [
        "2 + 3",
        "5 - 2",
        "3 * 4",
        "10 / 2",
        "2 + 3 * 4",
        "(2 + 3) * 4",
        "2.5 + 3.5",
        "-5 + 10",
        "10 / (2 * 5)",
        "2 * (3 + (4 - 1))"
    ]
    
    print("Calculator Test Cases:")
    print("-" * 30)
    
    for expr in test_expressions:
        try:
            result = calc.calculate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} => Error: {e}")
    
    # Interactive mode
    print("\nInteractive Calculator (type 'exit' to quit)")
    print("-" * 40)
    
    while True:
        user_input = input("Enter an expression: ")
        if user_input.lower() == 'exit':
            break
            
        try:
            result = calc.calculate(user_input)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
