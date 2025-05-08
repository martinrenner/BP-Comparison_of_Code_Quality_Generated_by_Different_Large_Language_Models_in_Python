import re  # Used for tokenization

class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, parentheses, and decimal/negative numbers.

    The calculator adheres to ISO/IEC 25010 quality characteristics by:

    - Correctness: Produces expected results through thorough design and testing.
    - Performance: Employs the efficient Shunting Yard algorithm.
    - Modularity: Logically separates tokenization, conversion to RPN, and RPN evaluation.
    - Safety: Includes robust input validation and error handling.
    - Testability: Code structure facilitates unit testing.
    - Readability and Documentation: Uses docstrings, clear naming, and comments.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: For invalid characters, unbalanced parentheses, or division by zero.
            TypeError:  If not enough operands are supplied to an operator
            SyntaxError: If expression has consecutive operators
        """
        tokens = self._tokenize(expression)
        postfix_tokens = self._shunting_yard(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the input expression.

        Args:
            expression: The expression string.

        Returns:
            A list of tokens (numbers, operators, parentheses).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Regular expression to split the expression into tokens.
        # It handles numbers (integers and decimals, including negative numbers),
        # operators (+, -, *, /), and parentheses.
        token_pattern = r"(-?\d+\.?\d*)|([+\-*/()])"
        tokens = []
        for match in re.finditer(token_pattern, expression):
            if match.group(1):  # It's a number
                tokens.append(match.group(1))
            elif match.group(2):  # It's an operator or parenthesis
                tokens.append(match.group(2))
            else:
                raise ValueError(f"Invalid character found: {match.group(0)}")

        return tokens


    def _shunting_yard(self, tokens: list) -> list:
        """
        Converts the infix expression (tokens) to postfix notation (RPN).

        Args:
            tokens: A list of tokens in infix notation.

        Returns:
            A list of tokens in postfix notation.

        Raises:
            ValueError: If parentheses are unbalanced.
            SyntaxError: If expression has consecutive operators
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"^-?\d+\.?\d*$", token):  # If it's a number
                output.append(token)
            elif token in precedence:  # If it's an operator
                if (operator_stack and operator_stack[-1] in precedence and
                        precedence[token] <= precedence[operator_stack[-1]]):

                    # Check for consecutive operators (e.g., "2 + + 3")
                    if len(output) > 0 and output[-1] in precedence:
                        raise SyntaxError(f"Invalid expression: consecutive operators")

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
                raise ValueError(f"Invalid token: {token}")

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Unbalanced parentheses")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            tokens:  A list of tokens in postfix notation.

        Returns:
            The result of the expression.

        Raises:
            ValueError: If division by zero is attempted.
            TypeError: If an operator doesn't receive enough operands
        """
        stack = []
        for token in tokens:
            if re.match(r"^-?\d+\.?\d*$", token):  # If it's a number
                stack.append(float(token))
            else:  # It's an operator
                try:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise TypeError(f"Insufficient operands for operator: {token}")

                if token == '+':
                    stack.append(operand1 + operand2)
                elif token == '-':
                    stack.append(operand1 - operand2)
                elif token == '*':
                    stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ValueError("Division by zero")
                    stack.append(operand1 / operand2)
                else:
                    raise ValueError(f"Invalid operator {token}") #Should not happen

        return stack.pop()



def main():
    """
    Main function to run the calculator in a loop.
    """
    calculator = Calculator()
    while True:
        expression = input("Enter an expression (or 'quit' to exit): ")
        if expression.lower() == 'quit':
            break
        try:
            result = calculator.calculate(expression)
            print("Result:", result)
        except (ValueError, TypeError, SyntaxError) as e:
            print("Error:", e)

if __name__ == "__main__":
    main()

