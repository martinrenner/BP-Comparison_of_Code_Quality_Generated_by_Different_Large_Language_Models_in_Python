"""
A console-based arithmetic calculator that supports basic operations,
parentheses, and correct operator precedence. This implementation adheres
to ISO/IEC 25010 quality requirements including correctness, performance,
modularity, safety, testability, and readability.

Supported operations:
  - Addition (+)
  - Subtraction (-)
  - Multiplication (*)
  - Division (/)

Features:
  • Supports integer and floating point numbers (including negative numbers)
  • Provides input validation (e.g., unbalanced parentheses, invalid characters, division by zero)
  • Uses Object-Oriented Programming (OOP): Class Calculator with the interface calculate(expression: str) -> float
  • Does not use eval() or similar methods for evaluating expressions

Usage:
  Run the module and enter arithmetic expressions at the console. Type 'quit' or 'exit' to end.
"""

class Calculator:
    """
    A class that evaluates arithmetic expressions using the Shunting Yard algorithm
    and postfix expression evaluation.
    """
    
    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression and returns the result as a float.
        
        Parameters:
            expression (str): The arithmetic expression to evaluate.
            
        Returns:
            float: The result of the evaluated expression.
            
        Raises:
            ValueError: If the expression contains invalid characters or mismatched parentheses.
            ZeroDivisionError: If there is an attempt to divide by zero.
        """
        tokens = self._tokenize(expression)
        postfix = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix)
        return result

    def _tokenize(self, expression: str) -> list:
        """
        Converts the input expression string into a list of tokens (numbers and operators).
        
        Supports:
          • Integer and floating point numbers (optionally with a unary '+' or '-' sign).
          • The operators: +, -, *, /
          • Parentheses: ( and )
        
        Parameters:
            expression (str): The arithmetic expression.
            
        Returns:
            list: A list of tokens where numbers are of type float and other tokens are strings.
            
        Raises:
            ValueError: If an invalid character is found.
        """
        tokens = []
        i = 0
        length = len(expression)
        
        while i < length:
            char = expression[i]
            
            # Skip any whitespace
            if char.isspace():
                i += 1
                continue

            # Check for a unary operator (only '+' or '-' allowed as a sign) attached to a number.
            if char in '+-' and (i == 0 or (tokens and isinstance(tokens[-1], str) and tokens[-1] in "+-*/(")):
                # Look ahead to ensure a number follows the unary sign.
                if i + 1 < length and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                    sign = char  # Preserve the '-' sign; ignore '+' as it doesn't change the number.
                    i += 1
                    num_str = ""
                    # Collect digits and at most one decimal point.
                    decimal_found = False
                    while i < length and (expression[i].isdigit() or (expression[i] == '.' and not decimal_found)):
                        if expression[i] == '.':
                            decimal_found = True
                        num_str += expression[i]
                        i += 1
                    if not num_str:
                        raise ValueError("Invalid syntax: missing number after unary operator.")
                    # Prepend the sign if negative.
                    token_value = float(sign + num_str) if sign == '-' else float(num_str)
                    tokens.append(token_value)
                    continue
                else:
                    # Not a valid unary sign if not followed by a digit or a dot.
                    raise ValueError("Invalid syntax: unexpected unary operator usage.")
            
            # If the current character is a digit or a dot, parse it as a (float) number.
            if char.isdigit() or char == '.':
                num_str = ""
                decimal_found = False
                while i < length and (expression[i].isdigit() or (expression[i] == '.' and not decimal_found)):
                    if expression[i] == '.':
                        decimal_found = True
                    num_str += expression[i]
                    i += 1
                try:
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: {num_str}")
                continue

            # If the character is a valid operator or parenthesis, add it as a token.
            if char in "+-*/()":
                tokens.append(char)
                i += 1
                continue
            
            # If we reach here, the character is not recognized.
            raise ValueError(f"Invalid character found: '{char}'")
            
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts a list of tokens in infix notation to postfix notation (Reverse Polish Notation)
        using the Shunting Yard algorithm.
        
        Parameters:
            tokens (list): List of tokens in infix order.
            
        Returns:
            list: List of tokens in postfix order.
            
        Raises:
            ValueError: If there are mismatched parentheses.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            if isinstance(token, float):
                # If token is a number, add it to the output queue.
                output_queue.append(token)
            elif token in precedence:
                # While there is an operator at the top of the stack with greater or equal precedence,
                # pop it to the output queue.
                while operator_stack and operator_stack[-1] in precedence and precedence[operator_stack[-1]] >= precedence[token]:
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                # Pop operators until the corresponding '(' is encountered.
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                # If the stack is empty before finding '(', it's a mismatched parenthesis.
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop()  # Pop the '(' from the stack.
            else:
                # This should not happen; any token other than number, operator, or parenthesis is invalid.
                raise ValueError(f"Invalid token encountered: {token}")
                
        # Pop any remaining operators from the operator stack.
        while operator_stack:
            op = operator_stack.pop()
            if op in '()':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)
            
        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix (Reverse Polish Notation) expression.
        
        Parameters:
            tokens (list): List of tokens in postfix order.
            
        Returns:
            float: The result of the evaluated expression.
            
        Raises:
            ValueError: If there is an error in the expression structure.
            ZeroDivisionError: If division by zero occurs.
        """
        stack = []
        
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in "+-*/":
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient values for operation.")
                b = stack.pop()
                a = stack.pop()
                result = None
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero encountered in expression.")
                    result = a / b
                stack.append(result)
            else:
                raise ValueError(f"Invalid token encountered during evaluation: {token}")
                
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many values remaining after evaluation.")
        
        return stack[0]

if __name__ == '__main__':
    calc = Calculator()
    print("Console-based Arithmetic Calculator")
    print("Type an arithmetic expression to evaluate (or 'quit' to exit).")
    
    while True:
        try:
            user_input = input(">> ").strip()
            if user_input.lower() in ("quit", "exit"):
                print("Exiting calculator.")
                break
            # Calculate and print the result.
            result = calc.calculate(user_input)
            print("Result:", result)
        except (ValueError, ZeroDivisionError) as err:
            print("Error:", err)
        except Exception as unexpected_err:
            print("Unexpected error:", unexpected_err)
