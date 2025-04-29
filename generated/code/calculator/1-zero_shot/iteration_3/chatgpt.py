class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses with correct operator precedence.

    This calculator accepts both integers and floating-point numbers (including negative values)
    and performs input validation for unbalanced parentheses, invalid characters,
    and division by zero.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the computed result as a float.

        Parameters:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the arithmetic computation.

        Raises:
            ValueError: If the expression contains invalid syntax or characters.
            ZeroDivisionError: If there is a division by zero during evaluation.
        """
        # Tokenize the input expression
        self.tokens = self._tokenize(expression)
        self.pos = 0

        if not self.tokens:
            raise ValueError("The expression is empty.")

        # Parse the expression using recursive descent
        result = self._parse_expression()

        # Ensure that all tokens were consumed.
        if self.pos < len(self.tokens):
            raise ValueError(
                f"Invalid syntax: unexpected token '{self.tokens[self.pos]}' at position {self.pos}."
            )

        return result

    def _tokenize(self, expression: str):
        """
        Converts the input expression string into a list of tokens.

        Tokens may be numbers (stored as floats), operators (+, -, *, /), or
        parentheses.

        Parameters:
            expression (str): The expression to tokenize.

        Returns:
            list: A list of tokens extracted from the expression.

        Raises:
            ValueError: If the expression contains invalid characters or format.
        """
        tokens = []
        i = 0
        # Remove all whitespace characters for easier token processing.
        expr = expression.replace(" ", "")
        while i < len(expr):
            char = expr[i]

            if char in "+-*/()":
                tokens.append(char)
                i += 1
            elif char.isdigit() or char == ".":
                # Build the number, ensuring proper decimal handling.
                num_str = char
                i += 1
                dot_count = 1 if char == "." else 0
                while i < len(expr) and (expr[i].isdigit() or expr[i] == "."):
                    if expr[i] == ".":
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError(f"Invalid number format: {num_str + expr[i]}")
                    num_str += expr[i]
                    i += 1
                try:
                    num_value = float(num_str)
                except ValueError:
                    raise ValueError(f"Invalid number '{num_str}'.")
                tokens.append(num_value)
            else:
                raise ValueError(f"Invalid character '{char}' in expression.")
        return tokens

    def _parse_expression(self) -> float:
        """
        Parses an expression according to the grammar:
            Expression -> Term { ('+' | '-') Term }*
        
        Returns:
            float: The computed value of the expression.
        """
        result = self._parse_term()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ("+", "-"):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self._parse_term()
            result = result + right if op == "+" else result - right
        return result

    def _parse_term(self) -> float:
        """
        Parses a term according to the grammar:
            Term -> Factor { ('*' | '/') Factor }*
        
        Returns:
            float: The computed value of the term.
        
        Raises:
            ZeroDivisionError: If division by zero occurs.
        """
        result = self._parse_factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ("*", "/"):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self._parse_factor()
            if op == "*":
                result *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero.")
                result /= right
        return result

    def _parse_factor(self) -> float:
        """
        Parses a factor according to the grammar:
            Factor -> Number | '(' Expression ')' | ('+' | '-') Factor

        Returns:
            float: The computed value of the factor.

        Raises:
            ValueError: If a syntax error is encountered.
        """
        # Handle unary operators
        if self.pos < len(self.tokens) and self.tokens[self.pos] in ("+", "-"):
            op = self.tokens[self.pos]
            self.pos += 1
            value = self._parse_factor()
            return value if op == "+" else -value

        token = self.tokens[self.pos]

        if token == "(":
            self.pos += 1
            result = self._parse_expression()
            if self.pos >= len(self.tokens) or self.tokens[self.pos] != ")":
                raise ValueError("Unbalanced parentheses: missing closing ')'.")
            self.pos += 1  # Consume the closing parenthesis
            return result

        if isinstance(token, (int, float)):
            self.pos += 1
            return token

        raise ValueError(f"Unexpected token '{token}' encountered during parsing.")


def main():
    """
    Main function for the console-based arithmetic calculator.
    Continuously prompts the user for input, computes the expression,
    and prints the result. Type 'exit' or 'quit' to terminate.
    """
    calc = Calculator()
    print("Arithmetic Calculator")
    print("Enter 'exit' or 'quit' to end the program.")

    while True:
        try:
            expression = input("Enter expression: ")
            if expression.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            result = calc.calculate(expression)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
