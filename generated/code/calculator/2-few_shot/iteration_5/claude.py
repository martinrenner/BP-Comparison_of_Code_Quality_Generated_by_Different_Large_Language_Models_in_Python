from typing import List, Union, Dict, Callable
import re


class Calculator:
    """
    A console-based arithmetic calculator supporting basic operations.
    
    This calculator handles addition, subtraction, multiplication, division,
    and respects parentheses and operator precedence. It processes both
    integers and floating-point numbers.
    """
    
    def __init__(self) -> None:
        """Initialize the calculator with operators and their precedence."""
        # Define operator precedence (higher value means higher precedence)
        self.operators: Dict[str, int] = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }
        
        # Define operation functions
        self.operations: Dict[str, Callable[[float, float], float]] = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': self._safe_division
        }
    
    def _safe_division(self, a: float, b: float) -> float:
        """
        Perform division with zero-division check.
        
        Args:
            a (float): Dividend
            b (float): Divisor
            
        Returns:
            float: Result of division
            
        Raises:
            ZeroDivisionError: If divisor is zero
        """
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return a / b
    
    def _validate_expression(self, expression: str) -> None:
        """
        Validate the expression for syntax errors.
        
        Args:
            expression (str): Mathematical expression to validate
            
        Raises:
            ValueError: If expression contains invalid characters or syntax errors
            SyntaxError: If parentheses are unbalanced
        """
        # Check for valid characters
        allowed_chars = set("0123456789+-*/().e ")
        if not all(char.lower() in allowed_chars for char in expression):
            invalid_chars = [char for char in expression if char.lower() not in allowed_chars]
            raise ValueError(f"Expression contains invalid characters: {invalid_chars}")
        
        # Check for balanced parentheses
        open_count = expression.count('(')
        close_count = expression.count(')')
        if open_count != close_count:
            raise SyntaxError("Unbalanced parentheses in the expression.")
        
        # Check for empty expression
        if expression.strip() == "":
            raise ValueError("Expression cannot be empty.")
        
        # Check for invalid syntax patterns
        invalid_patterns = [
            r'[+\-*/]{2,}',  # Multiple operators in sequence
            r'\(\s*\)',       # Empty parentheses
            r'\d\s+\d',       # Numbers with spaces between them
            r'\d\(',          # Number immediately followed by opening parenthesis
            r'\)[0-9]'        # Closing parenthesis immediately followed by number
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, expression):
                raise SyntaxError(f"Invalid syntax in expression: matches pattern '{pattern}'")
    
    def _tokenize(self, expression: str) -> List[str]:
        """
        Convert expression string into a list of tokens.
        
        Args:
            expression (str): Mathematical expression to tokenize
            
        Returns:
            List[str]: List of tokens (numbers and operators)
        """
        # Normalize expression by removing spaces
        expression = expression.replace(" ", "")
        
        # Add spaces around operators and parentheses for easier splitting
        for char in "+-*/()":
            expression = expression.replace(char, f" {char} ")
        
        # Split and filter out empty strings
        return [token for token in expression.split() if token]
    
    def _parse_tokens(self, tokens: List[str]) -> float:
        """
        Parse tokens using the Shunting Yard algorithm and evaluate.
        
        Args:
            tokens (List[str]): List of tokens to parse
            
        Returns:
            float: Result of the evaluated expression
            
        Raises:
            ValueError: If invalid tokens are encountered
            SyntaxError: If expression syntax is incorrect
        """
        # Output queue (for numbers and operators in postfix order)
        output_queue: List[Union[float, str]] = []
        
        # Operator stack
        operator_stack: List[str] = []
        
        for token in tokens:
            # If token is a number
            if self._is_number(token):
                output_queue.append(float(token))
            
            # If token is an operator
            elif token in self.operators:
                # While there are operators on the stack with higher or equal precedence
                while (operator_stack and 
                       operator_stack[-1] in self.operators and 
                       self.operators[operator_stack[-1]] >= self.operators[token]):
                    output_queue.append(operator_stack.pop())
                
                # Push current operator onto the stack
                operator_stack.append(token)
            
            # If token is an opening parenthesis
            elif token == '(':
                operator_stack.append(token)
            
            # If token is a closing parenthesis
            elif token == ')':
                # Until we find the matching opening parenthesis
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                # Remove the opening parenthesis
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
                else:
                    raise SyntaxError("Mismatched parentheses in expression.")
            
            else:
                raise ValueError(f"Unknown token: {token}")
        
        # Move remaining operators to output queue
        while operator_stack:
            if operator_stack[-1] == '(':
                raise SyntaxError("Mismatched parentheses in expression.")
            output_queue.append(operator_stack.pop())
        
        # Evaluate the postfix expression
        return self._evaluate_postfix(output_queue)
    
    def _is_number(self, token: str) -> bool:
        """
        Check if a token is a valid number.
        
        Args:
            token (str): Token to check
            
        Returns:
            bool: True if token is a valid number, False otherwise
        """
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def _evaluate_postfix(self, queue: List[Union[float, str]]) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            queue (List[Union[float, str]]): Postfix expression as a list of tokens
            
        Returns:
            float: Result of the evaluated expression
            
        Raises:
            SyntaxError: If the expression is invalid
        """
        # Stack for operands
        operand_stack: List[float] = []
        
        for token in queue:
            # If token is a number
            if isinstance(token, (int, float)):
                operand_stack.append(token)
            
            # If token is an operator
            elif token in self.operations:
                if len(operand_stack) < 2:
                    raise SyntaxError("Invalid expression: insufficient operands for operator.")
                
                b = operand_stack.pop()
                a = operand_stack.pop()
                
                # Perform the operation and push result to stack
                result = self.operations[token](a, b)
                operand_stack.append(result)
        
        # The final result should be the only item on the stack
        if len(operand_stack) != 1:
            raise SyntaxError("Invalid expression: too many operands.")
        
        return operand_stack[0]
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression.
        
        Args:
            expression (str): Mathematical expression to evaluate
            
        Returns:
            float: Result of the evaluated expression
            
        Raises:
            ValueError: If expression is invalid
            SyntaxError: If expression has syntax errors
            ZeroDivisionError: If division by zero is attempted
        """
        # Validate the expression
        self._validate_expression(expression)
        
        # Tokenize the expression
        tokens = self._tokenize(expression)
        
        # Parse and evaluate the tokens
        return self._parse_tokens(tokens)


def main() -> None:
    """Run the calculator program with user input."""
    calculator = Calculator()
    print("Console Calculator")
    print("Enter 'quit' or 'exit' to exit the program.")
    
    while True:
        try:
            expression = input("\nEnter an expression: ")
            
            if expression.lower() in ('quit', 'exit'):
                print("Goodbye!")
                break
            
            result = calculator.calculate(expression)
            
            # Format result to avoid unnecessary decimal places
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except (ValueError, SyntaxError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
