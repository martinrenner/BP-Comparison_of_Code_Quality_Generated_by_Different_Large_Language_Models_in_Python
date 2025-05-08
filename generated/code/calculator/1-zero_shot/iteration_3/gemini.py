import re


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It handles operator precedence
    and both integer and floating-point numbers.  The implementation adheres to
    ISO/IEC 25010 quality characteristics.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
            TypeError: If the input expression is not a string
        """

        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        try:
            tokens = self._tokenize(expression)
            parsed_expression = self._parse(tokens)
            result = self._evaluate(parsed_expression)
            return result
        except ZeroDivisionError:
            raise ValueError("Division by zero encountered.")
        except Exception as e:  # Catch broader exceptions for robustness
            raise ValueError(f"Invalid expression: {e}")


    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the input expression.

        Args:
            expression: The arithmetic expression string.

        Returns:
            A list of tokens (numbers, operators, parentheses).

        Raises:
            ValueError: if an invalid character is in the expression.
        """
        # Remove all whitespace to handle inputs like "1 + 2"
        expression = expression.replace(" ", "")

        # Use regular expression for tokenization process to increase performance
        token_specification = [
            ('NUMBER',   r'-?\d+(\.\d*)?'),  # Integer or decimal number (including negative values)
            ('OPERATOR', r'[+\-*/]'),      # Arithmetic operators
            ('LPAREN',   r'\('),             # Left parenthesis
            ('RPAREN',   r'\)'),             # Right parenthesis
        ]
        # Creates the regex to match everything, and groups everything using the specification name
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        tokens = []
        for match in re.finditer(tok_regex, expression):
            kind = match.lastgroup
            value = match.group()
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'OPERATOR':
                pass  # Operators, no conversion needed
            elif kind == 'LPAREN' or kind == 'RPAREN':
                pass    # Parentheses
            tokens.append((kind, value))

        # Check for invalid input characters, helps ensure the input is well-formed
        valid_chars = r'^[\d+\-*/().\s]+$'  # Added \s to allow whitespace
        if not re.match(valid_chars, expression):
          invalid_chars = re.sub(valid_chars, '', expression)
          raise ValueError(f"Invalid character(s) found in expression: {invalid_chars}")

        return tokens

    def _parse(self, tokens: list) -> list:
        """
        Parses the token list into a Reverse Polish Notation (RPN) list using
        the Shunting Yard algorithm.  This handles operator precedence and
        parentheses.

        Args:
            tokens: A list of tokens from the _tokenize method.

        Returns:
            A list representing the expression in RPN.

        Raises:
            ValueError: If parentheses are unbalanced.
        """
        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for kind, value in tokens:
            if kind == 'NUMBER':
                output_queue.append(value)
            elif kind == 'OPERATOR':
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(value, -1)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(value)
            elif kind == 'LPAREN':
                operator_stack.append(value)
            elif kind == 'RPAREN':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Unbalanced parentheses: Mismatched ')'")
                if operator_stack[-1] == '(':
                    operator_stack.pop()  #Discard the '('

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Unbalanced parentheses: Mismatched '('")
            output_queue.append(operator_stack.pop())

        return output_queue

    def _evaluate(self, rpn_expression: list) -> float:
        """
        Evaluates the Reverse Polish Notation (RPN) expression.

        Args:
            rpn_expression: A list representing the expression in RPN.

        Returns:
            The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid.
        """
        stack = []
        for token in rpn_expression:
            if isinstance(token, (int, float)):
                stack.append(token)
            else:  # It's an operator
                if len(stack) < 2:
                    raise ValueError("Invalid expression: Insufficient operands")
                operand2 = stack.pop()
                operand1 = stack.pop()
                if token == '+':
                    stack.append(operand1 + operand2)
                elif token == '-':
                    stack.append(operand1 - operand2)
                elif token == '*':
                    stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError  # Explicitly raise for clarity
                    stack.append(operand1 / operand2)
        if len(stack) != 1:
            raise ValueError("Invalid expression: Too many operands")

        return stack[0]


def main():
    """
    Main function to run the calculator in console.
    """
    calculator = Calculator()

    while True:
        expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
        if expression.lower() == 'quit':
            break

        try:
            result = calculator.calculate(expression)
            print("Result:", result)
        except ValueError as e:
            print("Error:", e)
        except TypeError as e:
            print("Error", e)


if __name__ == "__main__":
    main()
