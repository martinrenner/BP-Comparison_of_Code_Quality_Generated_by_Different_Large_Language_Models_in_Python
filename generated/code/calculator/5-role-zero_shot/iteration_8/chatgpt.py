class Calculator:
    """
    A console-based arithmetic calculator that evaluates arithmetic expressions containing
    addition (+), subtraction (-), multiplication (*), division (/), and parentheses.
    
    This implementation follows best practices for modular design, error handling, and clean code.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluate the arithmetic expression provided as a string.

        Supported operations:
            - Addition (+)
            - Subtraction (-)
            - Multiplication (*)
            - Division (/)
            - Parentheses for grouping

        Both integers and floating-point numbers (including negative values) are supported.
        Operator precedence is correctly handled.

        :param expression: The arithmetic expression as a string.
                           Example: "(1 + 2) * 3 - 4 / 5"
        :return: The result of the evaluation as a float.
        :raises ValueError: If the expression is empty, contains invalid characters,
                            has mismatched parentheses, or has invalid syntax.
        :raises ZeroDivisionError: If a division by zero is encountered during evaluation.
        """
        tokens = self._tokenize(expression)
        self.tokens = tokens  # List of tokens (numbers and operators)
        self.index = 0        # Current index pointer in the token list

        if not tokens:
            raise ValueError("Empty expression provided.")

        result = self._parse_expression()

        # After parsing, ensure there are no unexpected tokens left.
        if self.index != len(self.tokens):
            raise ValueError(
                f"Invalid syntax: Unexpected token '{self.tokens[self.index]}' at position {self.index}."
            )
        return result

    def _tokenize(self, expression: str) -> list:
        """
        Convert the expression string into a list of tokens.
        
        Valid tokens are:
            - Numbers (as float values)
            - Operators: '+', '-', '*', '/'
            - Parentheses: '(' and ')'

        Any invalid character will result in a ValueError.

        :param expression: The arithmetic expression as a string.
        :return: A list of tokens.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isspace():
                i += 1
                continue
            elif char in '+-*/()':
                tokens.append(char)
                i += 1
            elif char.isdigit() or char == '.':
                num_str = ''
                dot_count = 0
                # Accumulate digits and at most one decimal point.
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid numeric format: multiple decimals in number.")
                    num_str += expression[i]
                    i += 1
                try:
                    num_value = float(num_str)
                except ValueError:
                    raise ValueError(f"Invalid numeric format: '{num_str}'.")
                tokens.append(num_value)
            else:
                raise ValueError(f"Invalid character encountered: '{char}'.")
        return tokens

    def _parse_expression(self) -> float:
        """
        Parse and compute an expression that may include addition and subtraction.
        
        Grammar:
            expression = term { ("+" | "-") term }

        :return: The computed value as a float.
        """
        value = self._parse_term()
        while self.index < len(self.tokens) and self.tokens[self.index] in ('+', '-'):
            op = self.tokens[self.index]
            self.index += 1
            next_term = self._parse_term()
            if op == '+':
                value += next_term
            elif op == '-':
                value -= next_term
        return value

    def _parse_term(self) -> float:
        """
        Parse and compute a term that may include multiplication and division.
        
        Grammar:
            term = factor { ("*" | "/") factor }

        :return: The computed term value as a float.
        """
        value = self._parse_factor()
        while self.index < len(self.tokens) and self.tokens[self.index] in ('*', '/'):
            op = self.tokens[self.index]
            self.index += 1
            next_factor = self._parse_factor()
            if op == '*':
                value *= next_factor
            elif op == '/':
                if next_factor == 0:
                    raise ZeroDivisionError("Division by zero.")
                value /= next_factor
        return value

    def _parse_factor(self) -> float:
        """
        Parse and compute a factor which can be:
            - A numeric literal (integer or float)
            - A parenthesized subexpression
            - A unary operation (plus or minus)

        Grammar:
            factor = ["+" | "-"] ( number | "(" expression ")" )

        :return: The computed factor value as a float.
        :raises ValueError: If the syntax is invalid or if parentheses are mismatched.
        """
        if self.index >= len(self.tokens):
            raise ValueError("Invalid syntax: Unexpected end of expression.")

        token = self.tokens[self.index]

        # Handle unary operators.
        if token in ('+', '-'):
            self.index += 1
            factor = self._parse_factor()
            return factor if token == '+' else -factor

        # Handle parenthesized expression.
        if token == '(':
            self.index += 1  # Consume the '('
            value = self._parse_expression()
            if self.index >= len(self.tokens) or self.tokens[self.index] != ')':
                raise ValueError("Mismatched parentheses.")
            self.index += 1  # Consume the ')'
            return value

        # The token should be a number at this point.
        if isinstance(token, (int, float)):
            self.index += 1
            return float(token)

        # Fallback for any unexpected token (should normally never hit this case).
        raise ValueError(f"Unexpected token: {token}")


if __name__ == "__main__":
    """
    Entry point for the console-based arithmetic calculator.
    
    The calculator repeatedly prompts the user for an arithmetic expression,
    evaluates it, and prints the result. The program exits when the user types 'exit'
    or 'quit'.
    """
    calculator = Calculator()
    print("Arithmetic Calculator")
    print("Type 'exit' or 'quit' to end the program.")
    
    while True:
        try:
            expression = input("Enter expression: ")
            if expression.strip().lower() in {"exit", "quit"}:
                print("Exiting the calculator. Goodbye!")
                break
            result = calculator.calculate(expression)
            print("Result:", result)
        except Exception as error:
            print("Error:", error)
