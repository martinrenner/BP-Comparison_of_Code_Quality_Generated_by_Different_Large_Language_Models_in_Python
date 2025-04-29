import re  # Used for tokenization

class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It adheres to the order of
    operations and handles invalid input gracefully.
    """

    def __init__(self):
        self.precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
        }

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression contains invalid characters,
                        has an invalid format or unbalanced parenthesis.
            ZeroDivisionError: If the expression attempts division by zero.
            SyntaxError: If parenthesis are unbalanced
        """
        try:
            tokens = self._tokenize(expression)
            postfix = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix)
            return result
        except (ValueError, ZeroDivisionError, SyntaxError) as e:
            print(f"Error: {e}")  # Or handle the errors any way you see fit.
            raise

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the input expression.

        Args:
            expression: The expression string.

        Returns:
            A list of tokens (numbers, operators, parentheses).

        Raises:
            ValueError: if input is not valid
        """
        # Regex to split into tokens, handles integers, decimals, and operators
        tokens = re.findall(r"(\d+\.?\d*|\+|\-|\*|\/|\(|\))", expression)
        
        # Filter out any empty strings that might have resulted from extra spaces
        tokens = [t for t in tokens if t]
        
        # Simple validation of each token.
        for token in tokens:
            if not re.match(r"(\d+\.?\d*|\+|\-|\*|\/|\(|\))$", token):
                raise ValueError(f"Invalid character or token: {token}")
        return tokens
        

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts a list of tokens from infix notation to postfix notation
        using the Shunting Yard algorithm.

        Args:
            tokens: A list of tokens in infix notation.

        Returns:
            A list of tokens in postfix notation.

        Raises:
            SyntaxError: If parenthesis are unbalanced
        """
        output = []
        operator_stack = []
        parenthesis_check = 0

        for token in tokens:
            if re.match(r"(\d+\.?\d*)", token):  # If it's a number
                output.append(float(token))  # Convert to float and add to output
            elif token in self.precedence:  # If it's an operator
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       self.precedence[operator_stack[-1]] >= self.precedence[token]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
                parenthesis_check += 1
            elif token == ')':
                parenthesis_check -= 1
                if parenthesis_check < 0:
                    raise SyntaxError("Unbalanced parentheses")
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise SyntaxError("Unbalanced parentheses")
                operator_stack.pop()  # Pop the '('
            else:
                raise ValueError(f"Invalid token: {token}")
        if parenthesis_check != 0:
            raise SyntaxError("Unbalanced parentheses")

        while operator_stack:
            if operator_stack[-1] == '(':
                raise SyntaxError("Unbalanced parentheses")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a list of tokens in postfix notation.

        Args:
            tokens: A list of tokens in postfix notation.

        Returns:
            The result of the expression.

        Raises:
            ValueError:  If there are not enough operands for an operation.
            ZeroDivisionError: If there's an attempt to divide by zero.

        """
        stack = []

        for token in tokens:
            if isinstance(token, float):  # If token is a number
                stack.append(token)
            else:  # If token is an operator
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                operand2 = stack.pop()
                operand1 = stack.pop()
                if token == '+':
                    stack.append(operand1 + operand2)
                elif token == '-':
                    stack.append(operand1 - operand2)
                elif token == '*':
                    stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero")
                    stack.append(operand1 / operand2)

        if len(stack) != 1:
             raise ValueError("Invalid expression: too many operands")
        return stack.pop()


# Example usage in a console environment
if __name__ == "__main__":
    calculator = Calculator()

    while True:
        expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
        if expression.lower() == 'quit':
            break
        try:
            result = calculator.calculate(expression)
            print("Result:", result)
        except Exception as e:
             # Exception are caught on lower level, so this exception should never trigger
            print(f"An unexpected error occurred: {e}") # Only for any unexpected error

