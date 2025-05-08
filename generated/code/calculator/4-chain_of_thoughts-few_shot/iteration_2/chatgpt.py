class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions including addition, subtraction,
    multiplication, division, and supports parentheses. The calculator supports integer and decimal 
    numbers (including negative numbers) and enforces the correct operator precedence.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression string and returns its numerical result.

        Args:
            expression (str): A string representing the arithmetic expression to evaluate.
                              Example: "-(2.5 + 3) * 4 / (1 - 5)"

        Returns:
            float: The evaluated result.

        Raises:
            ValueError: If the expression contains invalid characters or unbalanced parentheses.
            ZeroDivisionError: If division by zero is attempted.
        """
        # Normalize expression: remove whitespace and validate allowed characters.
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("Expression has unbalanced parentheses.")

        # Tokenize the normalized expression.
        self.tokens = self._tokenize(normalized_expr)
        self.current_token_index = 0

        # Parse the tokens using recursive descent parsing.
        result = self._parse_expression()

        # If there are any remaining tokens, the expression is malformed.
        if self.current_token_index != len(self.tokens):
            raise ValueError("Invalid syntax: unused tokens remain.")

        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Removes spaces from the expression and validates that all characters are allowed.

        Args:
            expression (str): The input arithmetic expression.

        Returns:
            str: The normalized expression.

        Raises:
            ValueError: If any invalid character is found in the expression.
        """
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether the input expression has properly paired parentheses.

        Args:
            expression (str): The arithmetic expression.

        Returns:
            bool: True if parentheses are balanced, False otherwise.
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
        Converts the arithmetic expression string into a list of tokens
        (numbers and operators).

        Args:
            expression (str): The normalized arithmetic expression.

        Returns:
            list: A list of tokens (as strings). Numbers are kept as strings and will be converted later.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]

            # If the character is a digit or a decimal point, parse the full number.
            if char.isdigit() or char == '.':
                num_str = char
                i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                # Check if the number format is valid.
                if num_str.count('.') > 1:
                    raise ValueError(f"Invalid number format: {num_str}")
                tokens.append(num_str)
            # Operators and parentheses.
            elif char in "+-*/()":
                tokens.append(char)
                i += 1
            else:
                # Should not get here due to normalization.
                raise ValueError(f"Invalid character encountered: {char}")
        return tokens

    def _current_token(self) -> str:
        """
        Retrieves the current token from the list of tokens.

        Returns:
            str: The current token, or None if at the end of tokens.
        """
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def _advance(self) -> None:
        """
        Advances the current token pointer by one.
        """
        self.current_token_index += 1

    def _parse_expression(self) -> float:
        """
        Parses an expression which is a series of terms separated by '+' or '-' operators.
        Follows the grammar:
            Expression -> Term { ('+' | '-') Term }*
        
        Returns:
            float: The evaluated result of the expression.
        """
        result = self._parse_term()

        while True:
            token = self._current_token()
            if token == '+' or token == '-':
                self._advance()
                next_term = self._parse_term()
                if token == '+':
                    result += next_term
                else:
                    result -= next_term
            else:
                break

        return result

    def _parse_term(self) -> float:
        """
        Parses a term which is a series of factors separated by '*' or '/' operators.
        Follows the grammar:
            Term -> Factor { ('*' | '/') Factor }*
        
        Returns:
            float: The evaluated result of the term.

        Raises:
            ZeroDivisionError: When division by zero is encountered.
        """
        result = self._parse_factor()

        while True:
            token = self._current_token()
            if token == '*' or token == '/':
                self._advance()
                next_factor = self._parse_factor()
                if token == '*':
                    result *= next_factor
                else:
                    if next_factor == 0:
                        raise ZeroDivisionError("Division by zero encountered.")
                    result /= next_factor
            else:
                break

        return result

    def _parse_factor(self) -> float:
        """
        Parses a factor, handling unary plus and minus, followed by a primary.
        Follows the grammar:
            Factor -> { ('+' | '-') } Primary
        
        Returns:
            float: The evaluated result of the factor.
        """
        sign = 1
        # Handle any number of unary plus or minus.
        while True:
            token = self._current_token()
            if token == '+':
                self._advance()  # '+' does not change the sign.
            elif token == '-':
                self._advance()
                sign *= -1
            else:
                break

        primary_value = self._parse_primary()
        return sign * primary_value

    def _parse_primary(self) -> float:
        """
        Parses a primary element: either a number or a parenthesized expression.
        Follows the grammar:
            Primary -> number | '(' Expression ')'
        
        Returns:
            float: The evaluated result of the primary.

        Raises:
            ValueError: If the primary is not a valid number or expression.
        """
        token = self._current_token()
        if token is None:
            raise ValueError("Unexpected end of expression.")

        if token == '(':
            self._advance()  # Consume '('
            expr_value = self._parse_expression()
            if self._current_token() != ')':
                raise ValueError("Mismatched parentheses: ')' expected.")
            self._advance()  # Consume ')'
            return expr_value
        else:
            # Attempt to parse the token as a number.
            try:
                value = float(token)
                self._advance()
                return value
            except ValueError:
                raise ValueError(f"Invalid numeric value: {token}")


if __name__ == "__main__":
    # Console-based usage of the Calculator.
    calc = Calculator()
    print("Arithmetic Calculator. Enter an expression or type 'quit' to exit.")
    while True:
        try:
            user_input = input(">> ")
            if user_input.strip().lower() == "quit":
                break
            result = calc.calculate(user_input)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
