class Calculator:
    """
    A console-based arithmetic calculator that supports basic operations,
    parentheses, and correct order of operations.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
            TypeError: If the expression type is incorrect.
        """
        try:
            normalized_expression = self._normalize_expression(expression)
            if not self._is_balanced(normalized_expression):
                raise ValueError("Unbalanced parentheses.")

            tokens = self._tokenize(normalized_expression)
            postfix_tokens = self._shunting_yard(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except ZeroDivisionError:
            raise ValueError("Division by zero.")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid expression: {e}")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {e}")


    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.

        Args:
            expression (str): A mathematical expression as a string.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")
    
    def _is_balanced(self, expression: str) -> bool:
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
                    return False
                stack.pop()
        return not stack

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes a mathematical expression.

        Args:
            expression (str): The normalized mathematical expression.

        Returns:
            list: A list of tokens (numbers and operators).
        """
        tokens = []
        current_number = ""
        for char in expression:
            if char.isdigit() or char == '.':
                current_number += char
            else:
                if current_number:
                    tokens.append(current_number)
                    current_number = ""
                if char in "+-*/()":  # Only append valid operators
                    tokens.append(char)
        if current_number:
            tokens.append(current_number)
        return tokens

    def _precedence(self, operator: str) -> int:
        """
        Returns the precedence of an operator.

        Args:
            operator (str): The operator.

        Returns:
            int: The precedence of the operator.
        """
        if operator in ('+', '-'):
            return 1
        elif operator in ('*', '/'):
            return 2
        return 0  # For parentheses

    def _shunting_yard(self, tokens: list) -> list:
        """
        Converts an infix expression to postfix using the Shunting Yard algorithm.

        Args:
            tokens (list): A list of tokens in infix notation.

        Returns:
            list: A list of tokens in postfix notation.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit():  # Check if it's a number
                output_queue.append(float(token))
            elif token in ('+', '-', '*', '/'):
                while (operator_stack and operator_stack[-1] != '(' and
                       self._precedence(operator_stack[-1]) >= self._precedence(token)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Remove the '('

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())

        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            tokens (list): A list of tokens in postfix notation.

        Returns:
            float: The result of the evaluation.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: Not enough operands")
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
             raise ValueError("Invalid expression: Too many operands")
        return stack[0]


# Example Usage and Testing
calculator = Calculator()

test_cases = [
    ("2 + 3 * 4", 14.0),
    ("(2 + 3) * 4", 20.0),
    "10 / (2 + 3)", 2.0),
    "10 / 2 + 3", 8.0),
    "-5 + 2", -3.0),
    "5 + -2", 3.0),
    "2 * (3 + 4) / 7", 2.0),
    "1.5 * 2 + 1", 4.0),
    "1 + 2 * (3 * (4 + 5) - 6) / 7", 8.714285714285714),  # More complex
    ("2 / 0", "Division by zero"),  # Division by zero
    ("2 + (3 * )", "Invalid expression: Mismatched parentheses"),  # Invalid
    ("2a + 3", "Invalid expression: Expression contains invalid characters."),
    # Test cases for invalid input in _evaluate_postfix
    ("1 2 + +",  "Invalid expression: Too many operands"),
    ("1 +", "Invalid expression: Not enough operands"),
]


for expression, expected in test_cases:
    try:
        result = calculator.calculate(expression)
        print(f"'{expression}' = {result}")
        assert result == expected or (isinstance(result, float) and abs(result - expected) < 1e-9) , f"Test failed for '{expression}'. Expected {expected}, got {result}"
    except ValueError as e:
        print(f"'{expression}' => Error: {e}")
        assert str(e) == expected, f"Test failed for '{expression}'. Expected Error: {expected}, got {e}"

print("All tests passed!")
