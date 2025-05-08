class Calculator:
    """
    A console-based arithmetic calculator that supports basic operations,
    parentheses, and decimal/negative numbers.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (unbalanced parentheses,
                        invalid characters, division by zero).
        """
        self._validate_parentheses(expression)
        self._validate_characters(expression)
        normalized_expression = expression.replace(" ", "")
        tokens = self._tokenize(normalized_expression)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _validate_parentheses(self, expression: str) -> None:
        """
        Checks whether a mathematical expression has properly paired parentheses.

        :param expression: A string containing the mathematical expression.
        :return: True if parentheses are correctly paired, otherwise False.
        """
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise ValueError("Unbalanced parentheses.")
                stack.pop()
        if stack:
            raise ValueError("Unbalanced parentheses.")

    def _validate_characters(self, expression: str) -> None:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.

        Args:
            expression (str): A mathematical expression as a string.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes a mathematical expression.

        Args:
            expression (str): The expression to tokenize.

        Returns:
            list: A list of tokens.
        """
        tokens = []
        current_number = ""
        for i, char in enumerate(expression):
            if char.isdigit() or char == '.':
                current_number += char
            elif char == '-' and (i == 0 or expression[i-1] in '+-*/('):
                # Handle negative numbers at the beginning or after an operator/parenthesis
                current_number += char
            else:
                if current_number:
                    tokens.append(current_number)
                    current_number = ""
                tokens.append(char)
        if current_number:
            tokens.append(current_number)
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts an infix expression to postfix notation (RPN).

        Args:
            tokens (list): A list of tokens in infix notation.

        Returns:
            list: A list of tokens in postfix notation.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit():  # Check if it's a number
                output.append(token)
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Remove the '('
                else:
                    raise ValueError("Mismatched parentheses") # Should be caught in validation
            else:
                raise ValueError(f"Invalid token: {token}")

        while operator_stack:
            if operator_stack[-1] == '(':
                 raise ValueError("Mismatched parentheses") # Should be caught in validation
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            tokens (list): A list of tokens in postfix notation.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., division by zero).
        """
        stack = []
        for token in tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit():
                stack.append(float(token))
            else:
                try:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise ValueError("Invalid expression: not enough operands")

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
                     raise ValueError(f"Invalid operator: {token}") # should never happen

        if len(stack) != 1:
             raise ValueError("Invalid expression: too many operands")
        return stack.pop()


calculator = Calculator()

# Test cases
test_cases = [
    ("2 + 3 * 4", 14.0),
    ("(2 + 3) * 4", 20.0),
    "10 / (2 + 3)", 2.0),
    "-5 + 3", -2.0),
    "1.5 * 2", 3.0),
    "10 / 0", "Division by zero"),  # Expected error
    "2 + (3 * 4", "Unbalanced parentheses."),  # Expected error
    "2 + a * 4", "Expression contains invalid characters."),  # Expected error
    '2+3*4-1', 13.0),
    '2 + ((3 * 4) - 1)', 13.0),
    '10 - (2 * (3 + 1))', 2.0),
    '-5 - (-3)', -2.0),
     '5', 5.0),  # Simple number
    '(-5)', -5.0),  # Negative number in parentheses
    '2 * (3 + 4) / (1 + 1)', 7.0),  # Mixed operators and parentheses
    '10 / (5 - 5)', "Division by zero"),   # Should raise an error
    '10 + (4 * 2) - 3', 15.0),
    '9 + (3 * (10 / (2 + 4) - 1)) * 2', 15.0),  # Complex scenario
    '1 + 2 + (3   +4) ', 10.0),  # Extra spaces
    '(2 + 3))', "Unbalanced parentheses."),
    '(1 + 2', "Unbalanced parentheses."),
    '2 + 3 * x', "Expression contains invalid characters."),  # Invalid character

]


for expression, expected in test_cases:
    try:
        result = calculator.calculate(expression)
        print(f"'{expression}' = {result}")
        assert result == expected, f"Expected {expected}, got {result}"
    except ValueError as e:
        print(f"'{expression}' => Error: {e}")
        assert str(e) == expected, f"Expected error message '{expected}', got '{e}'"

print("All test cases passed!")
