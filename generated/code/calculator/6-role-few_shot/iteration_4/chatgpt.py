class Calculator:
    """
    A simple arithmetic calculator that supports addition, subtraction,
    multiplication, and division with operator precedence, parentheses,
    and both integer and floating-point numbers.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the computed result.

        Args:
            expression (str): A mathematical expression (e.g., "3 + 4 * (2 - 1)").

        Returns:
            float: The evaluation result.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, invalid syntax, or division by zero.
        """
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("Unbalanced parentheses in the expression.")

        self.expression = normalized_expr  # The expression to parse (without whitespace)
        self.index = 0  # Pointer to the current position in the expression

        result = self._parse_expression()

        # Ensure the entire expression has been consumed; otherwise, it's invalid.
        if self.index != len(self.expression):
            raise ValueError(f"Invalid syntax: unexpected character at position {self.index}")

        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating allowed characters.

        Args:
            expression (str): The raw input expression.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains characters other than digits,
                        decimal points, operators (+, -, *, /), or parentheses.
        """
        allowed_chars = set("0123456789+-*/(). ")
        for char in expression:
            if char not in allowed_chars:
                raise ValueError(f"Expression contains invalid character: '{char}'")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether the parentheses in the expression are properly balanced.

        Args:
            expression (str): The mathematical expression.

        Returns:
            bool: True if parentheses are correctly paired; False otherwise.
        """
        stack = []
        for char in expression:
            if char == "(":
                stack.append(char)
            elif char == ")":
                if not stack:
                    return False
                stack.pop()
        return not stack

    def _parse_expression(self) -> float:
        """
        Parses an expression handling addition and subtraction operators.

        Returns:
            float: The computed value of the expression.
        """
        value = self._parse_term()
        while self.index < len(self.expression) and self.expression[self.index] in "+-":
            op = self.expression[self.index]
            self.index += 1  # consume the operator
            next_term = self._parse_term()
            if op == "+":
                value += next_term
            elif op == "-":
                value -= next_term
        return value

    def _parse_term(self) -> float:
        """
        Parses a term handling multiplication and division operators.

        Returns:
            float: The computed term value.
        """
        value = self._parse_factor()
        while self.index < len(self.expression) and self.expression[self.index] in "*/":
            op = self.expression[self.index]
            self.index += 1  # consume the operator
            next_factor = self._parse_factor()
            if op == "*":
                value *= next_factor
            elif op == "/":
                if next_factor == 0:
                    raise ValueError("Division by zero.")
                value /= next_factor
        return value

    def _parse_factor(self) -> float:
        """
        Parses a factor which could be a number, a parenthesized expression, or include a unary operator.

        Returns:
            float: The computed factor value.

        Raises:
            ValueError: If a number or a matching parenthesis is not found.
        """
        # Handle optional unary plus or minus
        if self.index < len(self.expression) and self.expression[self.index] in "+-":
            op = self.expression[self.index]
            self.index += 1
            factor = self._parse_factor()
            return factor if op == '+' else -factor

        # Parenthesized expression
        if self.index < len(self.expression) and self.expression[self.index] == "(":
            self.index += 1  # consume '('
            value = self._parse_expression()
            if self.index >= len(self.expression) or self.expression[self.index] != ")":
                raise ValueError("Mismatched parentheses.")
            self.index += 1  # consume ')'
            return value

        return self._parse_number()

    def _parse_number(self) -> float:
        """
        Parses a numeric value (integer or float) from the expression.

        Returns:
            float: The numeric value.

        Raises:
            ValueError: If a proper number cannot be parsed.
        """
        start_index = self.index
        dot_seen = False

        while self.index < len(self.expression) and (
            self.expression[self.index].isdigit() or self.expression[self.index] == '.'
        ):
            if self.expression[self.index] == '.':
                if dot_seen:
                    raise ValueError("Invalid number: multiple decimal points.")
                dot_seen = True
            self.index += 1

        if start_index == self.index:
            raise ValueError(f"Invalid syntax: expected number at position {self.index}")

        num_str = self.expression[start_index:self.index]
        try:
            return float(num_str)
        except Exception as e:
            raise ValueError(f"Invalid number format: {num_str}") from e


def main():
    """
    Runs the console-based arithmetic calculator.
    The user can input an expression to evaluate or type 'exit' to quit.
    """
    calc = Calculator()
    print("Console-based Arithmetic Calculator")
    print("Enter a mathematical expression to evaluate or type 'exit' to quit.")
    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() in {"exit", "quit"}:
                print("Exiting calculator.")
                break
            result = calc.calculate(user_input)
            print(f"Result: {result}")
        except ValueError as ve:
            print("Error:", ve)
        except Exception as e:
            print("An unexpected error occurred:", e)


if __name__ == "__main__":
    main()
