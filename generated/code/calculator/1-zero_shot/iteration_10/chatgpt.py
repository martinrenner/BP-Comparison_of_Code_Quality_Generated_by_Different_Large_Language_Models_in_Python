import re
from collections import deque
from typing import List, Union

Number = Union[float, int]


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses. It correctly handles operator precedence,
    negative numbers, and both integer and floating-point arithmetic.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return the computed result as a float.

        :param expression: A string containing the arithmetic expression.
        :return: The result of evaluating the expression as a float.
        :raises ValueError: If the expression is invalid (e.g., unbalanced parentheses or invalid characters).
        :raises ZeroDivisionError: If the expression attempts division by zero.
        """
        tokens = self._tokenize(expression)
        postfix = self._to_postfix(tokens)
        result = self._evaluate_postfix(postfix)
        return result

    def _tokenize(self, expression: str) -> List[str]:
        """
        Convert the input expression string into a list of tokens.
        Tokens can be numbers (as strings), operators, or parentheses.
        
        Supports negative numbers by checking for unary '-' or '+' signs.
        
        :param expression: The arithmetic expression as a string.
        :return: A list of tokens.
        :raises ValueError: If the expression contains invalid characters.
        """
        tokens = []
        i = 0
        n = len(expression)

        while i < n:
            char = expression[i]

            # Skip whitespace
            if char.isspace():
                i += 1
                continue

            # Check if starting a number: can start with a digit or a dot.
            if char.isdigit() or char == '.':
                number_token, i = self._read_number(expression, i)
                tokens.append(number_token)
                continue

            # If the character is '+' or '-' it can either be a binary operator or a unary sign.
            if char in '+-':
                # Determine if it is a unary operator:
                # It is unary if it is at the start, or if the previous token is an operator or '('.
                if (len(tokens) == 0 or tokens[-1] in '+-*/(') and (i + 1 < n and (expression[i + 1].isdigit() or expression[i + 1] == '.')):
                    # Parse as part of a numeric token, e.g. -3.5 or +2
                    number_token, i = self._read_number(expression, i)
                    tokens.append(number_token)
                    continue
                else:
                    # Otherwise, it's a binary operator.
                    tokens.append(char)
                    i += 1
                    continue

            # Operators '*' and '/'
            if char in '*/':
                tokens.append(char)
                i += 1
                continue

            # Parentheses
            if char in '()':
                tokens.append(char)
                i += 1
                continue

            # If the character doesn't match a valid token, raise an error.
            raise ValueError(f"Invalid character '{char}' in expression.")

        return tokens

    def _read_number(self, expression: str, index: int) -> (str, int):
        """
        Read a numeric token (which can be an integer or float, and may include a leading + or -)
        starting from the given index in the expression.
        
        :param expression: The full arithmetic expression string.
        :param index: The current index to start reading the number.
        :return: A tuple (number_token, new_index) where number_token is the extracted numeric string
                 and new_index is the updated position in the string.
        :raises ValueError: If the number format is invalid.
        """
        num_str = ''
        n = len(expression)

        # If there is a leading sign, include it.
        if index < n and expression[index] in '+-':
            num_str += expression[index]
            index += 1

        dot_encountered = False
        digit_found = False

        while index < n:
            ch = expression[index]
            if ch.isdigit():
                digit_found = True
                num_str += ch
                index += 1
            elif ch == '.':
                if dot_encountered:
                    raise ValueError("Invalid number format: multiple decimal points.")
                dot_encountered = True
                num_str += ch
                index += 1
            else:
                break

        if not digit_found:
            raise ValueError("Invalid number format: no digits found.")
        return num_str, index

    def _to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Convert the list of tokens (in infix order) to a postfix (Reverse Polish Notation) list
        using the Shunting Yard algorithm.
        
        :param tokens: The tokenized arithmetic expression.
        :return: A list of tokens in postfix order.
        :raises ValueError: If there are unbalanced parentheses.
        """
        # Define operator precedence.
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        operator_stack = deque()

        for token in tokens:
            if self._is_number(token):
                output_queue.append(token)
            elif token in precedence:
                # Pop operators from the stack with higher or equal precedence.
                while operator_stack:
                    top = operator_stack[-1]
                    if top in precedence and precedence[top] >= precedence[token]:
                        output_queue.append(operator_stack.pop())
                    else:
                        break
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                # Pop until '(' is encountered.
                found_left_paren = False
                while operator_stack:
                    top = operator_stack.pop()
                    if top == '(':
                        found_left_paren = True
                        break
                    output_queue.append(top)
                if not found_left_paren:
                    raise ValueError("Unbalanced parentheses: missing '('.")
            else:
                raise ValueError(f"Unknown token '{token}' encountered.")

        # After processing all tokens, pop any remaining operators.
        while operator_stack:
            top = operator_stack.pop()
            if top in '()':
                raise ValueError("Unbalanced parentheses in the expression.")
            output_queue.append(top)
        return output_queue

    def _evaluate_postfix(self, tokens: List[str]) -> float:
        """
        Evaluate a postfix (Reverse Polish Notation) expression and return the result.
        
        :param tokens: The list of tokens in postfix order.
        :return: The result as a float.
        :raises ZeroDivisionError: If a division by zero occurs.
        :raises ValueError: If the postfix expression is malformed.
        """
        stack = []

        for token in tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in '+-*/':
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient values for the operation.")
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
                        raise ZeroDivisionError("Division by zero encountered.")
                    result = a / b
                stack.append(result)
            else:
                raise ValueError(f"Unknown token '{token}' encountered during evaluation.")

        if len(stack) != 1:
            raise ValueError("Malformed expression: too many values remain.")

        return stack[0]

    def _is_number(self, token: str) -> bool:
        """
        Check if the token represents a numeric value.
        
        :param token: The token to check.
        :return: True if token represents a number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False


def main():
    """
    Entry point for the console-based calculator.
    Continuously prompts the user for input and outputs the evaluation result.
    Type 'exit' to quit the application.
    """
    calc = Calculator()
    print("Console-based Arithmetic Calculator")
    print("Enter an expression to evaluate or type 'exit' to quit.")
    
    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() in {'exit', 'quit'}:
                print("Exiting the calculator. Goodbye!")
                break
            result = calc.calculate(user_input)
            print("Result:", result)
        except Exception as e:
            # Catch any error (e.g., ValueError, ZeroDivisionError) and display an error message.
            print("Error:", e)


if __name__ == "__main__":
    main()
