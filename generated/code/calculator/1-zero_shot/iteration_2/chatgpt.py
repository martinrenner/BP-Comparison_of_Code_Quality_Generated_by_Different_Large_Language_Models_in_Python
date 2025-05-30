class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, parentheses for grouping, and both integer and
    floating-point numbers (including negative values). This implementation uses
    a recursive descent parser to ensure correct operator precedence.

    Methods:
        calculate(expression: str) -> float:
            Evaluates the provided arithmetic expression and returns the result.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluate the arithmetic expression provided as a string.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The evaluation result.

        Raises:
            ValueError: If the expression contains invalid characters or an
                        invalid number format.
            SyntaxError: If the expression has unbalanced parentheses or
                         invalid syntax.
            ZeroDivisionError: If division by zero occurs.
        """
        self.tokens = self._tokenize(expression)
        self.index = 0
        result = self._parse_expression()
        if self.index != len(self.tokens):
            raise SyntaxError("Invalid syntax: unexpected tokens remain")
        return result

    def _tokenize(self, expression: str):
        """
        Convert the input expression into a list of tokens (numbers and operators).

        Supports:
            - Numbers: integer and floating-point values.
            - Operators: +, -, *, /
            - Parentheses: ( and )

        Args:
            expression (str): The arithmetic expression.

        Returns:
            list: A list of tokens (either floats/ints or operator strings).

        Raises:
            ValueError: If the input contains invalid characters or number format.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]

            # Skip whitespace
            if char.isspace():
                i += 1
                continue

            # Operators and parentheses
            if char in '+-*/()':
                tokens.append(char)
                i += 1
            # Numbers (including integers and decimals)
            elif char.isdigit() or char == '.':
                num_str = ''
                dot_count = 0
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid number format: multiple decimals in a number.")
                    num_str += expression[i]
                    i += 1
                try:
                    # Convert token to int if it doesn't contain a dot, else float.
                    token_number = float(num_str) if '.' in num_str else int(num_str)
                except ValueError:
                    raise ValueError(f"Invalid numeric value: {num_str}")
                tokens.append(token_number)
            else:
                raise ValueError(f"Invalid character encountered: {char}")

        return tokens

    def _parse_expression(self):
        """
        Parse and evaluate an expression.

        Grammar:
            expression = term { ("+" | "-") term }*

        Returns:
            float: The evaluated result of the expression.
        """
        result = self._parse_term()
        while self.index < len(self.tokens) and self.tokens[self.index] in ('+', '-'):
            op = self.tokens[self.index]
            self.index += 1  # consume the operator
            next_term = self._parse_term()
            if op == '+':
                result += next_term
            else:
                result -= next_term
        return result

    def _parse_term(self):
        """
        Parse and evaluate a term.

        Grammar:
            term = factor { ("*" | "/") factor }*

        Returns:
            float: The evaluated result of the term.
        """
        result = self._parse_factor()
        while self.index < len(self.tokens) and self.tokens[self.index] in ('*', '/'):
            op = self.tokens[self.index]
            self.index += 1  # consume the operator
            next_factor = self._parse_factor()
            if op == '*':
                result *= next_factor
            else:
                if next_factor == 0:
                    raise ZeroDivisionError("Division by zero encountered.")
                result /= next_factor
        return result

    def _parse_factor(self):
        """
        Parse and evaluate a factor.

        Grammar:
            factor = [ ("+" | "-") ] primary
            primary = NUMBER | "(" expression ")"

        Returns:
            float: The evaluated result of the factor.

        Raises:
            SyntaxError: If the expression syntax is invalid.
        """
        if self.index >= len(self.tokens):
            raise SyntaxError("Unexpected end of expression.")

        token = self.tokens[self.index]

        # Handle unary plus and minus
        if token == '+':
            self.index += 1
            return self._parse_factor()
        elif token == '-':
            self.index += 1
            return -self._parse_factor()

        # Handle parentheses - evaluate the expression inside them
        if token == '(':
            self.index += 1  # consume '('
            result = self._parse_expression()
            if self.index >= len(self.tokens) or self.tokens[self.index] != ')':
                raise SyntaxError("Unbalanced parentheses: missing ')'.")
            self.index += 1  # consume ')'
            return result

        # The token should be a number at this point
        if isinstance(token, (int, float)):
            self.index += 1
            return token

        raise SyntaxError(f"Unexpected token: {token}")


if __name__ == "__main__":
    calc = Calculator()
    print("Console-based Arithmetic Calculator")
    print("Enter an arithmetic expression to evaluate or type 'exit' to quit.")
    while True:
        try:
            user_input = input(">> ")
            if user_input.strip().lower() in {"exit", "quit"}:
                break
            result = calc.calculate(user_input)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
