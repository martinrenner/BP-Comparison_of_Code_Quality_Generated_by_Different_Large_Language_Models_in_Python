from typing import List, Union, Dict
import re


class Calculator:
    """
    A calculator that evaluates arithmetic expressions with proper operator precedence.
    
    Supports:
    - Basic operations: addition, subtraction, multiplication, division
    - Parentheses for expression grouping
    - Negative numbers and floating-point values
    """
    
    def __init__(self):
        """Initialize the calculator with operator definitions."""
        # Define operators and their precedence (higher value = higher precedence)
        self.operators: Dict[str, Dict] = {
            '+': {'precedence': 1, 'function': lambda a, b: a + b},
            '-': {'precedence': 1, 'function': lambda a, b: a - b},
            '*': {'precedence': 2, 'function': lambda a, b: a * b},
            '/': {'precedence': 2, 'function': lambda a, b: a / b},
        }
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result.
        
        Args:
            expression: A string containing an arithmetic expression
            
        Returns:
            The result of the evaluated expression as a float
            
        Raises:
            ValueError: If the expression is invalid (e.g., syntax error)
            ZeroDivisionError: If division by zero is attempted
            SyntaxError: If parentheses are unbalanced
        """
        # Remove all whitespace from the expression
        expression = expression.replace(' ', '')
        
        # Validate the expression
        self._validate_expression(expression)
        
        # Parse and evaluate the expression
        return self._evaluate_expression(expression)
    
    def _validate_expression(self, expression: str) -> None:
        """
        Validates the expression for correct syntax.
        
        Args:
            expression: The expression to validate
            
        Raises:
            ValueError: If invalid characters are found
            SyntaxError: If parentheses are unbalanced
        """
        # Check for invalid characters
        valid_chars = set("0123456789.+-*/() ")
        invalid_chars = set(char for char in expression if char not in valid_chars)
        if invalid_chars:
            raise ValueError(f"Invalid characters in expression: {', '.join(invalid_chars)}")
        
        # Check for balanced parentheses
        open_count = expression.count('(')
        close_count = expression.count(')')
        if open_count != close_count:
            raise SyntaxError("Unbalanced parentheses in expression")
        
        # Check for empty expression
        if not expression:
            raise ValueError("Expression cannot be empty")
            
        # Check for invalid syntax patterns
        # Check for consecutive operators
        if re.search(r'[+\-*/][+*/]', expression):
            raise ValueError("Invalid syntax: consecutive operators")
            
        # Check for operators at the end
        if expression[-1] in "+-*/":
            raise ValueError("Invalid syntax: expression cannot end with an operator")
            
        # Ensure there's content between parentheses
        if re.search(r'\(\)', expression):
            raise ValueError("Invalid syntax: empty parentheses")
            
        # Double decimal point in a number
        if re.search(r'\d+\.\d*\.\d*', expression):
            raise ValueError("Invalid syntax: multiple decimal points in a number")
    
    def _evaluate_expression(self, expression: str) -> float:
        """
        Evaluates the expression using the Shunting Yard algorithm.
        
        Args:
            expression: The expression to evaluate
            
        Returns:
            The result of the evaluated expression
        """
        # Convert infix expression to postfix notation (using the Shunting Yard algorithm)
        postfix = self._infix_to_postfix(expression)
        
        # Evaluate the postfix expression
        return self._evaluate_postfix(postfix)
    
    def _infix_to_postfix(self, expression: str) -> List:
        """
        Converts an infix expression to postfix notation using the Shunting Yard algorithm.
        
        Args:
            expression: The infix expression
            
        Returns:
            A list of tokens in postfix order
        """
        output_queue = []
        operator_stack = []
        
        # Process the token stream
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # Handle numbers (including negative numbers and decimals)
            if char.isdigit() or (char == '-' and (i == 0 or expression[i-1] in '(+-*/')):
                # Determine if it's a negative number
                is_negative = char == '-'
                if is_negative:
                    i += 1
                    if i >= len(expression) or not (expression[i].isdigit() or expression[i] == '.'):
                        raise ValueError("Invalid syntax: isolated negative sign")
                
                # Extract the number
                start = i
                decimal_point_found = False
                
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        if decimal_point_found:
                            raise ValueError("Invalid number format: multiple decimal points")
                        decimal_point_found = True
                    i += 1
                    
                # Parse the number
                number_str = expression[start:i]
                try:
                    number = float(number_str)
                    if is_negative:
                        number = -number
                    output_queue.append(number)
                except ValueError:
                    raise ValueError(f"Invalid number format: {number_str}")
                
                # Adjust i because the loop will increment it again
                i -= 1
            
            # Handle operators
            elif char in self.operators:
                while (operator_stack and operator_stack[-1] != '(' and 
                       self.operators.get(operator_stack[-1], {}).get('precedence', 0) >= 
                       self.operators.get(char, {}).get('precedence', 0)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(char)
            
            # Handle opening parenthesis
            elif char == '(':
                operator_stack.append(char)
            
            # Handle closing parenthesis
            elif char == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Discard the opening parenthesis
                else:
                    raise SyntaxError("Mismatched parentheses")
            
            # Move to the next character
            i += 1
        
        # Pop any remaining operators from the stack to the output queue
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise SyntaxError("Mismatched parentheses")
            output_queue.append(op)
        
        return output_queue
    
    def _evaluate_postfix(self, postfix: List) -> float:
        """
        Evaluates a postfix expression.
        
        Args:
            postfix: The postfix expression as a list of tokens
            
        Returns:
            The result of the evaluated expression
            
        Raises:
            ZeroDivisionError: If division by zero is attempted
            ValueError: If the expression is syntactically incorrect
        """
        stack = []
        
        for token in postfix:
            if isinstance(token, (int, float)):
                stack.append(token)
            elif token in self.operators:
                if len(stack) < 2:
                    raise ValueError("Invalid expression syntax")
                
                b = stack.pop()
                a = stack.pop()
                
                if token == '/' and b == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                
                result = self.operators[token]['function'](a, b)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many values")
        
        return stack[0]


def main():
    """Main function to run the calculator from the command line."""
    calculator = Calculator()
    
    print("Arithmetic Calculator")
    print("Enter 'exit' to quit")
    
    while True:
        expression = input("\nEnter an expression: ")
        
        if expression.lower() in ('exit', 'quit'):
            break
        
        try:
            result = calculator.calculate(expression)
            
            # Format the output - display as integer if it's a whole number
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    print("Calculator closed.")


if __name__ == "__main__":
    main()
