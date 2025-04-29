import re  # Importing the regular expression module

class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It adheres to the correct
    order of operations and handles various error conditions.
    """

    def __init__(self):
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, division by zero,
                        or syntax errors).
        """
        try:
            expression = expression.replace(" ", "")  # Remove spaces
            tokens = self._tokenize(expression)  # generates a list of tokens
            postfix = self._shunting_yard(tokens)  # convert to RPN expression
            result = self._evaluate_postfix(postfix)  # evaluates RPN expression and returns the result
            return result
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"Invalid expression: {e}") from e

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the expression into a list of numbers, operators, and parentheses.

        Args:
            expression: The arithmetic expression.

        Returns:
            A list of tokens.

        Raises:
            ValueError: If there are invalid characters in the expression.
        """
        # Regex pattern for tokenization, handling multi-digit numbers and decimals correctly
        pattern = r"(\d+\.?\d*)|([\+\-\*/()])"
        tokens = []
        for match in re.findall(pattern, expression):
            number, operator = match
            if number:
                tokens.append(number)  # Add numeric tokens
            elif operator:
                tokens.append(operator)  # Add operator tokens

        # Check for invalid characters
        allowed_chars = set("0123456789+-*/().")
        expression_chars = set(expression)
        if not expression_chars.issubset(allowed_chars):
            invalid_chars = expression_chars - allowed_chars
            raise ValueError(f"Invalid characters: {', '.join(invalid_chars)}")
        return tokens

    def _shunting_yard(self, tokens: list) -> list:
        """
        Converts the token list from infix notation to postfix notation
        using the Shunting Yard algorithm.

        Args:
            tokens: A list of tokens in infix notation.

        Returns:
            A list of tokens in postfix notation.

        Raises:
            ValueError: If parentheses are unbalanced.
        """
        output_queue = []
        operator_stack = []
        paren_count = 0 # count number of parentheses

        for token in tokens:
            if re.match(r"\d+\.?\d*", token): # token is a number, including decimals: integer or decimal
                output_queue.append(float(token)) # convert them to float
            elif token in self.precedence:  # token is an operator
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       self.precedence[operator_stack[-1]] >= self.precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':  # token is a left parenthesis
                operator_stack.append(token)
                paren_count += 1
            elif token == ')':  # token is a right parenthesis
                paren_count -= 1
                if paren_count < 0: # there should not be a closing parenthesis before an opening parenthesis
                    raise ValueError("Unbalanced parentheses (extra closing parenthesis).")
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack: # there is no open parentheses
                    raise ValueError("Unbalanced parentheses (missing opening parenthesis).")

                operator_stack.pop()  # Pop the '('

        while operator_stack: # there are still tokens in the stack
            if operator_stack[-1] == '(': # stack shouldn't contain any '('
                raise ValueError("Unbalanced parentheses (missing closing parenthesis).")
            output_queue.append(operator_stack.pop())

        if paren_count != 0:
            raise ValueError("Unbalanced parentheses (parentheses count mismatch).")
        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            tokens: A list of tokens in postfix notation.

        Returns:
            The result of the expression.

        Raises:
            ValueError: If there's a division by zero or a syntax error.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float): # all tokens are float here
                stack.append(token)
            else:  # Token is an operator
                if len(stack) < 2:
                    raise ValueError("Syntax error: Insufficient operands.")
                try:

                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise ValueError("Syntax error: malformed expression")

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
                else: # operator is not present in the stack
                    raise ValueError(f"Unknown operator: {token}")

        if len(stack) != 1:
            raise ValueError("Syntax error: Too many operands.")
        return stack[0]


# --- Example Usage and Testing ---
if __name__ == "__main__":
    calculator = Calculator()

    test_cases = [
        ("2 + 3 * 4", 14.0),
        ("(2 + 3) * 4", 20.0),
        ("10 / (2 + 3)", 2.0),
        ("10 / 2 + 3", 8.0),
        ("1 + 2 * (3 - 1) / 2", 3.0),
        ("-5 + 2", -3.0),
        ("2.5 * 4", 10.0),
        ("10 / 2.5", 4.0),
        ("10 / 0", "Division by zero"),  # Division by zero
        ("2 + + 3", "Syntax error: Insufficient operands."),  # Invalid syntax
        ("2 * (3 + )", "Invalid expression: Unbalanced parentheses (extra closing parenthesis)."), # mismatched parentheses
        ("(2 * (3 + 4)", "Invalid expression: Unbalanced parentheses (missing closing parenthesis)."),  # Unbalanced parentheses
        ("2 * 3 + $", "Invalid expression: Invalid characters: $"),  # Invalid character
        ("", "Syntax error: Too many operands."), # empty expression
        ("()", "Syntax error: Too many operands.") # empty parenthesis

    ]

    for expression, expected in test_cases:
        try:
            result = calculator.calculate(expression)
            print(f"Expression: {expression}, Result: {result}, Expected: {expected}")
            assert result == expected, f"Test failed for {expression}: Expected {expected}, got {result}"
        except ValueError as e:
            print(f"Expression: {expression}, Error: {e}, Expected: {expected}")
            assert str(e) == str(expected),  f"Test failed for {expression}: Expected {expected}, got {e}"

    print("All test cases passed!")
