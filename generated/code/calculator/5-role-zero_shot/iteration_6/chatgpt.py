class Calculator:
    """
    A console-based arithmetic calculator that supports addition (+), subtraction (-),
    multiplication (*), and division (/) with proper operator precedence, parentheses,
    and both integer and floating-point numbers (including negatives).

    This implementation follows clean architecture and modular design principles.

    Public Interface:
        calculate(expression: str) -> float

    Exceptions:
        ValueError: Raised for invalid characters in the expression.
        SyntaxError: Raised for syntactical errors such as unbalanced parentheses.
        ZeroDivisionError: Raised when division by zero is attempted.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression string and returns the result as a float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The evaluated result.

        Raises:
            ValueError: If the expression contains invalid characters.
            SyntaxError: If there are any syntax errors such as unbalanced parentheses.
            ZeroDivisionError: If a division by zero is attempted.
        """
        self.tokens = self._tokenize(expression)
        self.position = 0  # Pointer to the current token
        result = self._parse_expression()

        # After complete parsing, ensure no tokens remain unconsumed.
        if self.position != len(self.tokens):
            raise SyntaxError("Unexpected token at the end of the expression.")
        return result

    def _tokenize(self, expression: str):
        """
        Converts the input string into a list of tokens (numbers, operators, parentheses).

        Args:
            expression (str): The raw input expression.

        Returns:
            list: A list of tokens as strings.

        Raises:
            ValueError: If an invalid character is found.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]

            # Skip whitespace
            if char.isspace():
                i += 1
                continue

            # Process a number (integer or float)
            if char.isdigit() or (char == '.' and i + 1 < len(expression) and expression[i + 1].isdigit()):
                num_chars = [char]
                i += 1
                dot_encountered = (char == '.')
                while i < len(expression) and (expression[i].isdigit() or (expression[i] == '.' and not dot_encountered)):
                    if expression[i] == '.':
                        dot_encountered = True
                    num_chars.append(expression[i])
                    i += 1
                token = ''.join(num_chars)
                tokens.append(token)
                continue

            # Process operators and parentheses
            if char in '+-*/()':
                tokens.append(char)
                i += 1
                continue

            # Any other character is invalid
            raise ValueError(f"Invalid character encountered: '{char}'")
        return tokens

    def _current_token(self):
        """
        Returns the current token based on the parsing position.

        Returns:
            str or None: The current token if available; otherwise, None.
        """
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def _consume(self, expected_token=None):
        """
        Consumes the current token and advances the position.

        Args:
            expected_token (str, optional): If specified, ensures the current token matches this.

        Returns:
            str: The consumed token.

        Raises:
            SyntaxError: If the expected token does not match the current token.
        """
        token = self._current_token()
        if expected_token is not None and token != expected_token:
            raise SyntaxError(f"Expected token '{expected_token}' but got '{token}'")
        self.position += 1
        return token

    def _parse_expression(self):
        """
        Parses an expression containing addition and subtraction.

        Returns:
            float: The result of the parsed expression.
        """
        result = self._parse_term()
        while True:
            token = self._current_token()
            if token in ('+', '-'):
                self._consume()  # consume the operator
                next_term = self._parse_term()
                if token == '+':
                    result += next_term
                else:
                    result -= next_term
            else:
                break
        return result

    def _parse_term(self):
        """
        Parses a term containing multiplication and division.

        Returns:
            float: The result of the parsed term.
        """
        result = self._parse_factor()
        while True:
            token = self._current_token()
            if token in ('*', '/'):
                self._consume()  # consume the operator
                next_factor = self._parse_factor()
                if token == '*':
                    result *= next_factor
                else:
                    if next_factor == 0:
                        raise ZeroDivisionError("Division by zero is undefined.")
                    result /= next_factor
            else:
                break
        return result

    def _parse_factor(self):
        """
        Parses a factor, handling unary plus and minus operators.

        Returns:
            float: The evaluated factor.
        """
        token = self._current_token()

        # Handle unary operators
        if token in ('+', '-'):
            self._consume()  # consume the unary operator
            factor = self._parse_factor()
            return factor if token == '+' else -factor

        return self._parse_primary()

    def _parse_primary(self):
        """
        Parses the primary unit: a number or a parenthesized expression.

        Returns:
            float: The evaluated primary expression.

        Raises:
            SyntaxError: If the primary expression is invalid.
        """
        token = self._current_token()
        if token is None:
            raise SyntaxError("Unexpected end of expression.")

        # Parenthesized expression
        if token == '(':
            self._consume('(')
            result = self._parse_expression()
            if self._current_token() != ')':
                raise SyntaxError("Unbalanced parentheses: missing ')'.")
            self._consume(')')
            return result

        # Number token
        try:
            value = float(token)
            self._consume()  # consume the number token
            return value
        except ValueError:
            raise SyntaxError(f"Expected a number but got '{token}'.")


if __name__ == '__main__':
    import sys

    calc = Calculator()

    print("Console-based Arithmetic Calculator")
    print("Enter an arithmetic expression or type 'exit' to quit.")

    while True:
        try:
            expression = input(">> ")
            if expression.lower() in ('exit', 'quit'):
                print("Exiting calculator.")
                sys.exit(0)

            result = calc.calculate(expression)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
