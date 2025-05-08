class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    This calculator supports basic arithmetic operations (+, -, *, /), 
    parentheses, and follows the correct order of operations.
    """
    
    def __init__(self):
        """Initialize the Calculator."""
        self.operators = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression (str): A string containing a mathematical expression
                              (e.g., "3 + 4 * (2 - 1)")
        
        Returns:
            float: The result of evaluating the expression
            
        Raises:
            ValueError: If the expression contains invalid characters or syntax
            ZeroDivisionError: If the expression involves division by zero
            SyntaxError: If the expression has unbalanced parentheses
        """
        # Remove all whitespace
        expression = expression.replace(" ", "")
        
        # Check for empty expression
        if not expression:
            raise ValueError("Empty expression")
        
        # Check for invalid characters
        valid_chars = set('0123456789.+-*/() ')
        if not all(c in valid_chars for c in expression):
            raise ValueError("Expression contains invalid characters")
            
        # Check for balanced parentheses
        if not self._check_parentheses(expression):
            raise SyntaxError("Unbalanced parentheses in the expression")
            
        # Parse and evaluate the expression
        return self._evaluate_expression(expression)
    
    def _check_parentheses(self, expression: str) -> bool:
        """
        Check if parentheses in the expression are balanced.
        
        Args:
            expression (str): The expression to check
            
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
    
    def _evaluate_expression(self, expression: str) -> float:
        """
        Evaluate the given expression using the shunting yard algorithm.
        
        Args:
            expression (str): The expression to evaluate
            
        Returns:
            float: The result of evaluating the expression
        """
        # Convert infix to postfix using the shunting yard algorithm
        postfix = self._infix_to_postfix(expression)
        
        # Evaluate the postfix expression
        return self._evaluate_postfix(postfix)
    
    def _infix_to_postfix(self, expression: str) -> list:
        """
        Convert an infix expression to postfix using the shunting yard algorithm.
        
        Args:
            expression (str): The infix expression to convert
            
        Returns:
            list: The postfix representation of the expression
        """
        output = []
        operator_stack = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Handle numbers (including decimals and negatives)
            if char.isdigit() or (char == '-' and (i == 0 or expression[i-1] in '(+-*/')):
                # Handle negative numbers
                if char == '-':
                    output.append('0')  # Add 0 before negative for proper evaluation
                    operator_stack.append('-')
                    i += 1
                    continue
                
                # Extract the full number
                number = char
                j = i + 1
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    number += expression[j]
                    j += 1
                
                output.append(number)
                i = j
                continue
            
            # Handle operators
            if char in self.operators:
                while (operator_stack and operator_stack[-1] != '(' and
                       (operator_stack[-1] in self.operators) and
                       (self.operators[operator_stack[-1]] >= self.operators[char])):
                    output.append(operator_stack.pop())
                operator_stack.append(char)
            
            # Handle left parenthesis
            elif char == '(':
                operator_stack.append(char)
            
            # Handle right parenthesis
            elif char == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Discard the left parenthesis
                else:
                    raise SyntaxError("Mismatched parentheses")
            
            i += 1
        
        # Pop any remaining operators
        while operator_stack:
            if operator_stack[-1] == '(':
                raise SyntaxError("Mismatched parentheses")
            output.append(operator_stack.pop())
            
        return output
    
    def _evaluate_postfix(self, postfix: list) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix (list): The postfix expression to evaluate
            
        Returns:
            float: The result of evaluating the expression
            
        Raises:
            ZeroDivisionError: If the expression involves division by zero
        """
        operand_stack = []
        
        for token in postfix:
            if token in self.operators:
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                
                # Pop operands in reverse order
                b = float(operand_stack.pop())
                a = float(operand_stack.pop())
                
                # Perform operation
                if token == '+':
                    operand_stack.append(a + b)
                elif token == '-':
                    operand_stack.append(a - b)
                elif token == '*':
                    operand_stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero is not allowed")
                    operand_stack.append(a / b)
            else:
                # Token is a number
                operand_stack.append(token)
        
        if len(operand_stack) != 1:
            raise ValueError("Invalid expression: too many operands")
            
        return float(operand_stack[0])


def main():
    """Main function to demonstrate the Calculator class."""
    calc = Calculator()
    
    print("Console-based Arithmetic Calculator")
    print("Enter 'exit' to quit.")
    print("Supported operations: +, -, *, / and parentheses ()")
    
    while True:
        try:
            expression = input("\nEnter an expression: ")
            if expression.lower() == 'exit':
                break
                
            result = calc.calculate(expression)
            print(f"Result: {result}")
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
