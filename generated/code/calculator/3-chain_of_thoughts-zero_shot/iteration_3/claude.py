class Calculator:
    """
    A calculator class that evaluates arithmetic expressions.
    
    This class implements a calculator that can handle basic arithmetic operations
    (addition, subtraction, multiplication, division) with proper order of operations
    and support for parentheses.
    """
    
    def __init__(self):
        """Initialize the Calculator object."""
        # Define the operators and their precedence
        self.operators = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return the result.
        
        Args:
            expression: A string containing the arithmetic expression to evaluate.
                        Supports +, -, *, /, parentheses, integers and decimal numbers.
        
        Returns:
            The calculated result as a float.
            
        Raises:
            ValueError: If the expression contains invalid characters or has syntax errors.
            ZeroDivisionError: If the expression involves division by zero.
            SyntaxError: If the parentheses in the expression are not balanced.
        """
        # Remove all whitespace from the expression
        expression = expression.replace(' ', '')
        
        if not expression:
            raise ValueError("Expression cannot be empty")
        
        # Validate the expression
        self._validate_expression(expression)
        
        # Tokenize the expression
        tokens = self._tokenize(expression)
        
        # Convert infix notation to postfix (Reverse Polish Notation)
        postfix = self._infix_to_postfix(tokens)
        
        # Evaluate the postfix expression
        return self._evaluate_postfix(postfix)
    
    def _validate_expression(self, expression: str) -> None:
        """
        Validate the input expression for common errors.
        
        Args:
            expression: The expression to validate.
            
        Raises:
            ValueError: If the expression contains invalid characters.
            SyntaxError: If the parentheses in the expression are not balanced.
        """
        # Check for balanced parentheses
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise SyntaxError("Unbalanced parentheses in expression")
                stack.pop()
        
        if stack:
            raise SyntaxError("Unbalanced parentheses in expression")
        
        # Check for invalid characters
        allowed_chars = set("0123456789.+-*/() ")
        for char in expression:
            if char not in allowed_chars:
                raise ValueError(f"Invalid character in expression: '{char}'")
        
        # Check for consecutive operators
        for i in range(len(expression) - 1):
            if expression[i] in "+-*/" and expression[i+1] in "+-*/":
                raise ValueError(f"Invalid consecutive operators: '{expression[i]}{expression[i+1]}'")
        
        # Check if expression starts with an invalid operator
        if expression and expression[0] in "*/":
            raise ValueError(f"Expression cannot start with '{expression[0]}'")
        
        # Check if expression ends with an operator
        if expression and expression[-1] in "+-*/":
            raise ValueError("Expression cannot end with an operator")
    
    def _tokenize(self, expression: str) -> list:
        """
        Convert the expression string into a list of tokens.
        
        Args:
            expression: The expression to tokenize.
            
        Returns:
            A list of tokens (numbers and operators).
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Handle parentheses and operators
            if char in "()+-*/":
                tokens.append(char)
                i += 1
            
            # Handle numbers (integers and decimals)
            elif char.isdigit() or (char == '.' and i + 1 < len(expression) and expression[i + 1].isdigit()):
                # Start of a number
                number_str = char
                i += 1
                
                # Continue collecting digits and at most one decimal point
                decimal_point_encountered = char == '.'
                
                while i < len(expression) and (expression[i].isdigit() or (expression[i] == '.' and not decimal_point_encountered)):
                    if expression[i] == '.':
                        decimal_point_encountered = True
                    number_str += expression[i]
                    i += 1
                
                # Convert to float and add to tokens
                tokens.append(float(number_str))
            
            else:
                i += 1
        
        # Handle unary operators (e.g., convert -5 to 0-5)
        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] == '(' or tokens[i-1] in self.operators):
                # This is a unary minus
                processed_tokens.append(0)  # Add 0 before to make it a subtraction
                processed_tokens.append(token)
            elif token == '+' and (i == 0 or tokens[i-1] == '(' or tokens[i-1] in self.operators):
                # This is a unary plus, we can ignore it
                continue
            else:
                processed_tokens.append(token)
        
        return processed_tokens
    
    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Convert infix notation to postfix notation (Reverse Polish Notation).
        
        Args:
            tokens: A list of tokens in infix notation.
            
        Returns:
            A list of tokens in postfix notation.
        """
        output = []
        operator_stack = []
        
        for token in tokens:
            # If token is a number, add it to output
            if isinstance(token, (int, float)):
                output.append(token)
            
            # If token is an opening parenthesis, push it to the stack
            elif token == '(':
                operator_stack.append(token)
            
            # If token is a closing parenthesis, pop operators until opening parenthesis
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                
                # Remove the opening parenthesis
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
                else:
                    raise SyntaxError("Mismatched parentheses")
            
            # If token is an operator
            elif token in self.operators:
                # Pop operators with higher or equal precedence and add to output
                while (operator_stack and 
                       operator_stack[-1] != '(' and 
                       operator_stack[-1] in self.operators and 
                       self.operators[operator_stack[-1]] >= self.operators[token]):
                    output.append(operator_stack.pop())
                
                # Push current operator to stack
                operator_stack.append(token)
        
        # Pop any remaining operators and add to output
        while operator_stack:
            if operator_stack[-1] == '(':
                raise SyntaxError("Mismatched parentheses")
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, postfix: list) -> float:
        """
        Evaluate a postfix expression.
        
        Args:
            postfix: A list of tokens in postfix notation.
            
        Returns:
            The result of the evaluation as a float.
            
        Raises:
            ZeroDivisionError: If the expression involves division by zero.
        """
        result_stack = []
        
        for token in postfix:
            # If token is a number, push it to the stack
            if isinstance(token, (int, float)):
                result_stack.append(token)
            
            # If token is an operator, pop two values, apply the operator, and push the result
            elif token in self.operators:
                if len(result_stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                
                b = result_stack.pop()
                a = result_stack.pop()
                
                if token == '+':
                    result_stack.append(a + b)
                elif token == '-':
                    result_stack.append(a - b)
                elif token == '*':
                    result_stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    result_stack.append(a / b)
        
        # The final result should be the only value on the stack
        if len(result_stack) != 1:
            raise ValueError("Invalid expression: too many operands")
        
        return result_stack[0]


def main():
    """
    Main function to demonstrate the Calculator functionality.
    Provides a simple command-line interface to use the calculator.
    """
    calculator = Calculator()
    print("Console Calculator")
    print("Enter 'exit' or 'quit' to end the program")
    
    while True:
        try:
            expression = input("\nEnter an expression: ")
            if expression.lower() in ['exit', 'quit']:
                print("Exiting calculator")
                break
            
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        
        except (ValueError, SyntaxError, ZeroDivisionError) as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
