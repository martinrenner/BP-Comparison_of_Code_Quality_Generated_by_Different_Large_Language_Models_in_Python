#!/usr/bin/env python3
"""
A console-based arithmetic calculator that complies with ISO/IEC 25010 quality requirements.
It supports addition (+), subtraction (-), multiplication (*), and division (/), including
handling of parentheses and respecting the correct order of operations. Input numbers can be
integers or decimals (including negative numbers).

This module implements the Calculator class using an object‐oriented approach with clear
modularity, error handling, and documentation for maintainability and testability.
"""

class Calculator:
    """
    A simple arithmetic calculator that evaluates mathematical expressions.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression string and returns the result as a float.
        
        Args:
            expression (str): The arithmetic expression to evaluate.
            
        Returns:
            float: The result of the evaluation.
            
        Raises:
            ValueError: If the expression has invalid syntax (e.g., unbalanced parentheses,
                        invalid characters, or malformed numbers).
            ZeroDivisionError: If division by zero is attempted.
        """
        tokens = self._tokenize(expression)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _tokenize(self, expression: str) -> list:
        """
        Converts the input expression string into a list of tokens (numbers and operators).
        Supports unary plus and minus. Raises ValueError on invalid characters or malformed numbers.
        
        Args:
            expression (str): The arithmetic expression.
            
        Returns:
            list: A list of tokens (floats for numbers, str for operators/parentheses).
        """
        tokens = []
        i = 0
        length = len(expression)
        while i < length:
            char = expression[i]

            # Skip whitespace
            if char.isspace():
                i += 1
                continue

            # If the character is a digit or a decimal point, parse a number.
            if char.isdigit() or char == '.':
                num_str = ''
                dot_count = 0
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid numeric format: multiple decimal points in a number.")
                    num_str += expression[i]
                    i += 1
                try:
                    number = float(num_str)
                except ValueError:
                    raise ValueError(f"Invalid numeric literal: {num_str}")
                tokens.append(number)
                continue

            # Handle potential unary plus or minus
            if char in '+-':
                # Determine if the plus/minus is unary: either at the beginning
                # of the expression or following an operator or an opening parenthesis.
                if (len(tokens) == 0 or 
                    (isinstance(tokens[-1], str) and tokens[-1] in "+-*/(")):
                    # Check what follows the unary operator.
                    # If the next non-space character is a digit or a dot, read the number.
                    # Alternatively, if it's an opening parenthesis, transform the unary
                    # operator into "0 <op>" to facilitate evaluation.
                    j = i + 1
                    # Skip any intermediate spaces.
                    while j < length and expression[j].isspace():
                        j += 1
                    if j < length and (expression[j].isdigit() or expression[j] == '.'):
                        # Parse the number with its sign.
                        sign = char
                        num_str = sign
                        i += 1  # Move past the sign.
                        dot_count = 0
                        while i < length and (expression[i].isdigit() or expression[i] == '.'):
                            if expression[i] == '.':
                                dot_count += 1
                                if dot_count > 1:
                                    raise ValueError("Invalid numeric format: multiple decimal points in a number.")
                            num_str += expression[i]
                            i += 1
                        try:
                            number = float(num_str)
                        except ValueError:
                            raise ValueError(f"Invalid numeric literal: {num_str}")
                        tokens.append(number)
                        continue
                    elif j < length and expression[j] == '(':
                        # For an expression like "-(3+2)", convert it to "0 - (3+2)".
                        tokens.append(0.0)
                        tokens.append(char)
                        i += 1
                        continue
                    else:
                        raise ValueError("Invalid expression: unary operator not followed by a valid number or '('.")
                else:
                    # Binary operator
                    tokens.append(char)
                    i += 1
                    continue

            # Handle multiplication and division operators.
            if char in "*/":
                tokens.append(char)
                i += 1
                continue

            # Handle parentheses.
            if char in "()":
                tokens.append(char)
                i += 1
                continue

            # If none of the valid characters match, raise an exception.
            raise ValueError(f"Invalid character in expression: '{char}'")
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts an infix notation list of tokens into postfix notation using the shunting-yard algorithm.
        
        Args:
            tokens (list): List of tokens in infix order.
            
        Returns:
            list: List of tokens in postfix order.
            
        Raises:
            ValueError: If there are unbalanced parentheses in the input tokens.
        """
        output_queue = []
        operator_stack = []
        # Define operator precedence: higher value means higher precedence.
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            # If the token is a number, add it directly to the output queue.
            if isinstance(token, float):
                output_queue.append(token)
            # If the token is an operator.
            elif token in precedence:
                # Pop from the operator stack to the output queue while the operator at the top
                # of the stack has greater or equal precedence.
                while (operator_stack and operator_stack[-1] in precedence and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            # If the token is an opening parenthesis, push it onto the stack.
            elif token == '(':
                operator_stack.append(token)
            # If the token is a closing parenthesis, pop operators until an opening parenthesis is found.
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Unbalanced parentheses in expression.")
                # Discard the opening parenthesis.
                operator_stack.pop()
            else:
                # Should not reach here if tokenization is correct.
                raise ValueError(f"Unknown token encountered: {token}")

        # Pop any remaining operators on the stack.
        while operator_stack:
            op = operator_stack.pop()
            if op in "()":
                raise ValueError("Unbalanced parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix (Reverse Polish Notation) expression represented as a list of tokens.
        
        Args:
            tokens (list): A list of tokens in postfix order.
            
        Returns:
            float: The result of the evaluated expression.
            
        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: If the expression is malformed.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in "+-*/":
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient values for operation.")
                # It's important to note: when popping from the stack for a binary operation,
                # the first value popped is the right operand and the second is the left operand.
                right = stack.pop()
                left = stack.pop()
                result = None
                if token == '+':
                    result = left + right
                elif token == '-':
                    result = left - right
                elif token == '*':
                    result = left * right
                elif token == '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero encountered in expression.")
                    result = left / right
                stack.append(result)
            else:
                # Should not occur if previous steps are correct.
                raise ValueError(f"Unknown token in postfix expression: {token}")

        if len(stack) != 1:
            raise ValueError("Malformed expression: too many values remain after evaluation.")

        return stack[0]


def main():
    """
    The main function provides a simple console interface for the arithmetic calculator.
    Users can input arithmetic expressions, and the result will be displayed.
    Type 'exit' or 'quit' to end the program.
    """
    calc = Calculator()
    print("Welcome to the ISO/IEC 25010 compliant arithmetic calculator.")
    print("Supported operators: +, -, *, / and parentheses ().")
    print("Enter 'exit' or 'quit' to close the calculator.\n")

    while True:
        expression = input("Enter expression: ").strip()
        if expression.lower() in ("exit", "quit"):
            print("Exiting calculator.")
            break

        try:
            result = calc.calculate(expression)
        except Exception as e:
            print("Error:", e)
        else:
            print("Result:", result)
        print()  # Print a blank line for readability


if __name__ == "__main__":
    main()
