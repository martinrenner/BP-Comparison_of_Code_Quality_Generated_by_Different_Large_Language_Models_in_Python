import re
from typing import Union


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression and returns the result.

        Args:
            expression: The arithmetic expression string.

        Returns:
            The result of the expression evaluation.

        Raises:
            ValueError: If the expression is invalid.  This includes:
                - Unbalanced parentheses.
                - Invalid characters.
                - Division by zero.
                - Consecutive operators.
                - Empty expression.
                - Missing operator between number and parenthesis.
                - Starting or ending with an invalid operator.
        """

        if not expression:
            raise ValueError("Expression cannot be empty.")

        expression = expression.replace(" ", "")  # Remove spaces for easier processing

        # Validate the expression (before tokenization for efficiency)
        self._validate_expression(expression)

        # "Tokenize", then convert to postfix, then evaluate postfix.
        tokens = self._tokenize(expression)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)

        return result

    def _validate_expression(self, expression: str):
        """Validates the given expression for common errors."""

        # 1. Check for balanced parentheses:
        paren_balance = 0
        for char in expression:
            if char == '(':
                paren_balance += 1
            elif char == ')':
                paren_balance -= 1
            if paren_balance < 0:
                raise ValueError("Unbalanced parentheses (too many closing).")
        if paren_balance != 0:
            raise ValueError("Unbalanced parentheses (too many opening).")

        # 2. Check for invalid characters:
        valid_chars_pattern = r"^[\d+\-*/().\s]+$"  # Allow digits, operators, parentheses, and whitespace
        if not re.match(valid_chars_pattern, expression):
            raise ValueError("Invalid characters in expression.")

        # 3. Check for consecutive operators (e.g., "++" or "*-")
        if re.search(r"[\+\-*/]{2,}", expression):
            raise ValueError("Consecutive operators are not allowed.")

        # 4. Check for operators at the beginning or end (except for unary minus):
        if len(expression) > 0 and expression[0] in "*/":
            raise ValueError("Expression cannot start with * or /.")
        if len(expression) > 0 and expression[-1] in "+-*/":
            raise ValueError("Expression cannot end with an operator.")


        # 5. Check for invalid positions of operators and parentheses:
        for i in range(len(expression) - 1):
            if expression[i] == '(' and expression[i+1] in '*/':
                 raise ValueError("Invalid operator after opening parenthesis.")
            if expression[i] in '+-*/' and expression[i+1] == ')':
                 raise ValueError("Invalid operator before closing parenthesis.")

        # 6. Check for missing operator between digit and opening parenthesis.
        if re.search(r'\d\(', expression) or re.search(r'\)\d', expression) :
            raise ValueError("Missing operator between number and parenthesis.")

    def _tokenize(self, expression: str) -> list[str]:
        """
        Tokenizes the expression string into a list of numbers and operators.

        Handles unary minus correctly.
        """
        tokens = []
        current_number = ""

        for i, char in enumerate(expression):
            if char.isdigit() or char == '.':
                current_number += char
            else:
                if current_number:
                    tokens.append(current_number)
                    current_number = ""
                if char in "+-*/()":
                    # Handle unary minus
                    if char == '-' and (i == 0 or expression[i-1] in '+-*/('):
                        current_number += '-'  # Treat as part of the next number
                    else:
                        tokens.append(char)
                # Ignore any other characters (they should've been caught by validation)

        if current_number:
            tokens.append(current_number)

        return tokens

    def _infix_to_postfix(self, tokens: list[str]) -> list[str]:
        """Converts a list of tokens from infix notation to postfix notation."""

        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit():  # Check if it's a (possibly negative, floating-point) number
                output.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses.")  # Extra check
                operator_stack.pop()  # Pop the '('
            elif token in '+-*/':
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)

        while operator_stack:
            if operator_stack[-1] == '(':  # Check for leftover '('
                raise ValueError("Mismatched parentheses.")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list[str]) -> float:
        """Evaluates a list of tokens in postfix notation."""
        stack = []

        for token in tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit(): # Check if it is a number
                stack.append(float(token))
            elif token in '+-*/':
                if len(stack) < 2:
                    raise ValueError("Invalid expression (not enough operands).")
                operand2 = stack.pop()
                operand1 = stack.pop()
                result = self._perform_operation(operand1, operand2, token)
                stack.append(result)

        if len(stack) != 1:
            raise ValueError("Invalid expression (too many operands).")
        return stack[0]


    def _perform_operation(self, operand1: float, operand2: float, operator: str) -> float:
        """Performs the specified arithmetic operation."""
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                raise ValueError("Division by zero.")
            return operand1 / operand2
        else:
            raise ValueError(f"Unknown operator: {operator}")


def main():
    calculator = Calculator()
    while True:
        try:
            expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
