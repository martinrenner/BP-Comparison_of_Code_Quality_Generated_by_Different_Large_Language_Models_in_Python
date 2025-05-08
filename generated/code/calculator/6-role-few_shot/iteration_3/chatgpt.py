class Calculator:
    """
    A console-based arithmetic calculator that supports addition (+), subtraction (-),
    multiplication (*), division (/), parentheses, and both integer and floating-point
    numbers (including negative values). The calculator ensures correct operator precedence
    and proper input validation.

    Methods:
        calculate(expression: str) -> float:
            Evaluates the arithmetic expression and returns the computed result.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression provided as a string.

        Args:
            expression (str): The arithmetic expression to be evaluated.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression is empty, contains invalid characters,
                        has unbalanced parentheses, or is otherwise malformed.
            ZeroDivisionError: If a division by zero occurs during evaluation.
        """
        normalized_expr = self._normalize_expression(expression)
        if not normalized_expr:
            raise ValueError("Empty expression is not allowed.")
        if not self._is_balanced(normalized_expr):
            raise ValueError("Invalid expression: unbalanced parentheses detected.")

        # Initialize parser state.
        self.expression = normalized_expr
        self.pos = 0

        result = self._parse_expression()

        # After parsing, the entire input string should be consumed.
        if self.pos != len(self.expression):
            raise ValueError("Invalid expression: unexpected characters remain.")

        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression by removing whitespace and validating allowed characters.

        Args:
            expression (str): The arithmetic expression.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains any invalid characters.
        """
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether the parentheses in the expression are balanced.

        Args:
            expression (str): The arithmetic expression.

        Returns:
            bool: True if the parentheses are balanced, otherwise False.
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

    def _parse_expression(self) -> float:
        """
        Parses the expression following the grammar:
            Expression = Term { ("+"|"-") Term }*

        Returns:
            float: The computed value of the expression.
        """
        value = self._parse_term()
        while self.pos < len(self.expression) and self.expression[self.pos] in ('+', '-'):
            op = self.expression[self.pos]
            self.pos += 1  # Consume the operator
            next_term = self._parse_term()
            if op == '+':
                value += next_term
            else:  # op == '-'
                value -= next_term
        return value

    def _parse_term(self) -> float:
        """
        Parses a term following the grammar:
            Term = Factor { ("*"|"/") Factor }*

        Returns:
            float: The computed value of the term.
        """
        value = self._parse_factor()
        while self.pos < len(self.expression) and self.expression[self.pos] in ('*', '/'):
            op = self.expression[self.pos]
            self.pos += 1  # Consume the operator
            next_factor = self._parse_factor()
            if op == '*':
                value *= next_factor
            else:  # op == '/'
                if next_factor == 0:
                    raise ZeroDivisionError("Division by zero encountered.")
                value /= next_factor
        return value

    def _parse_factor(self) -> float:
        """
        Parses a factor using the grammar:
            Factor = Number | "(" Expression ")" | ("+"|"-") Factor

        Returns:
            float: The computed value of the factor.
        """
        # Handle unary operators.
        if self.pos < len(self.expression) and self.expression[self.pos] in ('+', '-'):
            op = self.expression[self.pos]
            self.pos += 1
            factor = self._parse_factor()
            return -factor if op == '-' else factor

        # Handle parentheses.
        if self.pos < len(self.expression) and self.expression[self.pos] == '(':
            self.pos += 1  # Consume '('
            value = self._parse_expression()
            if self.pos >= len(self.expression) or self.expression[self.pos] != ')':
                raise ValueError("Unbalanced parentheses detected.")
            self.pos += 1  # Consume ')'
            return value

        # Parse a number.
        return self._parse_number()

    def _parse_number(self) -> float:
        """
        Parses a number (integer or floating-point) starting from the current position.

        Returns:
            float: The parsed number.

        Raises:
            ValueError: If no valid number can be parsed or if multiple decimal points are found.
        """
        start_pos = self.pos
        dot_count = 0

        while self.pos < len(self.expression) and (self.expression[self.pos].isdigit() or self.expression[self.pos] == '.'):
            if self.expression[self.pos] == '.':
                if dot_count >= 1:
                    raise ValueError("Invalid number format: multiple decimal points detected.")
                dot_count += 1
            self.pos += 1

        if start_pos == self.pos:
            raise ValueError("Invalid number format.")

        num_str = self.expression[start_pos:self.pos]
        try:
            return float(num_str)
        except Exception as e:
            raise ValueError(f"Invalid number format: {num_str}") from e


if __name__ == "__main__":
    # Console-based interface for the arithmetic calculator.
    calc = Calculator()

    print("Console-based Arithmetic Calculator")
    print("Enter an arithmetic expression or type 'exit' to quit.")

    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() in ('exit', 'quit'):
                break

            result = calc.calculate(user_input)
            print("Result:", result)
        except Exception as error:
            print("Error:", error)
