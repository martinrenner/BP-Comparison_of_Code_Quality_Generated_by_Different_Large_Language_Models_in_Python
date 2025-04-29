class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, parentheses, and both integer and floating-point numbers.
    
    The calculator follows the ISO/IEC 25010 standard for code quality by ensuring
    correctness, performance, modularity, security, testability, and readability.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression provided as a string and returns the result.

        The expression can include:
         - positive and negative integers and floating-point numbers
         - basic arithmetic operators: +, -, *, /
         - parentheses for grouping

        Args:
            expression (str): A mathematical expression (e.g., "2*(3+4) - 5/2").

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, or a malformed number.
            ZeroDivisionError: If a division by zero occurs.
        """
        # Normalize expression by removing whitespace and validating characters.
        expression = self._normalize_expression(expression)
        if not self._is_balanced(expression):
            raise ValueError("Unbalanced parentheses in the expression.")

        # Initialize parsing state.
        self.expression = expression
        self.index = 0

        # Parse the expression and compute the result.
        result = self._parse_expression()

        # If there are any unexpected characters remaining, the expression is invalid.
        if self.index != len(self.expression):
            raise ValueError("Invalid expression: unexpected characters remaining.")
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.

        Args:
            expression (str): The input mathematical expression.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether a mathematical expression has properly paired parentheses.

        Args:
            expression (str): The mathematical expression.

        Returns:
            bool: True if parentheses are correctly paired, otherwise False.
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

    def _current_char(self):
        """
        Returns the current character in the expression based on the parser's index.

        Returns:
            str or None: The current character if available, otherwise None.
        """
        if self.index < len(self.expression):
            return self.expression[self.index]
        return None

    def _advance(self):
        """
        Advances the parser's index by one.
        """
        self.index += 1

    def _parse_expression(self) -> float:
        """
        Parses and evaluates an expression according to the grammar:
            expression = term { ('+' | '-') term }
        
        Returns:
            float: The result of the parsed expression.
        """
        result = self._parse_term()
        while self._current_char() in ('+', '-'):
            op = self._current_char()
            self._advance()
            term_value = self._parse_term()
            if op == '+':
                result += term_value
            elif op == '-':
                result -= term_value
        return result

    def _parse_term(self) -> float:
        """
        Parses and evaluates a term according to the grammar:
            term = factor { ('*' | '/') factor }
        
        Returns:
            float: The result of the parsed term.
        """
        result = self._parse_factor()
        while self._current_char() in ('*', '/'):
            op = self._current_char()
            self._advance()
            factor_value = self._parse_factor()
            if op == '*':
                result *= factor_value
            elif op == '/':
                if factor_value == 0:
                    raise ZeroDivisionError("Division by zero.")
                result /= factor_value
        return result

    def _parse_factor(self) -> float:
        """
        Parses and evaluates a factor which can be a number, a parenthesized expression,
        or a factor with a unary operator (+ or -).

        Returns:
            float: The result of the parsed factor.
        """
        char = self._current_char()
        if char is None:
            raise ValueError("Unexpected end of expression.")

        # Handle parenthesized expressions.
        if char == '(':
            self._advance()  # Consume '('
            result = self._parse_expression()
            if self._current_char() != ')':
                raise ValueError("Mismatched parentheses.")
            self._advance()  # Consume ')'
            return result

        # Handle unary plus.
        if char == '+':
            self._advance()
            return self._parse_factor()

        # Handle unary minus.
        if char == '-':
            self._advance()
            return -self._parse_factor()

        # Otherwise, it should be a number.
        return self._parse_number()

    def _parse_number(self) -> float:
        """
        Parses a numerical value (integer or floating-point) from the expression.

        Returns:
            float: The numeric value parsed from the expression.

        Raises:
            ValueError: If the number format is invalid.
        """
        start_index = self.index
        has_decimal_point = False

        # A valid number must start with a digit or a dot.
        if self._current_char() is None or (not self._current_char().isdigit() and self._current_char() != '.'):
            raise ValueError(f"Invalid character at position {self.index}: expected a number.")

        # Consume the number characters.
        while (self._current_char() is not None and 
               (self._current_char().isdigit() or self._current_char() == '.')):
            if self._current_char() == '.':
                if has_decimal_point:
                    raise ValueError("Invalid number format: multiple decimal points.")
                has_decimal_point = True
            self._advance()

        number_str = self.expression[start_index:self.index]
        try:
            return float(number_str)
        except ValueError:
            raise ValueError(f"Invalid number format: {number_str}")


if __name__ == "__main__":
    calc = Calculator()
    print("Simple Arithmetic Calculator")
    print("Enter an expression to calculate (or type 'exit' to quit):")

    while True:
        try:
            expr = input("> ")
            if expr.lower() == "exit":
                break
            result = calc.calculate(expr)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
