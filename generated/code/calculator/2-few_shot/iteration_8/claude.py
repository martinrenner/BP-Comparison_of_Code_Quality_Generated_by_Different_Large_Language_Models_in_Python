from typing import List, Union, Optional
import re


class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions
    following standard operator precedence rules.
    
    This calculator supports:
    - Basic arithmetic operations: addition (+), subtraction (-), 
      multiplication (*), and division (/)
    - Parentheses for grouping expressions
    - Both integer and floating-point numbers, including negative values
    
    The implementation follows a two-step process:
    1. Tokenization: Converts the input string into a list of tokens
    2. Evaluation: Uses the Shunting Yard algorithm to evaluate the expression
    """

    def __init__(self):
        """Initialize the Calculator object."""
        # Define the operators and their precedence
        self.operators = {
            '+': {'precedence': 1, 'associativity': 'left'},
            '-': {'precedence': 1, 'associativity': 'left'},
            '*': {'precedence': 2, 'associativity': 'left'},
            '/': {'precedence': 2, 'associativity': 'left'}
        }

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.

        Args:
            expression (str): A string containing a mathematical expression with
                              numbers, operators (+, -, *, /), and parentheses.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression contains invalid characters or has
                       unbalanced parentheses.
            ZeroDivisionError: If the expression involves division by zero.
            SyntaxError: If the expression has syntax errors.
        """
        # Validate and normalize the expression
        normalized_expr = self._normalize_expression(expression)
        
        # Check for balanced parentheses
        if not self._is_balanced_parentheses(normalized_expr):
            raise ValueError("Unbalanced parentheses in the expression.")
        
        # Tokenize the expression
        tokens = self._tokenize(normalized_expr)
        
        # Convert infix notation to postfix notation (Reverse Polish Notation)
        postfix = self._infix_to_postfix(tokens)
        
        # Evaluate the postfix expression
        result = self._evaluate_postfix(postfix)
        
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.

        Args:
            expression (str): A mathematical expression as a string.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Check if expression is empty or None
        if not expression or expression.isspace():
            raise ValueError("Expression cannot be empty.")
            
        # Define allowed characters (numbers, operators, parentheses, decimal point, and whitespace)
        allowed_chars = set("0123456789+-*/().eE ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        # Remove whitespace
        return expression.replace(" ", "")

    def _is_balanced_parentheses(self, expression: str) -> bool:
        """
        Checks whether parentheses in the expression are properly balanced.

        Args:
            expression (str): A mathematical expression.

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
        Converts a string expression into a list of tokens.

        Args:
            expression (str): A normalized mathematical expression.

        Returns:
            List[str]: A list of tokens (numbers, operators, parentheses).
            
        Raises:
            SyntaxError: If the expression contains syntax errors.
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Handle parentheses and operators
            if char in "()+-*/":
                tokens.append(char)
                i += 1
            # Handle numbers (including decimals and scientific notation)
            elif char.isdigit() or char == '.':
                # Check if it's a negative number
                if char == '-' and (i == 0 or expression[i-1] in '(+-*/'):
                    number_str = char
                    i += 1
                else:
                    number_str = ""
                
                # Collect all digits, decimal points, and scientific notation
                while i < len(expression) and (expression[i].isdigit() or 
                                               expression[i] == '.' or 
                                               expression[i].lower() == 'e' or 
                                               (expression[i] in '+-' and i > 0 and expression[i-1].lower() == 'e')):
                    number_str += expression[i]
                    i += 1
                
                try:
                    # Convert to float and then back to string to handle any formatting issues
                    float(number_str)
                    tokens.append(number_str)
                except ValueError:
                    raise SyntaxError(f"Invalid number format: {number_str}")
            else:
                i += 1  # Skip any unexpected characters (already validated)
        
        # Check for syntax errors like consecutive operators
        for i in range(len(tokens) - 1):
            if (tokens[i] in self.operators and tokens[i+1] in self.operators):
                raise SyntaxError(f"Invalid syntax: consecutive operators '{tokens[i]}{tokens[i+1]}'")
        
        return tokens

    def _infix_to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Converts an infix expression to postfix notation using the Shunting Yard algorithm.

        Args:
            tokens (List[str]): A list of tokens in infix notation.

        Returns:
            List[str]: A list of tokens in postfix notation.
            
        Raises:
            SyntaxError: If the expression has mismatched parentheses.
        """
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            # Handle numbers
            if token not in self.operators and token not in "()":
                output_queue.append(token)
            
            # Handle operators
            elif token in self.operators:
                while (operator_stack and operator_stack[-1] != "(" and
                      (self.operators[operator_stack[-1]]['precedence'] > self.operators[token]['precedence'] or
                       (self.operators[operator_stack[-1]]['precedence'] == self.operators[token]['precedence'] and
                        self.operators[token]['associativity'] == 'left'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            
            # Handle left parenthesis
            elif token == "(":
                operator_stack.append(token)
            
            # Handle right parenthesis
            elif token == ")":
                while operator_stack and operator_stack[-1] != "(":
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == "(":
                    operator_stack.pop()  # Discard the left parenthesis
                else:
                    raise SyntaxError("Mismatched parentheses")
        
        # Pop any remaining operators
        while operator_stack:
            if operator_stack[-1] == "(":
                raise SyntaxError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
            
        return output_queue

    def _evaluate_postfix(self, postfix: List[str]) -> float:
        """
        Evaluates a postfix expression.

        Args:
            postfix (List[str]): A list of tokens in postfix notation.

        Returns:
            float: The result of the evaluation.
            
        Raises:
            ZeroDivisionError: If division by zero is attempted.
            SyntaxError: If the expression is malformed.
        """
        operand_stack = []
        
        for token in postfix:
            if token not in self.operators:
                # If token is a number, push it onto the stack
                operand_stack.append(float(token))
            else:
                # If token is an operator, pop operands and apply the operation
                if len(operand_stack) < 2:
                    raise SyntaxError("Invalid expression: not enough operands")
                
                right_operand = operand_stack.pop()
                left_operand = operand_stack.pop()
                
                if token == "+":
                    operand_stack.append(left_operand + right_operand)
                elif token == "-":
                    operand_stack.append(left_operand - right_operand)
                elif token == "*":
                    operand_stack.append(left_operand * right_operand)
                elif token == "/":
                    if right_operand == 0:
                        raise ZeroDivisionError("Division by zero")
                    operand_stack.append(left_operand / right_operand)
        
        # The final result should be the only item on the stack
        if len(operand_stack) != 1:
            raise SyntaxError("Invalid expression: too many operands")
            
        return operand_stack[0]


def main():
    """
    Main function for running the calculator from the command line.
    """
    calculator = Calculator()
    
    print("Console Calculator")
    print("Enter 'quit' or 'exit' to end the program")
    
    while True:
        try:
            expression = input("\nEnter expression: ")
            
            if expression.lower() in ["quit", "exit"]:
                print("Exiting calculator. Goodbye!")
                break
                
            result = calculator.calculate(expression)
            
            # Format the result to avoid unnecessary decimal places
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
                
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
