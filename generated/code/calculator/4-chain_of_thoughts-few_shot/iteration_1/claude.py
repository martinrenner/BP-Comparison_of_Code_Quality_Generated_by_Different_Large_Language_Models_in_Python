from typing import List, Tuple, Union, Optional
import re


class Calculator:
    """
    A calculator class that can evaluate arithmetic expressions.
    
    This calculator supports:
    - Basic operations: addition, subtraction, multiplication, division
    - Parentheses for controlling operation precedence
    - Decimal and negative numbers
    - Order of operations (PEMDAS)
    """
    
    # Regular expression for validating input characters
    VALID_CHARS_PATTERN = r'^[0-9+\-*/().\s]*$'
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.
        
        Args:
            expression (str): The mathematical expression to evaluate.
            
        Returns:
            float: The result of the expression.
            
        Raises:
            ValueError: If the expression contains invalid characters or has syntax errors.
            ZeroDivisionError: If the expression includes division by zero.
        """
        # Validate and normalize the expression
        normalized_expr = self._normalize_expression(expression)
        
        # Check for balanced parentheses
        if not self._is_balanced_parentheses(normalized_expr):
            raise ValueError("Unbalanced parentheses in expression.")
        
        # Tokenize the expression
        tokens = self._tokenize(normalized_expr)
        
        # Convert to postfix notation (Reverse Polish Notation)
        postfix = self._to_postfix(tokens)
        
        # Evaluate the postfix notation
        return self._evaluate_postfix(postfix)
    
    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression by removing spaces and validating characters.
        
        Args:
            expression (str): The expression to normalize.
            
        Returns:
            str: The normalized expression.
            
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Check if expression contains only valid characters
        if not re.match(self.VALID_CHARS_PATTERN, expression):
            raise ValueError("Expression contains invalid characters.")
        
        # Remove whitespace
        normalized = expression.replace(" ", "")
        
        # Handle consecutive operators like '+-' -> '-', '--' -> '+', etc.
        # This is a simple handling - a more robust solution would use proper parsing
        normalized = normalized.replace("+-", "-")
        normalized = normalized.replace("-+", "-")
        normalized = normalized.replace("--", "+")
        
        return normalized
    
    def _is_balanced_parentheses(self, expression: str) -> bool:
        """
        Checks if parentheses in the expression are balanced.
        
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
    
    def _tokenize(self, expression: str) -> List[str]:
        """
        Converts an expression string into a list of tokens.
        
        Args:
            expression (str): The expression to tokenize.
            
        Returns:
            List[str]: A list of tokens (numbers and operators).
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Handle operators and parentheses
            if char in "+-*/()":
                # Special case for unary operators
                if char in "+-" and (i == 0 or expression[i-1] in "+-*/("): 
                    # Unary operator
                    number_start = i
                    i += 1
                    # Get the number after the unary operator
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        i += 1
                    tokens.append(expression[number_start:i])
                else:
                    tokens.append(char)
                    i += 1
            
            # Handle numbers (including decimals)
            elif char.isdigit() or char == '.':
                number_start = i
                i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    i += 1
                tokens.append(expression[number_start:i])
            
            else:
                i += 1
        
        return tokens
    
    def _get_precedence(self, operator: str) -> int:
        """
        Returns the precedence of an operator.
        
        Args:
            operator (str): The operator whose precedence to return.
            
        Returns:
            int: The precedence value (higher means higher precedence).
        """
        if operator in "+-":
            return 1
        if operator in "*/":
            return 2
        return 0  # For parentheses or other characters
    
    def _to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Converts infix notation tokens to postfix notation (Shunting Yard algorithm).
        
        Args:
            tokens (List[str]): The tokens in infix notation.
            
        Returns:
            List[str]: The tokens in postfix notation.
        """
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            # If token is a number, add to output
            if self._is_number(token):
                output_queue.append(token)
            
            # Left parenthesis, push to stack
            elif token == '(':
                operator_stack.append(token)
            
            # Right parenthesis, pop from stack until left parenthesis
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                # Discard the left parenthesis
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
                else:
                    raise ValueError("Mismatched parentheses.")
            
            # Operator
            elif token in "+-*/":
                while (operator_stack and 
                       operator_stack[-1] != '(' and 
                       self._get_precedence(operator_stack[-1]) >= self._get_precedence(token)):
                    output_queue.append(operator_stack.pop())
                
                operator_stack.append(token)
        
        # Pop any remaining operators from the stack to the output
        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses.")
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _is_number(self, token: str) -> bool:
        """
        Checks if a token is a number (including negative numbers).
        
        Args:
            token (str): The token to check.
            
        Returns:
            bool: True if token is a number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def _evaluate_postfix(self, postfix_tokens: List[str]) -> float:
        """
        Evaluates a postfix expression.
        
        Args:
            postfix_tokens (List[str]): The tokens in postfix notation.
            
        Returns:
            float: The result of the evaluation.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ValueError: If the expression is invalid.
        """
        operand_stack = []
        
        for token in postfix_tokens:
            if self._is_number(token):
                operand_stack.append(float(token))
            else:  # Operator
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands.")
                
                b = operand_stack.pop()
                a = operand_stack.pop()
                
                if token == '+':
                    operand_stack.append(a + b)
                elif token == '-':
                    operand_stack.append(a - b)
                elif token == '*':
                    operand_stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero is not allowed.")
                    operand_stack.append(a / b)
        
        if len(operand_stack) != 1:
            raise ValueError("Invalid expression: too many operands.")
        
        return operand_stack[0]


# Demo usage
def main():
    calculator = Calculator()
    
    try:
        # Example expressions
        expressions = [
            "2 + 3",
            "5 - 2",
            "3 * 4",
            "10 / 2",
            "2 + 3 * 4",
            "(2 + 3) * 4",
            "2.5 + 3.5",
            "-5 + 10",
            "10 / 0",  # Will raise ZeroDivisionError
            "2 + * 3"  # Will raise ValueError (invalid syntax)
        ]
        
        for expr in expressions:
            try:
                result = calculator.calculate(expr)
                print(f"{expr} = {result}")
            except Exception as e:
                print(f"{expr} → Error: {e}")
                
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
