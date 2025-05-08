import re

class Calculator:
    """
    A console-based arithmetic calculator class that evaluates arithmetic expressions.
    
    Supported features:
      - Operations: addition (+), subtraction (-), multiplication (*), and division (/)
      - Parentheses for grouping: ()
      - Correct operator precedence and associativity
      - Both integers and floating-point numbers, including negative values
      
    The calculator validates the input expression for unbalanced parentheses,
    invalid characters, and division by zero.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression provided as a string.
        
        The expression may contain numbers, parentheses, and the operators:
        +, -, *, /. Correct operator precedence is observed, and negative numbers
        are supported via unary operators.
        
        Args:
            expression (str): The arithmetic expression to evaluate.
            
        Returns:
            float: The result of the evaluated expression.
        
        Raises:
            ValueError: If the expression contains invalid characters, is unbalanced,
                        or contains unexpected tokens.
            ZeroDivisionError: If a division by zero is encountered.
        """
        tokens = self._tokenize(expression)
        if not tokens:
            raise ValueError("The expression is empty.")
        self.tokens = tokens
        self.index = 0
        result = self._parse_expression()
        if self.index < len(self.tokens):
            raise ValueError(
                f"Unexpected token '{self.tokens[self.index]}' at position {self.index}."
            )
        return result

    def _tokenize(self, expression: str) -> list:
        """
        Converts the input expression string into a list of tokens.

        A token is either:
          - A number (integer or floating point, including numbers like '.5')
          - An operator: +, -, *, /
          - A parenthesis: ( or )

        Args:
            expression (str): The arithmetic expression.
            
        Returns:
            list: The list of tokens.
            
        Raises:
            ValueError: If an invalid character is encountered.
        """
        # Pattern explanation:
        #   \s*                 -> Skip any leading whitespace
        #   (?:
        #       (\d+(?:\.\d+)?) -> Group 1: integer or floating point with an integer part
        #     | (\.\d+)         -> Group 2: floating point numbers starting with a dot
        #     | ([+\-*/()])     -> Group 3: operators or parentheses
        #   )
        token_pattern = r'\s*(?:(\d+(?:\.\d+)?)|(\.\d+)|([+\-*/()]))'
        tokens = []
        pos = 0
        while pos < len(expression):
            match = re.match(token_pattern, expression[pos:])
            if not match:
                # If no match is found and the character is not just whitespace,
                # it means an invalid character was encountered.
                if expression[pos].isspace():
                    pos += 1
                    continue
                else:
                    raise ValueError(f"Invalid character '{expression[pos]}' at position {pos}.")
            # Append the first non-None matching group as the token.
            if match.group(1) is not None:
                tokens.append(match.group(1))
            elif match.group(2) is not None:
                tokens.append(match.group(2))
            elif match.group(3) is not None:
                tokens.append(match.group(3))
            else:
                raise ValueError("Unknown token encountered.")
            pos += match.end()
        return tokens

    def _current_token(self):
        """Returns the current token if available, otherwise None."""
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        return None

    def _consume_token(self):
        """Consumes the current token and advances to the next."""
        token = self._current_token()
        self.index += 1
        return token

    def _parse_expression(self) -> float:
        """
        Parses an expression, managing the addition and subtraction operations.
        
        Grammar:
            expression := term (('+' | '-') term)*
        
        Returns:
            float: The evaluated result of the expression.
        """
        value = self._parse_term()
        while True:
            token = self._current_token()
            if token in ('+', '-'):
                op = self._consume_token()
                right = self._parse_term()
                if op == '+':
                    value += right
                else:
                    value -= right
            else:
                break
        return value

    def _parse_term(self) -> float:
        """
        Parses a term, managing multiplication and division.
        
        Grammar:
            term := factor (('*' | '/') factor)*
        
        Returns:
            float: The evaluated result of the term.
        """
        value = self._parse_factor()
        while True:
            token = self._current_token()
            if token in ('*', '/'):
                op = self._consume_token()
                right = self._parse_factor()
                if op == '*':
                    value *= right
                elif op == '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero.")
                    value /= right
            else:
                break
        return value

    def _parse_factor(self) -> float:
        """
        Parses a factor, which may be:
          - A number
          - A parenthesized expression
          - A unary operation with '+' or '-'
        
        Grammar:
            factor := ('+' | '-') factor | number | '(' expression ')'
        
        Returns:
            float: The evaluated result of the factor.
        """
        token = self._current_token()
        if token is None:
            raise ValueError("Unexpected end of expression.")

        # Handle unary operators
        if token == '+':
            self._consume_token()
            return self._parse_factor()
        elif token == '-':
            self._consume_token()
            return -self._parse_factor()
        elif token == '(':
            self._consume_token()  # Consume '('
            value = self._parse_expression()
            if self._current_token() != ')':
                raise ValueError("Unbalanced parentheses: missing ')'.")
            self._consume_token()  # Consume ')'
            return value
        else:
            # Attempt to parse a number.
            try:
                value = float(token)
                self._consume_token()
                return value
            except ValueError:
                raise ValueError(f"Invalid number: '{token}'.")

if __name__ == '__main__':
    calculator = Calculator()
    print("Console-based Arithmetic Calculator")
    print("Enter an arithmetic expression to evaluate or type 'exit' to quit.")

    while True:
        expr = input("Expression: ")
        if expr.strip().lower() == "exit":
            break
        try:
            result = calculator.calculate(expr)
            print("Result:", result)
        except Exception as error:
            print("Error:", error)
