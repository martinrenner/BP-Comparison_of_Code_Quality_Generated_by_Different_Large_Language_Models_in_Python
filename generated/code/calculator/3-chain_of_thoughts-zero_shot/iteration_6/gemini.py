import re  # Used for tokenization

class Calculator:
    """
    A console-based arithmetic calculator.

    This class implements a calculator that can evaluate arithmetic
    expressions with addition, subtraction, multiplication, division,
    and parentheses. It uses the Shunting Yard algorithm for correct
    operator precedence.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                parentheses, invalid characters, division by zero).
            TypeError: If an invalid operation type is detected.
        """
        try:
            tokens = self._tokenize(expression)
            postfix = self._shunting_yard(tokens)
            result = self._evaluate_postfix(postfix)
            return result
        except ZeroDivisionError:
            raise ZeroDivisionError("Division by zero detected.")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid expression: {e}")

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the input expression.

        Args:
            expression: The arithmetic expression.

        Returns:
            A list of tokens (numbers, operators, parentheses).
        """
        # Regular expression to split the expression into tokens.  Handles:
        #   - Numbers (integers and decimals, including negative numbers)
        #   - Operators (+, -, *, /)
        #   - Parentheses ( and )
        token_pattern = r"(-?\d+\.?\d*)|([+\-*/()])"

        tokens = []
        for match in re.finditer(token_pattern, expression):
            if match.group(1):  # It's a number (group 1 captures numbers)
                tokens.append(match.group(1))
            elif match.group(2):  # It's an operator or parenthesis (group 2 captures them)
                tokens.append(match.group(2))
            else: # Something went wrong with regex, what is not desirable.
                raise ValueError("Invalid characters detected during _tokenize().")

        return tokens
    def _shunting_yard(self, tokens: list) -> list:
        """
        Converts infix notation to postfix notation (Reverse Polish Notation).

        Args:
            tokens: The list of tokens in infix notation.

        Returns:
            A list of tokens in postfix notation.

        Raises:
            ValueError: If parentheses are unbalanced.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"^-?\d+\.?\d*$", token):  # If it's a number
                output.append(float(token))
            elif token in precedence:  # If it's an operator
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                try:
                    while operator_stack[-1] != '(':
                        output.append(operator_stack.pop())
                    operator_stack.pop()  # Pop the '('
                except IndexError:
                    raise ValueError("Unbalanced parentheses")
            else:
                raise ValueError(f"Invalid character: {token}")

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Unbalanced parentheses")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, postfix: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            postfix: The list of tokens in postfix notation.

        Returns:
            The result of the expression.

        Raises:
            ValueError: If the postfix expression contains unsupported tokens.
            TypeError: If there is not enough operands for an operation.
        """
        stack = []
        for token in postfix:
            if isinstance(token, float):  # Check if it's already a number
                stack.append(token)
            elif token == '+':
                try:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise TypeError("Not enough operands for '+' operation.")
                stack.append(operand1 + operand2)
            elif token == '-':
                try:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise TypeError("Not enough operands for '-' operation.")
                stack.append(operand1 - operand2)
            elif token == '*':
                try:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise TypeError("Not enough operands for '*' operation.")
                stack.append(operand1 * operand2)
            elif token == '/':
                try:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise TypeError("Not enough operands for '/' operation.")
                if operand2 == 0:
                    raise ZeroDivisionError("Division by zero")  # Explicitly handle here
                stack.append(operand1 / operand2)
            else:
                raise ValueError(f"Unsupported token in postfix expression: {token}")  # Should not occur
        return stack.pop()

# Interactive console loop for testing
if __name__ == "__main__":
    calculator = Calculator()
    while True:
        expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
        if expression.lower() == 'quit':
            break
        try:
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")

