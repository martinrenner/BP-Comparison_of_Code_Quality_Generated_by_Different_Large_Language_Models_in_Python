class Calculator:
    """
    A console-based arithmetic calculator that supports basic operations with
    correct operator precedence and parentheses.

    This calculator implements the requirements of ISO/IEC 25010 with a focus on
    functionality, reliability, usability, and maintainability.
    
    Supported operations:
    - Addition (+)
    - Subtraction (-)
    - Multiplication (*)
    - Division (/)
    - Parentheses for grouping operations
    """

    def __init__(self):
        """Initialize the calculator."""
        # Supported operators and their precedence
        self.operators = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result.

        Args:
            expression (str): The arithmetic expression to evaluate.
                              Supports +, -, *, /, and parentheses.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression contains invalid characters, unbalanced 
                        parentheses, or is syntactically incorrect.
            ZeroDivisionError: If division by zero is attempted.
            ArithmeticError: For other calculation errors.
        """
        # Normalize and validate the expression
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("Unbalanced parentheses in the expression.")

        # Check for syntax errors
        self._check_syntax(normalized_expr)

        # Parse the expression using Shunting Yard algorithm
        tokens = self._tokenize(normalized_expr)
        rpn = self._to_reverse_polish_notation(tokens)
        
        # Evaluate the expression in RPN form
        return self._evaluate_rpn(rpn)

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.

        Args:
            expression (str): A mathematical expression as a string.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters or is empty.
        """
        if not expression or expression.isspace():
            raise ValueError("Expression cannot be empty.")

        allowed_chars = set("0123456789+-*/().e ")
        if not all(char.lower() in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether the expression has properly balanced parentheses.

        Args:
            expression (str): The arithmetic expression to check.

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

    def _check_syntax(self, expression: str) -> None:
        """
        Checks the expression for basic syntax errors.

        Args:
            expression (str): The normalized expression to check.

        Raises:
            ValueError: If syntax errors are found.
        """
        # Check for empty expression between parentheses
        if '()' in expression:
            raise ValueError("Empty parentheses are not allowed.")
            
        # Check for consecutive operators
        prev_char = None
        for i, char in enumerate(expression):
            # Handle unary operators
            if char in '+-' and (i == 0 or prev_char in '(+-*/'):
                continue
                
            if char in self.operators and prev_char in self.operators:
                raise ValueError(f"Invalid consecutive operators at position {i}")
                
            prev_char = char
            
        # Check for invalid starting/ending with operators
        if expression[-1] in self.operators:
            raise ValueError("Expression cannot end with an operator.")

    def _tokenize(self, expression: str) -> list:
        """
        Converts the expression string into a list of tokens (numbers and operators).

        Args:
            expression (str): The normalized expression to tokenize.

        Returns:
            list: A list of tokens (numbers, operators, parentheses).
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # Handle numbers (including negatives and decimals)
            if char.isdigit() or (char in '+-' and (i == 0 or expression[i-1] in '(+-*/')) and i+1 < len(expression) and expression[i+1].isdigit():
                # Start of a number
                num_start = i
                
                # Handle unary operators (+ or -) preceding a number
                if char in '+-':
                    i += 1
                    
                # Continue while we're still processing the number
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    i += 1
                    
                # Extract the number substring and convert to float
                number_str = expression[num_start:i]
                try:
                    number = float(number_str)
                    # Convert to integer if it's a whole number
                    if number.is_integer():
                        number = int(number)
                    tokens.append(number)
                except ValueError:
                    raise ValueError(f"Invalid number format: {number_str}")
            # Handle operators and parentheses
            elif char in self.operators or char in '()':
                tokens.append(char)
                i += 1
            else:
                # Should not reach here after validation, but included for robustness
                raise ValueError(f"Unexpected character: {char}")
        
        return tokens

    def _to_reverse_polish_notation(self, tokens: list) -> list:
        """
        Converts an infix expression to Reverse Polish Notation (RPN) using the Shunting Yard algorithm.

        Args:
            tokens (list): List of tokens from the expression.

        Returns:
            list: The expression in RPN form.
        """
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            # If token is a number, add to output
            if isinstance(token, (int, float)):
                output_queue.append(token)
            # If token is an operator
            elif token in self.operators:
                # While there's an operator on the stack with higher/equal precedence
                while (operator_stack and 
                       operator_stack[-1] in self.operators and 
                       self.operators[token] <= self.operators[operator_stack[-1]]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            # If token is a left parenthesis, push to stack
            elif token == '(':
                operator_stack.append(token)
            # If token is a right parenthesis, pop from stack until matching left parenthesis
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                
                # Remove the left parenthesis
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
                else:
                    # This should never happen with balanced parentheses
                    raise ValueError("Mismatched parentheses")
        
        # Pop any remaining operators from the stack to the output
        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
            
        return output_queue

    def _evaluate_rpn(self, rpn: list) -> float:
        """
        Evaluates an expression in Reverse Polish Notation.

        Args:
            rpn (list): The expression in RPN form.

        Returns:
            float: The result of the evaluation.

        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ArithmeticError: For other calculation errors.
        """
        if not rpn:
            raise ValueError("Empty expression")
            
        stack = []
        
        for token in rpn:
            if isinstance(token, (int, float)):
                stack.append(token)
            else:
                # Need at least two operands for any operation
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                
                # Pop operands in reverse order (right operand first)
                right_operand = stack.pop()
                left_operand = stack.pop()
                
                # Perform operation
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
        
        # The final result should be the only item left on the stack
        if len(stack) != 1:
            raise ArithmeticError("Invalid expression: too many operands")
            
        return stack[0]


def main():
    """
    Command-line interface for the calculator.
    Allows users to enter expressions and see results.
    """
    calculator = Calculator()
    
    print("Console Calculator - Type 'exit' to quit")
    print("Supported operations: +, -, *, / and parentheses ()")
    
    while True:
        try:
            expression = input("\nEnter expression: ")
            
            if expression.lower() == 'exit':
                print("Exiting calculator. Goodbye!")
                break
                
            result = calculator.calculate(expression)
            
            # Display the result (show as integer if it's a whole number)
            if isinstance(result, float) and result.is_integer():
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
