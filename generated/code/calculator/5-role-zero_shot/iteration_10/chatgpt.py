class Calculator:
    """
    A console-based arithmetic calculator that supports addition (+),
    subtraction (-), multiplication (*), division (/), and parentheses ().
    
    This class evaluates arithmetic expressions following operator precedence.
    It accepts integers and floating-point numbers, including negative values.
    
    Methods:
        calculate(expression: str) -> float
            Evaluates the arithmetic expression and returns the result as a float.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return the computed result.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the computation.

        Raises:
            ValueError: If the expression contains invalid syntax, unbalanced parentheses,
                        or unsupported characters.
            ZeroDivisionError: If a division by zero is encountered.
        """
        self.tokens = self._tokenize(expression)
        self.current = 0  # Pointer to the current token
        result = self._parse_expression()
        # After parsing we should have processed all tokens.
        if self.current < len(self.tokens):
            raise ValueError(f"Invalid syntax: unexpected token '{self.tokens[self.current]}'")
        return result

    def _tokenize(self, expression: str):
        """
        Convert the expression string into a list of tokens.

        Valid tokens include numbers (as strings supporting integers and floats),
        operators: '+', '-', '*', '/', and parentheses: '(' and ')'.

        Args:
            expression (str): The arithmetic expression.

        Returns:
            List[str]: A list of tokens.

        Raises:
            ValueError: If an invalid character or multiple decimal points in a number
                        are found.
        """
        tokens = []
        i = 0
        while i < len(expression):
            ch = expression[i]
            if ch.isspace():
                i += 1
                continue
            elif ch in '+-*/()':
                tokens.append(ch)
                i += 1
            elif ch.isdigit() or ch == '.':
                num_str = ''
                dot_count = 0
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid syntax: multiple decimals in a number")
                    num_str += expression[i]
                    i += 1
                # Attempt to convert to float to validate the number format.
                try:
                    float(num_str)
                except ValueError:
                    raise ValueError(f"Invalid number: {num_str}")
                tokens.append(num_str)
            else:
                raise ValueError(f"Invalid character: '{ch}'")
        return tokens

    def _parse_expression(self):
        """
        Parse an 'expression' which is defined as:
            expression = term { ('+' | '-') term }*
        This method handles addition and subtraction.

        Returns:
            float: The computed result for this part of the expression.
        """
        result = self._parse_term()
        while self.current < len(self.tokens) and self.tokens[self.current] in ('+', '-'):
            op = self.tokens[self.current]
            self.current += 1  # Consume the operator
            next_term = self._parse_term()
            if op == '+':
                result += next_term
            elif op == '-':
                result -= next_term
        return result

    def _parse_term(self):
        """
        Parse a 'term' which is defined as:
            term = factor { ('*' | '/') factor }*
        This method handles multiplication and division.

        Returns:
            float: The computed result for this term.
        """
        result = self._parse_factor()
        while self.current < len(self.tokens) and self.tokens[self.current] in ('*', '/'):
            op = self.tokens[self.current]
            self.current += 1  # Consume the operator
            next_factor = self._parse_factor()
            if op == '*':
                result *= next_factor
            elif op == '/':
                if next_factor == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= next_factor
        return result

    def _parse_factor(self):
        """
        Parse a 'factor' which handles:
            - Unary plus and minus: '+' factor or '-' factor.
            - Parenthesized expressions.
            - Numbers.

        Returns:
            float: The computed result for this factor.

        Raises:
            ValueError: If an unexpected token is encountered or there is an
                        unbalanced parenthesis.
        """
        if self.current >= len(self.tokens):
            raise ValueError("Invalid syntax: unexpected end of expression")

        token = self.tokens[self.current]

        # Handle unary plus and minus
        if token == '+':
            self.current += 1
            return self._parse_factor()
        elif token == '-':
            self.current += 1
            return -self._parse_factor()
        # Handle parenthesized expressions
        elif token == '(':
            self.current += 1  # Consume '('
            result = self._parse_expression()
            if self.current >= len(self.tokens) or self.tokens[self.current] != ')':
                raise ValueError("Unbalanced parentheses: missing ')'")
            self.current += 1  # Consume ')'
            return result
        else:
            # Token should be a valid number at this point.
            try:
                value = float(token)
            except ValueError:
                raise ValueError(f"Invalid number: {token}")
            self.current += 1
            return value

if __name__ == "__main__":
    # Instantiate the calculator
    calc = Calculator()
    print("Console-based Arithmetic Calculator")
    print("Enter arithmetic expressions, or type 'q' to quit.\n")
    
    while True:
        try:
            expr = input(">> ")
            if expr.strip().lower() in ("q", "quit", "exit"):
                print("Exiting calculator.")
                break
            result = calc.calculate(expr)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
