#!/usr/bin/env python3
"""
Console-based Arithmetic Calculator

This module implements a Calculator class that evaluates arithmetic expressions.
It supports addition (+), subtraction (-), multiplication (*), division (/),
and parentheses for grouping with correct operator precedence.
Both integer and floating-point numbers (including negative values) are supported.

The implementation follows ISO/IEC 25010 requirements in functionality, performance,
modularity, security, testability, and readability. The expression is parsed without
using eval() or similar insecure functions.
"""

class Calculator:
    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression provided as a string.

        Supported operators: +, -, *, /
        Supports parentheses for grouping, operator precedence,
        integers, floating-point numbers, and negative values.

        Parameters:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression contains unbalanced parentheses,
                        invalid characters, or an invalid number format.
            ZeroDivisionError: If a division by zero is encountered.
        """
        tokens = self._tokenize(expression)
        postfix_tokens = self._to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _tokenize(self, expression: str) -> list:
        """
        Convert the input expression string into a list of tokens.
        Tokens can be floats (numbers), operators, or parentheses.
        Handles negative numbers by distinguishing unary minus
        from the subtraction operator.

        Parameters:
            expression (str): The arithmetic expression string.

        Returns:
            list: A list of tokens where numbers are converted to floats.

        Raises:
            ValueError: If an invalid character is encountered
                        or if the number format is incorrect.
        """
        tokens = []
        i = 0
        n = len(expression)
        allowed_characters = "0123456789.+-*/() "  # Define allowed characters

        # Validate characters up-front for security and correctness.
        for ch in expression:
            if ch not in allowed_characters:
                raise ValueError(f"Invalid character encountered: {ch}")

        while i < n:
            ch = expression[i]
            if ch.isspace():
                i += 1
                continue
            # Check for unary minus: if '-' is at the beginning or preceded by an operator or '('.
            if ch == '-' and (i == 0 or expression[i - 1] in "(+-*/"):
                # Peek ahead to see if a number follows the unary minus.
                j = i + 1
                if j < n and (expression[j].isdigit() or expression[j] == '.'):
                    num_str = '-'  # Include the negative sign.
                    dot_count = 0
                    while j < n and (expression[j].isdigit() or expression[j] == '.'):
                        if expression[j] == '.':
                            dot_count += 1
                            if dot_count > 1:
                                raise ValueError("Invalid number format: multiple decimals in a number.")
                        num_str += expression[j]
                        j += 1
                    try:
                        number = float(num_str)
                    except ValueError:
                        raise ValueError("Invalid number format encountered.")
                    tokens.append(number)
                    i = j
                    continue
                else:
                    # If no number follows, treat '-' as a subtraction operator.
                    tokens.append(ch)
                    i += 1
                    continue
            # Parse a positive number if the character is a digit or a dot.
            elif ch.isdigit() or ch == '.':
                j = i
                num_str = ""
                dot_count = 0
                while j < n and (expression[j].isdigit() or expression[j] == '.'):
                    if expression[j] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid number format: multiple decimals in a number.")
                    num_str += expression[j]
                    j += 1
                try:
                    number = float(num_str)
                except ValueError:
                    raise ValueError("Invalid number format encountered.")
                tokens.append(number)
                i = j
                continue
            elif ch in "+*/":
                tokens.append(ch)
                i += 1
                continue
            elif ch in "()":
                tokens.append(ch)
                i += 1
                continue
            else:
                # This else should never be reached because of the allowed characters check.
                raise ValueError(f"Invalid character encountered: {ch}")
        
        # Final check for balanced parentheses.
        if tokens.count('(') != tokens.count(')'):
            raise ValueError("Unbalanced parentheses detected in the expression.")
        return tokens

    def _to_postfix(self, tokens: list) -> list:
        """
        Convert an infix expression (list of tokens) into a postfix expression
        (Reverse Polish Notation) using the shunting-yard algorithm.

        Parameters:
            tokens (list): A list of tokens, where numbers are floats.

        Returns:
            list: A list of tokens in postfix order.

        Raises:
            ValueError: If unbalanced parentheses are detected.
        """
        output_queue = []
        operator_stack = []
        # Define operator precedence
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in precedence:
                while (
                    operator_stack and operator_stack[-1] in precedence and
                    precedence[operator_stack[-1]] >= precedence[token]
                ):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                # Pop from stack to output until an '(' is encountered.
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Unbalanced parentheses encountered.")
                operator_stack.pop()  # Remove the '(' from the stack.
            else:
                raise ValueError("Unknown token encountered during parsing.")

        # Pop any remaining operators from the stack.
        while operator_stack:
            op = operator_stack.pop()
            if op in ("(", ")"):
                raise ValueError("Unbalanced parentheses encountered.")
            output_queue.append(op)
        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluate a postfix expression represented as a list of tokens.

        Parameters:
            tokens (list): The postfix expression tokens (numbers and operators).

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression format is invalid.
            ZeroDivisionError: If a division by zero is attempted.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in {'+', '-', '*', '/'}:
                if len(stack) < 2:
                    raise ValueError("Insufficient values in the expression for the operation.")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero encountered.")
                    result = a / b
                stack.append(result)
            else:
                raise ValueError("Unknown token encountered during evaluation.")
        if len(stack) != 1:
            raise ValueError("The expression could not be evaluated properly.")
        return stack[0]

if __name__ == "__main__":
    calc = Calculator()
    print("Console-based Arithmetic Calculator")
    print("Enter an arithmetic expression (or type 'exit' to quit):")
    while True:
        try:
            expr = input(">> ")
            if expr.lower() == "exit":
                break
            result = calc.calculate(expr)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
