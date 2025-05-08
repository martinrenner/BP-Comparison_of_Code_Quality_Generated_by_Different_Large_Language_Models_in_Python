class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses, respecting operator precedence.
    It accepts both integer and floating-point numbers (including negative values).
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression and returns the calculated result.

        This method validates the input expression (allowed characters and balanced
        parentheses) and then parses and evaluates the expression using a recursive
        descent parser.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression is empty, contains invalid characters,
                        has unbalanced parentheses, or has a syntax error.
            ZeroDivisionError: If a division by zero is encountered.
        """
        if not expression:
            raise ValueError("The expression is empty.")

        # Normalize the expression (remove spaces and validate characters)
        expression = self._normalize_expression(expression)
        if not self._is_balanced(expression):
            raise ValueError("The expression has unbalanced parentheses.")

        # Initialize parser state
        self.expression = expression
        self.pos = 0

        # Parse the expression and compute the result
        result = self._parse_expression()

        # After parsing, ensure no invalid trailing characters remain
        if self.pos < len(self.expression):
            raise ValueError(
                f"Invalid syntax at position {self.pos}: '{self.expression[self.pos:]}'"
            )
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Removes spaces from the expression and verifies that it contains only valid characters.

        Allowed characters are digits, the operators '+', '-', '*', '/', the decimal point '.', 
        and parentheses '(', ')'.

        Args:
            expression (str): The input arithmetic expression.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression becomes empty after normalization or contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().")
        normalized = expression.replace(" ", "")
        if not normalized:
            raise ValueError("The expression is empty after removing spaces.")

        for char in normalized:
            if char not in allowed_chars:
                raise ValueError(f"Invalid character detected: '{char}'")
        return normalized

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks that all parentheses in the expression are correctly paired.

        Args:
            expression (str): The arithmetic expression to check.

        Returns:
            bool: True if the parentheses are balanced, False otherwise.
        """
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        return not stack

    def _peek(self) -> str:
        """
        Returns the current character from the expression without advancing the pointer.

        Returns:
            str: The current character, or an empty string if at the end.
        """
        if self.pos < len(self.expression):
            return self.expression[self.pos]
        return ''

    def _advance(self) -> None:
        """
        Advances the current position pointer by one in the expression.
        """
        self.pos += 1

    def _parse_expression(self) -> float:
        """
        Parses an expression handling addition and subtraction.

        Expression grammar:
            expression = term { ("+" | "-") term }*

        Returns:
            float: The evaluated result of the expression.
        """
        result = self._parse_term()
        while self.pos < len(self.expression) and self._peek() in '+-':
            op = self._peek()
            self._advance()
            right_term = self._parse_term()
            if op == '+':
                result += right_term
            else:
                result -= right_term
        return result

    def _parse_term(self) -> float:
        """
        Parses a term handling multiplication and division.

        Term grammar:
            term = factor { ("*" | "/") factor }*

        Returns:
            float: The evaluated result of the term.
        """
        result = self._parse_factor()
        while self.pos < len(self.expression) and self._peek() in '*/':
            op = self._peek()
            self._advance()
            right_factor = self._parse_factor()
            if op == '*':
                result *= right_factor
            elif op == '/':
                if right_factor == 0:
                    raise ZeroDivisionError("Division by zero.")
                result /= right_factor
        return result

    def _parse_factor(self) -> float:
        """
        Parses a factor which can be a number, a parenthesized expression, or include unary operators.

        Factor grammar:
            factor = { ("+" | "-") } primary
            primary = number | "(" expression ")"

        Returns:
            float: The evaluated result of the factor.
        """
        # Handle unary operators
        sign = 1
        while self.pos < len(self.expression) and self._peek() in '+-':
            if self._peek() == '-':
                sign *= -1
            # For a '+' operator, sign remains unchanged.
            self._advance()

        # Parenthesized expression
        if self._peek() == '(':
            self._advance()  # Consume the '('
            result = self._parse_expression()
            if self._peek() != ')':
                raise ValueError(f"Missing closing parenthesis at position {self.pos}.")
            self._advance()  # Consume the ')'
            return sign * result

        # Parse a number
        return sign * self._parse_number()

    def _parse_number(self) -> float:
        """
        Parses a floating-point number from the current position in the expression.

        Returns:
            float: The parsed number.

        Raises:
            ValueError: If the number format is invalid.
        """
        start_pos = self.pos
        has_decimal_point = False

        while self.pos < len(self.expression) and (self._peek().isdigit() or self._peek() == '.'):
            if self._peek() == '.':
                if has_decimal_point:
                    raise ValueError(
                        f"Invalid number format with multiple decimal points at position {self.pos}."
                    )
                has_decimal_point = True
            self._advance()

        number_str = self.expression[start_pos:self.pos]
        if not number_str or number_str == '.':
            raise ValueError(f"Invalid number format at position {start_pos}.")
        try:
            return float(number_str)
        except ValueError:
            raise ValueError(f"Unable to parse number at position {start_pos}: '{number_str}'")

if __name__ == "__main__":
    calc = Calculator()
    print("Welcome to the Arithmetic Calculator!")
    print("Type 'exit' or 'quit' to close the program.\n")

    while True:
        try:
            user_input = input("Enter an expression: ")
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            result = calc.calculate(user_input)
            print("Result:", result, "\n")
        except Exception as e:
            print("Error:", e, "\n")
