class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    This calculator handles:
    - Basic operations: addition, subtraction, multiplication, and division
    - Parentheses for operation grouping
    - Proper operator precedence
    - Both integers and floating-point numbers (including negative values)
    
    The implementation follows proper validation techniques and uses an efficient
    parsing algorithm without relying on eval() or similar functions.
    """
    
    def __init__(self):
        """Initialize the Calculator class."""
        # Define the valid operators and their precedence
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
            expression (str): A string containing the mathematical expression to evaluate.
                              Supports +, -, *, / operations, parentheses, and numeric values.
        
        Returns:
            float: The result of evaluating the expression.
            
        Raises:
            ValueError: If the expression contains invalid characters or syntax.
            ZeroDivisionError: If the expression attempts to divide by zero.
            SyntaxError: If the expression has unbalanced parentheses or invalid structure.
        """
        # Normalize and validate the expression
        normalized_expr = self._normalize_expression(expression)
        self._validate_expression(normalized_expr)
        
        # Parse the expression using the Shunting Yard algorithm
        tokens = self._tokenize(normalized_expr)
        postfix = self._to_postfix(tokens)
        
        # Evaluate the expression in postfix notation
        return self._evaluate_postfix(postfix)
    
    def _normalize_expression(self, expression: str) -> str:
        """
        Remove spaces and validate that the expression only contains valid characters.
        
        Args:
            expression (str): The mathematical expression to normalize.
            
        Returns:
            str: The normalized expression with spaces removed.
            
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Define the allowed characters
        allowed_chars = set("0123456789+-*/().e ")
        
        # Check for invalid characters
        if not all(char in allowed_chars for char in expression):
            invalid_chars = [char for char in expression if char not in allowed_chars]
            raise ValueError(f"Expression contains invalid characters: {', '.join(repr(c) for c in invalid_chars)}")
        
        # Remove spaces
        return expression.replace(" ", "")
    
    def _validate_expression(self, expression: str) -> None:
        """
        Validate the expression for correct syntax.
        
        Args:
            expression (str): The expression to validate.
            
        Raises:
            SyntaxError: If the expression has unbalanced parentheses or invalid syntax.
            ValueError: If the expression is empty or has invalid structure.
        """
        if not expression:
            raise ValueError("Expression cannot be empty")
        
        # Check parentheses balance
        if not self._is_balanced_parentheses(expression):
            raise SyntaxError("Expression has unbalanced parentheses")
        
        # Additional syntax validations
        self._validate_syntax(expression)
    
    def _is_balanced_parentheses(self, expression: str) -> bool:
        """
        Check if parentheses in the expression are properly balanced.
        
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
    
    def _validate_syntax(self, expression: str) -> None:
        """
        Perform additional syntax validation checks.
        
        Args:
            expression (str): The expression to validate.
            
        Raises:
            SyntaxError: If syntax errors are found.
        """
        # Check for empty parentheses
        if '()' in expression:
            raise SyntaxError("Empty parentheses are not allowed")
        
        # Check for consecutive operators
        for i in range(len(expression) - 1):
            if expression[i] in self.operators and expression[i+1] in self.operators:
                raise SyntaxError(f"Consecutive operators found: '{expression[i]}{expression[i+1]}'")
        
        # Check for starting or ending with an operator (except negative numbers)
        if expression[0] in '+*/':
            raise SyntaxError(f"Expression cannot start with '{expression[0]}'")
        if expression[-1] in self.operators:
            raise SyntaxError(f"Expression cannot end with '{expression[-1]}'")
        
        # Check for operators after opening parenthesis (except negative sign)
        for i in range(len(expression) - 1):
            if expression[i] == '(' and expression[i+1] in '+*/':
                raise SyntaxError(f"Invalid syntax: '({expression[i+1]}'")
        
        # Check for operators before closing parenthesis
        for i in range(1, len(expression)):
            if expression[i] == ')' and expression[i-1] in self.operators:
                raise SyntaxError(f"Invalid syntax: '{expression[i-1]})'")
    
    def _tokenize(self, expression: str) -> list:
        """
        Convert an expression string into a list of tokens.
        
        Args:
            expression (str): The normalized expression to tokenize.
            
        Returns:
            list: A list of tokens (numbers and operators).
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Handle parentheses and operators
            if char in '()' or char in self.operators:
                # Special case for negative numbers
                if char == '-' and (i == 0 or expression[i-1] in '(' or expression[i-1] in self.operators):
                    # This is a negative sign, not a subtraction operator
                    j = i + 1
                    while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                        j += 1
                    
                    # Extract the negative number
                    number_str = expression[i:j]
                    try:
                        tokens.append(float(number_str))
                    except ValueError:
                        raise SyntaxError(f"Invalid number format: {number_str}")
                    i = j
                else:
                    tokens.append(char)
                    i += 1
            
            # Handle numbers
            elif char.isdigit() or char == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                
                # Extract the number
                number_str = expression[i:j]
                
                # Validate the number format
                if number_str.count('.') > 1:
                    raise SyntaxError(f"Invalid number format: {number_str}")
                
                try:
                    tokens.append(float(number_str))
                except ValueError:
                    raise SyntaxError(f"Invalid number format: {number_str}")
                
                i = j
            else:
                i += 1
        
        return tokens
    
    def _to_postfix(self, tokens: list) -> list:
        """
        Convert infix notation tokens to postfix notation using the Shunting Yard algorithm.
        
        Args:
            tokens (list): A list of tokens in infix notation.
            
        Returns:
            list: A list of tokens in postfix notation.
        """
        output = []
        operator_stack = []
        
        for token in tokens:
            # If token is a number
            if isinstance(token, float):
                output.append(token)
            
            # If token is an operator
            elif token in self.operators:
                while (operator_stack and operator_stack[-1] != '(' and 
                       (self.operators.get(operator_stack[-1], 0) >= self.operators.get(token, 0))):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            
            # If token is a left parenthesis
            elif token == '(':
                operator_stack.append(token)
            
            # If token is a right parenthesis
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Discard the left parenthesis
                else:
                    raise SyntaxError("Mismatched parentheses")
        
        # Pop remaining operators to output
        while operator_stack:
            if operator_stack[-1] == '(':
                raise SyntaxError("Mismatched parentheses")
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluate a postfix notation expression.
        
        Args:
            tokens (list): The postfix notation tokens to evaluate.
            
        Returns:
            float: The result of the evaluation.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ValueError: If the postfix expression is invalid.
        """
        stack = []
        
        for token in tokens:
            # If token is a number, push to stack
            if isinstance(token, float):
                stack.append(token)
            
            # If token is an operator, apply it to the top two elements in stack
            elif token in self.operators:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient values for operation")
                
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
        
        # After evaluation, stack should contain exactly one element (the result)
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many values")
        
        return stack[0]


def main():
    """
    Main function to run the calculator interactively.
    """
    calc = Calculator()
    print("Console-based Arithmetic Calculator")
    print("Enter 'q' to quit")
    print("Supported operations: +, -, *, / and parentheses")
    
    while True:
        try:
            expression = input("\nEnter expression: ")
            
            if expression.lower() in ['q', 'quit', 'exit']:
                print("Exiting calculator. Goodbye!")
                break
                
            result = calc.calculate(expression)
            
            # Format result to remove trailing zeros if it's a whole number
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
