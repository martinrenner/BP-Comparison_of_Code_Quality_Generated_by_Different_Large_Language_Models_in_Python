import re

class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses with correct operator precedence.
    It accepts both integers and floating-point numbers (including negative values).

    Methods:
        calculate(expression: str) -> float:
            Evaluates the given arithmetic expression and returns the result as a float.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression provided as a string and returns the result.

        Args:
            expression (str): The input arithmetic expression.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: For invalid syntax such as unbalanced parentheses or invalid characters.
            ZeroDivisionError: If a division by zero occurs.
        """
        self.tokens = self._tokenize(expression)
        self.current = 0  # Pointer to the current token
        result = self._parse_expression()
        if self.current < len(self.tokens):
            raise ValueError(f"Unexpected token: '{self.tokens[self.current]}'")
        return result

    def _tokenize(self, expression: str) -> list:
        """
        Converts the input expression into a list of tokens.

        Valid tokens include numbers (integer or float), parentheses, and operators.
        It ignores whitespace and raises ValueError on detecting invalid characters.

        Args:
            expression (str): The arithmetic expression.

        Returns:
            list: A list of tokens as strings.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Define the allowed token specification
        token_specification = [
            (r'\s+', None),          # Skip whitespace
            (r'\d+\.\d+|\d+\.\d*|\.\d+|\d+', 'NUMBER'),  # Integer or decimal number
            (r'[+\-*/()]', 'OPERATOR'),   # Arithmetic operators and parentheses
        ]
        tokens = []
        index = 0
        while index < len(expression):
            match = None
            for pattern, token_type in token_specification:
                regex = re.compile(pattern)
                match = regex.match(expression, index)
                if match:
                    text = match.group(0)
                    if token_type == 'NUMBER':
                        tokens.append(text)
                    elif token_type == 'OPERATOR':
                        tokens.append(text)
                    # If token_type is None (whitespace), do nothing.
                    break
            if not match:
                raise ValueError(f"Invalid character at position {index}: '{expression[index]}'")
            index = match.end()
        return tokens

    def _parse_expression(self) -> float:
        """
        Parses an expression which is defined by the grammar:
            Expression -> Term {( '+' | '-' ) Term}*
        
        Returns:
            float: The evaluated value of the expression.
        """
        value = self._parse_term()
        while self.current < len(self.tokens) and self.tokens[self.current] in ('+', '-'):
            operator = self.tokens[self.current]
            self.current += 1
            next_term = self._parse_term()
            if operator == '+':
                value += next_term
            else:
                value -= next_term
        return value

    def _parse_term(self) -> float:
        """
        Parses a term in the expression, handling multiplication and division:
            Term -> Factor {( '*' | '/' ) Factor}*
        
        Returns:
            float: The evaluated value of the term.
        """
        value = self._parse_factor()
        while self.current < len(self.tokens) and self.tokens[self.current] in ('*', '/'):
            operator = self.tokens[self.current]
            self.current += 1
            next_factor = self._parse_factor()
            if operator == '*':
                value *= next_factor
            else:
                if next_factor == 0:
                    raise ZeroDivisionError("Division by zero is undefined.")
                value /= next_factor
        return value

    def _parse_factor(self) -> float:
        """
        Parses a factor which can be a number, a parenthesized expression,
        or a unary plus/minus applied to a factor:
            Factor -> NUMBER | '(' Expression ')' | ('+' | '-') Factor

        Returns:
            float: The evaluated value of the factor.
        """
        if self.current >= len(self.tokens):
            raise ValueError("Unexpected end of expression.")

        token = self.tokens[self.current]

        # Handle unary plus/minus
        if token in ('+', '-'):
            self.current += 1
            factor = self._parse_factor()
            return factor if token == '+' else -factor

        # Handle parenthesized expressions
        if token == '(':
            self.current += 1
            value = self._parse_expression()
            if self.current >= len(self.tokens) or self.tokens[self.current] != ')':
                raise ValueError("Unbalanced parentheses: Missing closing ')'.")
            self.current += 1
            return value

        # The token should be a number at this point
        try:
            value = float(token)
        except ValueError:
            raise ValueError(f"Invalid number token: {token}") from None
        self.current += 1
        return value


def main():
    """
    Main loop for the console-based arithmetic calculator.
    It continuously prompts the user for an arithmetic expression,
    evaluates it using the Calculator class, and prints the result.
    The loop exits when the user enters an empty line.
    """
    calc = Calculator()
    print("Console-based Arithmetic Calculator")
    print("Enter an arithmetic expression or press Enter to exit.")
    while True:
        try:
            expression = input("> ").strip()
            if expression == "":
                print("Exiting Calculator. Goodbye!")
                break
            result = calc.calculate(expression)
            print(f"= {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
