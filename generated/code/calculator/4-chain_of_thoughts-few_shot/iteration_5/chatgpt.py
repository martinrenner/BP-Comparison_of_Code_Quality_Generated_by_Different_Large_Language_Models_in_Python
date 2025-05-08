class Calculator:
    """
    A console-based arithmetic calculator that supports addition (+),
    subtraction (-), multiplication (*), division (/), parentheses for
    grouping, and respects the correct order of operations. Input numbers
    can be integers or decimals (including negative numbers).
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result as a float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The computed result of the expression.

        Raises:
            ValueError: If the expression has invalid characters,
                        unbalanced parentheses, division by zero,
                        or a syntax error.
        """
        # Normalize the expression (remove whitespace and validate characters)
        expression = self._normalize_expression(expression)
        # Check that the parentheses are balanced
        if not self._is_balanced(expression):
            raise ValueError("Expression contains unbalanced parentheses.")

        # Tokenize the expression into numbers, operators, and parentheses
        self.tokens = self._tokenize(expression)
        self.current = 0  # Pointer to the current token

        # Parse and evaluate the expression based on operator precedence
        result = self._parse_expression()

        # If there are unused tokens, then the expression format is incorrect.
        if self.current != len(self.tokens):
            raise ValueError("Invalid syntax: unexpected tokens found.")
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Removes spaces from the expression and validates its characters.

        Args:
            expression (str): The original arithmetic expression.

        Returns:
            str: The cleaned expression without spaces.

        Raises:
            ValueError: If the expression contains any characters
                        other than digits, '.', '+', '-', '*', '/', '(', or ')'.
        """
        allowed_chars = set("0123456789.+-*/() ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether the expression has properly paired parentheses.

        Args:
            expression (str): A cleaned arithmetic expression.

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

    def _tokenize(self, expression: str) -> list:
        """
        Converts the arithmetic expression into a list of tokens (numbers,
        operators, and parentheses).

        Args:
            expression (str): The normalized arithmetic expression.

        Returns:
            list: A list of string tokens extracted from the expression.

        Raises:
            ValueError: If an invalid character or an improperly formatted number is found.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char in "+-*/()":
                tokens.append(char)
                i += 1
            elif char.isdigit() or char == '.':
                num_chars = []
                dot_encountered = False
                # Read the entire number (handling decimals)
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        if dot_encountered:
                            raise ValueError("Invalid number format: multiple decimal points.")
                        dot_encountered = True
                    num_chars.append(expression[i])
                    i += 1
                tokens.append(''.join(num_chars))
            else:
                raise ValueError(f"Invalid character encountered: '{char}'")
        return tokens

    def _parse_expression(self) -> float:
        """
        Parses an expression based on the grammar:
            Expression -> Term { ('+' | '-') Term }*

        Returns:
            float: The evaluated result of the expression.
        """
        result = self._parse_term()
        # Process any addition or subtraction operators
        while self.current < len(self.tokens) and self.tokens[self.current] in ('+', '-'):
            op = self.tokens[self.current]
            self.current += 1
            right = self._parse_term()
            if op == '+':
                result += right
            elif op == '-':
                result -= right
        return result

    def _parse_term(self) -> float:
        """
        Parses a term based on the grammar:
            Term -> Factor { ('*' | '/') Factor }*

        Returns:
            float: The evaluated result of the term.
        """
        result = self._parse_factor()
        # Process multiplication and division operators
        while self.current < len(self.tokens) and self.tokens[self.current] in ('*', '/'):
            op = self.tokens[self.current]
            self.current += 1
            right = self._parse_factor()
            if op == '*':
                result *= right
            elif op == '/':
                if right == 0:
                    raise ValueError("Division by zero error.")
                result /= right
        return result

    def _parse_factor(self) -> float:
        """
        Parses a factor based on the grammar:
            Factor -> NUMBER | '(' Expression ')' | ('+' | '-') Factor

        Returns:
            float: The evaluated result of the factor.

        Raises:
            ValueError: If the factor is invalid or improperly formatted.
        """
        if self.current >= len(self.tokens):
            raise ValueError("Unexpected end of expression.")

        token = self.tokens[self.current]

        # Handle unary plus (e.g., +5)
        if token == '+':
            self.current += 1
            return self._parse_factor()

        # Handle unary minus (e.g., -5)
        if token == '-':
            self.current += 1
            return -self._parse_factor()

        # Process expressions enclosed in parentheses.
        if token == '(':
            self.current += 1
            result = self._parse_expression()
            if self.current >= len(self.tokens) or self.tokens[self.current] != ')':
                raise ValueError("Missing closing parenthesis.")
            self.current += 1  # Skip the closing parenthesis
            return result

        # At this point, the token should be a number.
        try:
            value = float(token)
            self.current += 1
            return value
        except ValueError:
            raise ValueError(f"Invalid number: {token}")


if __name__ == "__main__":
    def main():
        """
        Runs the console-based arithmetic calculator, allowing the user to
        enter expressions until 'exit' is provided.
        """
        calculator = Calculator()
        print("Arithmetic Calculator")
        print("Enter 'exit' to quit.")
        while True:
            expression = input("Enter expression: ")
            if expression.strip().lower() == "exit":
                break
            try:
                result = calculator.calculate(expression)
                print("Result:", result)
            except Exception as ex:
                print("Error:", ex)

    main()
