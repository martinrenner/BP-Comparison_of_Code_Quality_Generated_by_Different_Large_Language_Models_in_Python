#!/usr/bin/env python3
"""
Console-Based Arithmetic Calculator

This module implements a console-based arithmetic calculator using object-oriented design.
It evaluates arithmetic expressions containing addition (+), subtraction (-),
multiplication (*), and division (/), with support for parentheses and proper operator precedence.
Both integers and floating-point numbers (including negative values) are supported.

This implementation is designed to meet ISO/IEC 25010 requirements by emphasizing:
    - Functionality: Correctly handles supported arithmetic operations and parenthesized expressions.
    - Performance: Uses an efficient recursive descent parsing algorithm.
    - Modularity: Separates tokenization and parsing into meaningful methods.
    - Security: Validates input for errors (invalid characters, unbalanced parentheses, division by zero).
    - Testability: Encapsulated in a class with clear interfaces.
    - Readability & Documentation: Proper docstrings, clear variable names, and inline comments.
"""

class Calculator:
    """
    A calculator that evaluates arithmetic expressions using recursive descent parsing.
    Supports addition, subtraction, multiplication, division, parentheses, and unary operators.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression string and returns the computed result as a float.

        :param expression: A string containing the arithmetic expression.
        :return: The result of the expression as a float.
        :raises ValueError: If the expression contains invalid characters, unbalanced parentheses, or malformed syntax.
        :raises ZeroDivisionError: If division by zero is encountered.
        """
        # Convert the expression into tokens
        self.tokens = self._tokenize(expression)
        self.current_token_index = 0
        # Parse the expression starting from the highest-level rule
        result = self._parse_expression()
        # Ensure that all tokens have been consumed; otherwise, the expression is invalid.
        if self.current_token_index < len(self.tokens):
            unexpected_token = self.tokens[self.current_token_index]
            raise ValueError(f"Unexpected token '{unexpected_token}' found after complete parsing.")
        return result

    def _tokenize(self, expression: str) -> list:
        """
        Converts the input expression into a list of tokens (numbers and operators).

        :param expression: The arithmetic expression string.
        :return: A list of tokens. Numbers are converted to floats; operators and parentheses remain as strings.
        :raises ValueError: If an invalid character is found in the expression.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isspace():
                i += 1
                continue
            elif char.isdigit() or char == '.':
                # Build a number token (handle integers and floating-point numbers)
                num_str = char
                i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                try:
                    number = float(num_str)
                except ValueError:
                    raise ValueError(f"Invalid number format: {num_str}")
                tokens.append(number)
            elif char in '+-*/()':
                tokens.append(char)
                i += 1
            else:
                raise ValueError(f"Invalid character found in expression: {char}")
        return tokens

    def _parse_expression(self) -> float:
        """
        Parses an expression and handles addition and subtraction.
        Grammar: expression = term { ('+' | '-') term }*

        :return: The evaluated result of the expression.
        """
        value = self._parse_term()
        while (self.current_token_index < len(self.tokens) and 
               self.tokens[self.current_token_index] in ('+', '-')):
            op = self.tokens[self.current_token_index]
            self.current_token_index += 1
            next_value = self._parse_term()
            if op == '+':
                value += next_value
            else:  # op == '-'
                value -= next_value
        return value

    def _parse_term(self) -> float:
        """
        Parses a term and handles multiplication and division.
        Grammar: term = factor { ('*' | '/') factor }*

        :return: The evaluated result of the term.
        :raises ZeroDivisionError: If division by zero is attempted.
        """
        value = self._parse_factor()
        while (self.current_token_index < len(self.tokens) and 
               self.tokens[self.current_token_index] in ('*', '/')):
            op = self.tokens[self.current_token_index]
            self.current_token_index += 1
            next_value = self._parse_factor()
            if op == '*':
                value *= next_value
            elif op == '/':
                if next_value == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                value /= next_value
        return value

    def _parse_factor(self) -> float:
        """
        Parses a factor which can be a number, a parenthesized expression, or a unary operator.
        Grammar: factor = ['+'|'-'] factor | number | '(' expression ')'

        :return: The evaluated result of the factor.
        :raises ValueError: If unexpected tokens or unbalanced parentheses are encountered.
        """
        if self.current_token_index >= len(self.tokens):
            raise ValueError("Unexpected end of expression.")

        token = self.tokens[self.current_token_index]

        # Handle unary operators: plus or minus.
        if token == '+':
            self.current_token_index += 1
            return self._parse_factor()
        elif token == '-':
            self.current_token_index += 1
            return -self._parse_factor()
        elif token == '(':
            self.current_token_index += 1
            value = self._parse_expression()
            # Ensure a corresponding closing parenthesis exists.
            if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index] != ')':
                raise ValueError("Unbalanced parentheses: missing closing ')'")
            self.current_token_index += 1
            return value
        elif isinstance(token, float):
            self.current_token_index += 1
            return token
        else:
            raise ValueError(f"Unexpected token: {token}")

if __name__ == "__main__":
    """
    Provides a simple console-based interface for the Calculator.
    Users can enter arithmetic expressions, and the result will be printed.
    Type 'exit' to quit the program.
    """
    calc = Calculator()
    print("Console-Based Arithmetic Calculator")
    print("Enter an arithmetic expression or type 'exit' to quit.")
    
    while True:
        try:
            user_input = input("Expression> ")
            if user_input.strip().lower() == "exit":
                print("Exiting calculator. Goodbye!")
                break
            result = calc.calculate(user_input)
            print("Result:", result)
        except (ValueError, ZeroDivisionError) as error:
            print("Error:", error)
        except Exception as ex:
            print("An unexpected error occurred:", ex)
