import re

class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses. It correctly handles operator
    precedence and supports both integers and floating-point numbers (including negatives).
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluate the arithmetic expression provided as a string.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The numerical result of the evaluation.

        Raises:
            ValueError: If the expression contains invalid characters, unbalanced parentheses,
                        or is otherwise syntactically invalid.
            ZeroDivisionError: If a division by zero is attempted.
        """
        # Remove leading/trailing whitespace and check for an empty expression.
        expression = expression.strip()
        if not expression:
            raise ValueError("Empty expression provided.")

        # Validate that the expression contains only allowed characters.
        allowed_chars = set("0123456789+-*/(). ")
        for ch in expression:
            if ch not in allowed_chars:
                raise ValueError(f"Invalid character found in expression: '{ch}'")

        # Tokenize the expression.
        tokens = self._tokenize(expression)
        if not tokens:
            raise ValueError("No valid tokens found in expression.")

        # Parse the tokens and evaluate the expression.
        result, index = self._parse_expression(tokens, 0)
        if index != len(tokens):
            raise ValueError("Invalid expression: unprocessed tokens remain.")

        return result

    def _tokenize(self, expression: str) -> list:
        """
        Convert the expression string into a list of tokens.

        Tokens include numbers (integer or float) and the operators: +, -, *, /, ( and ).

        Args:
            expression (str): The arithmetic expression.

        Returns:
            list: A list of tokens (strings).
        """
        # The regex matches integers, decimals (with leading or trailing digits) and operators.
        token_pattern = r'\d*\.\d+|\d+|[()+\-*/]'
        tokens = re.findall(token_pattern, expression)
        return tokens

    def _parse_expression(self, tokens: list, index: int) -> (float, int):
        """
        Recursive parser for expressions supporting addition and subtraction.

        Grammar:
            Expression -> Term { ('+' | '-') Term }

        Args:
            tokens (list): List of expression tokens.
            index (int): Current index in the token list.

        Returns:
            Tuple[float, int]: The evaluated result and the updated index.
        """
        value, index = self._parse_term(tokens, index)

        while index < len(tokens) and tokens[index] in ('+', '-'):
            op = tokens[index]
            index += 1
            next_value, index = self._parse_term(tokens, index)
            if op == '+':
                value += next_value
            else:
                value -= next_value

        return value, index

    def _parse_term(self, tokens: list, index: int) -> (float, int):
        """
        Recursive parser for terms supporting multiplication and division.

        Grammar:
            Term -> Factor { ('*' | '/') Factor }

        Args:
            tokens (list): List of expression tokens.
            index (int): Current index in the token list.

        Returns:
            Tuple[float, int]: The evaluated term and the updated index.
        """
        value, index = self._parse_factor(tokens, index)

        while index < len(tokens) and tokens[index] in ('*', '/'):
            op = tokens[index]
            index += 1
            next_value, index = self._parse_factor(tokens, index)
            if op == '*':
                value *= next_value
            else:
                if next_value == 0:
                    raise ZeroDivisionError("Division by zero encountered.")
                value /= next_value

        return value, index

    def _parse_factor(self, tokens: list, index: int) -> (float, int):
        """
        Recursive parser for factors which can be:
        - A number (integer or float)
        - A parenthesized expression
        - A unary +/- expression

        Grammar:
            Factor -> ['+'|'-'] Factor | Number | '(' Expression ')'

        Args:
            tokens (list): List of expression tokens.
            index (int): Current index in the token list.

        Returns:
            Tuple[float, int]: The evaluated factor and the updated index.
        """
        if index >= len(tokens):
            raise ValueError("Unexpected end of expression.")

        token = tokens[index]

        # Handle unary plus or minus.
        if token == '-' or token == '+':
            op = token
            index += 1
            factor, index = self._parse_factor(tokens, index)
            return (-factor if op == '-' else factor), index

        # Handle parenthesized expressions.
        if token == '(':
            index += 1
            value, index = self._parse_expression(tokens, index)
            if index >= len(tokens) or tokens[index] != ')':
                raise ValueError("Mismatched parentheses in expression.")
            index += 1  # Consume the closing parenthesis.
            return value, index

        # Attempt to parse the token as a number.
        try:
            value = float(token)
        except ValueError:
            raise ValueError(f"Invalid number encountered: '{token}'")
        index += 1
        return value, index


def main():
    """
    Entry point for the console-based arithmetic calculator.
    
    Users can enter arithmetic expressions and view the evaluated result.
    Type 'exit' to terminate the calculator.
    """
    calculator = Calculator()
    print("Simple Arithmetic Calculator (supports +, -, *, /, and parentheses).")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nEnter an expression: ")
        if user_input.strip().lower() == 'exit':
            print("Exiting the calculator. Goodbye!")
            break

        try:
            result = calculator.calculate(user_input)
            print(f"Result: {result}")
        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
