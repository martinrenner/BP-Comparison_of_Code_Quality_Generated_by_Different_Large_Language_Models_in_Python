class Calculator:
    """
    A calculator class that evaluates arithmetic expressions.
    
    This calculator supports:
    - Addition (+), subtraction (-), multiplication (*), and division (/)
    - Parentheses for expression grouping
    - Proper operator precedence
    - Both integer and floating-point numbers, including negative values
    
    The implementation follows the shunting-yard algorithm for parsing expressions
    and evaluating them without using eval() or similar functions.
    """
    
    def __init__(self):
        """Initialize the calculator."""
        self.operators = {
            '+': {'precedence': 1, 'associativity': 'left'},
            '-': {'precedence': 1, 'associativity': 'left'},
            '*': {'precedence': 2, 'associativity': 'left'},
            '/': {'precedence': 2, 'associativity': 'left'},
        }
        
    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return the result.
        
        Args:
            expression (str): The arithmetic expression to evaluate
            
        Returns:
            float: The result of the expression evaluation
            
        Raises:
            ValueError: If the expression contains invalid characters or is malformed
            ZeroDivisionError: If the expression attempts division by zero
            SyntaxError: If the expression has unbalanced parentheses or other syntax issues
        """
        # Normalize and validate the expression
        normalized_expr = self._normalize_expression(expression)
        
        # Check for balanced parentheses
        if not self._is_balanced_parentheses(normalized_expr):
            raise SyntaxError("Unbalanced parentheses in expression.")
            
        # Convert to postfix notation and evaluate
        postfix = self._infix_to_postfix(normalized_expr)
        return self._evaluate_postfix(postfix)
        
    def _normalize_expression(self, expression: str) -> str:
        """
        Normalize the expression by removing spaces and validating characters.
        
        Args:
            expression (str): The input arithmetic expression
            
        Returns:
            str: The normalized expression
            
        Raises:
            ValueError: If the expression contains invalid characters
        """
        # Remove all whitespace
        normalized = expression.replace(" ", "")
        
        # Check for valid characters
        allowed_chars = set("0123456789.+-*/()eE")
        if not all(char in allowed_chars for char in normalized):
            raise ValueError("Expression contains invalid characters.")
            
        # Handle special cases like unary minus
        # Replace instances like "(-" with "(0-" to handle negative numbers at start of parentheses
        normalized = normalized.replace("(-", "(0-")
        
        # Handle negative numbers at the start of the expression
        if normalized.startswith("-"):
            normalized = "0" + normalized
            
        return normalized
        
    def _is_balanced_parentheses(self, expression: str) -> bool:
        """
        Check if the expression has balanced parentheses.
        
        Args:
            expression (str): The normalized expression to check
            
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
        
    def _infix_to_postfix(self, expression: str) -> list:
        """
        Convert an infix expression to postfix notation using the shunting-yard algorithm.
        
        Args:
            expression (str): The normalized infix expression
            
        Returns:
            list: The expression in postfix notation as a list of tokens
            
        Raises:
            SyntaxError: If the expression has invalid syntax
        """
        output_queue = []
        operator_stack = []
        
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # If it's a digit, parse the entire number
            if char.isdigit() or char == '.':
                # Extract the complete number
                number_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    number_str += expression[i]
                    i += 1
                
                try:
                    # Convert to float and add to output
                    output_queue.append(float(number_str))
                except ValueError:
                    raise SyntaxError(f"Invalid number format: {number_str}")
                
                # Adjust i since we've already processed characters
                i -= 1
            
            # If it's an operator
            elif char in self.operators:
                while (operator_stack and 
                       operator_stack[-1] != '(' and
                       (self.operators[operator_stack[-1]]['precedence'] > self.operators[char]['precedence'] or
                        (self.operators[operator_stack[-1]]['precedence'] == self.operators[char]['precedence'] and
                         self.operators[char]['associativity'] == 'left'))):
                    output_queue.append(operator_stack.pop())
                    
                operator_stack.append(char)
                
            # If it's a left parenthesis
            elif char == '(':
                operator_stack.append(char)
                
            # If it's a right parenthesis
            elif char == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                    
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Discard the left parenthesis
                else:
                    raise SyntaxError("Mismatched parentheses in expression.")
            
            # Invalid character (should be caught by normalization)
            else:
                raise ValueError(f"Unexpected character: {char}")
                
            i += 1
                
        # Pop any remaining operators from the stack
        while operator_stack:
            if operator_stack[-1] == '(':
                raise SyntaxError("Mismatched parentheses in expression.")
            output_queue.append(operator_stack.pop())
            
        return output_queue
        
    def _evaluate_postfix(self, postfix: list) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix (list): The expression in postfix notation
            
        Returns:
            float: The result of the expression evaluation
            
        Raises:
            ZeroDivisionError: If a division by zero is attempted
            SyntaxError: If the expression is invalid (e.g., not enough operands)
        """
        stack = []
        
        for token in postfix:
            # If token is a number, push to stack
            if isinstance(token, (int, float)):
                stack.append(token)
                
            # If token is an operator, pop operands and compute
            else:
                if len(stack) < 2:
                    raise SyntaxError("Invalid expression: insufficient operands.")
                    
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                if token == '+':
                    stack.append(left_operand + right_operand)
                elif token == '-':
                    stack.append(left_operand - right_operand)
                elif token == '*':
                    stack.append(left_operand * right_operand)
                elif token == '/':
                    if right_operand == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    stack.append(left_operand / right_operand)
                    
        if len(stack) != 1:
            raise SyntaxError("Invalid expression: too many operands.")
            
        return stack[0]


def main():
    """Main function to demonstrate the calculator."""
    calculator = Calculator()
    
    print("Console Arithmetic Calculator")
    print("Type 'exit' to quit.")
    
    while True:
        try:
            expression = input("\nEnter an expression: ")
            
            if expression.lower() == 'exit':
                print("Exiting calculator.")
                break
                
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
