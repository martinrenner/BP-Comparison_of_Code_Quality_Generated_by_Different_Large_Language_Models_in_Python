#!/usr/bin/env python3
"""
Console-based Arithmetic Calculator
This module implements a simple arithmetic calculator that supports
addition (+), subtraction (-), multiplication (*), division (/),
and parentheses (). It properly handles order of operations and supports
integers, decimal numbers, and negative values.

The implementation follows ISO/IEC 25010 quality attributes such as
correctness, performance, modularity, safety, testability, and maintainability.
"""

class Calculator:
    """
    Calculator class that evaluates arithmetic expressions using
    a three-step process: tokenization, conversion to Reverse Polish Notation (RPN)
    via the shunting-yard algorithm, and evaluation of the RPN expression.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result as a float.

        Parameters:
            expression (str): A string representing the arithmetic expression.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression is invalid (e.g. contains invalid characters,
                        unbalanced parentheses, or improper numeric values).
            ZeroDivisionError: If there is a division by zero in the expression.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        return self._evaluate_rpn(rpn)

    def _tokenize(self, expr: str) -> list:
        """
        Converts the input expression into a list of tokens. Tokens can be numeric values (float)
        or operators: '+', '-', '*', '/', '(', ')'. Supports detecting unary plus and unary minus.

        Parameters:
            expr (str): The arithmetic expression as a string.

        Returns:
            list: A list containing numbers (float) and operator tokens (str).

        Raises:
            ValueError: If the expression contains invalid characters or malformed numbers.
        """
        tokens = []
        i = 0
        n = len(expr)
        while i < n:
            char = expr[i]
            if char.isspace():
                i += 1
                continue

            # Handle unary plus and minus if they appear at the beginning
            # or immediately following an operator or '('.
            if char in "+-":
                if i == 0 or (tokens and (isinstance(tokens[-1], str) and tokens[-1] in "+-*/(")):
                    # Unary operator detected. Attempt to parse a number.
                    sign = char
                    i += 1
                    num_str = sign
                    # There must be a digit or a decimal point following the unary operator.
                    if i < n and (expr[i].isdigit() or expr[i] == '.'):
                        # Parse the numeric part.
                        dot_count = 0
                        while i < n and (expr[i].isdigit() or expr[i] == '.'):
                            if expr[i] == '.':
                                dot_count += 1
                                if dot_count > 1:
                                    raise ValueError("Invalid numeric format: multiple decimal points")
                            num_str += expr[i]
                            i += 1
                        try:
                            number = float(num_str)
                        except ValueError:
                            raise ValueError(f"Invalid numeric value: {num_str}")
                        tokens.append(number)
                        continue
                    else:
                        raise ValueError(f"Invalid use of unary operator '{sign}'")
                else:
                    # It's a binary operator.
                    tokens.append(char)
                    i += 1
                    continue

            # Handle numeric tokens (digits and decimal point).
            elif char.isdigit() or char == '.':
                num_str = ""
                dot_count = 0
                while i < n and (expr[i].isdigit() or expr[i] == '.'):
                    if expr[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid numeric format: multiple decimal points")
                    num_str += expr[i]
                    i += 1
                try:
                    number = float(num_str)
                except ValueError:
                    raise ValueError(f"Invalid numeric value: {num_str}")
                tokens.append(number)
                continue

            # Handle operators and parentheses.
            elif char in "*/()":
                tokens.append(char)
                i += 1
                continue

            # Any other character is invalid.
            else:
                raise ValueError(f"Invalid character found: {char}")

        return tokens

    def _to_rpn(self, tokens: list) -> list:
        """
        Transforms the list of tokens from infix notation to Reverse Polish Notation (RPN)
        using the shunting-yard algorithm.

        Parameters:
            tokens (list): List of tokens (numbers and operators) from the tokenization process.

        Returns:
            list: Tokens arranged in RPN order.

        Raises:
            ValueError: If there are mismatched parentheses or unknown tokens.
        """
        output_queue = []
        operator_stack = []
        # Define operator precedence.
        precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2
        }

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in precedence:
                while (operator_stack and operator_stack[-1] in precedence and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == "(":
                operator_stack.append(token)
            elif token == ")":
                # Pop operators until a left parenthesis is encountered.
                while operator_stack and operator_stack[-1] != "(":
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses: no matching '(' found for ')'")
                operator_stack.pop()  # Remove the '('
            else:
                raise ValueError(f"Unknown token: {token}")

        # After processing all tokens, pop any remaining operators.
        while operator_stack:
            op = operator_stack.pop()
            if op in ("(", ")"):
                raise ValueError("Mismatched parentheses in the expression")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_tokens: list) -> float:
        """
        Evaluates the expression given in Reverse Polish Notation.

        Parameters:
            rpn_tokens (list): List of tokens in RPN order.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid.
            ZeroDivisionError: If a division by zero is encountered.
        """
        stack = []
        for token in rpn_tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in {"+", "-", "*", "/"}:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient values for operation")
                b = stack.pop()
                a = stack.pop()
                if token == "+":
                    result = a + b
                elif token == "-":
                    result = a - b
                elif token == "*":
                    result = a * b
                elif token == "/":
                    if b == 0:
                        raise ZeroDivisionError("Division by zero is not allowed")
                    result = a / b
                stack.append(result)
            else:
                raise ValueError(f"Unknown token in RPN evaluation: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression: too many or too few operands")
        return stack[0]


def main():
    """
    The main loop for the console-based arithmetic calculator.
    Continually prompts the user for an expression to evaluate until 'exit' is entered.
    """
    calc = Calculator()
    print("Console-based Arithmetic Calculator")
    print("Supported operations: +, -, *, / and parentheses ().")
    print("Enter 'exit' to quit.")

    while True:
        try:
            expression = input("Enter expression: ")
        except EOFError:
            # Handle end-of-file (Ctrl+D on Unix, Ctrl+Z on Windows)
            break

        if expression.strip().lower() == "exit":
            break

        if not expression.strip():
            continue  # Skip empty input

        try:
            result = calc.calculate(expression)
            print("Result:", result)
        except Exception as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
