import re


class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions with
    addition, subtraction, multiplication, division, and parentheses.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The mathematical expression as a string.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
        """
        normalized_expression = self._normalize_expression(expression)
        self._validate_balanced_parentheses(normalized_expression)
        tokens = self._tokenize(normalized_expression)
        return self._evaluate_tokens(tokens)

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression by removing spaces and validating characters.

        Args:
            expression (str): The input expression.

        Returns:
            str: The normalized expression.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")

    def _validate_balanced_parentheses(self, expression: str) -> None:
        """
        Validates that parentheses in the expression are balanced.

        Args:
            expression (str): The expression to validate.

        Raises:
            ValueError: If parentheses are unbalanced.
        """
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise ValueError("Unbalanced parentheses: unmatched ')'")
                stack.pop()
        if stack:
            raise ValueError("Unbalanced parentheses: unmatched '('")

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the expression into a list of numbers, operators, and parentheses.

        Args:
            expression: The normalized expression string.

        Returns:
            A list of tokens.
        """
        # Use regular expression to split the expression while keeping the delimiters
        return re.findall(r"(\b\d+\.?\d*\b|[()+*/-])", expression)

    def _evaluate_tokens(self, tokens: list) -> float:
        """
        Evaluates a list of tokens using the shunting yard algorithm and postfix evaluation.

        Args:
            tokens: List of tokens (numbers, operators, parentheses).

        Returns:
          The result of the evaluation.

        Raises:
            ValueError: if division by zero is attempted.
        """
        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if re.match(r"^\d+\.?\d*$", token):  # Check if token is a number (int or float)
                output_queue.append(float(token))
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence[operator_stack[-1]] >= precedence[token]):
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

        return self._evaluate_postfix(output_queue)

    def _evaluate_postfix(self, postfix_tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            postfix_tokens:  A list of tokens in postfix notation

        Returns:
            The result of the expression

        Raises:
            ValueError: If division by zero is attempted.
        """
        stack = []
        for token in postfix_tokens:
            if isinstance(token, float):
                stack.append(token)
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid expression")
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
                        raise ValueError("Division by zero")
                    stack.append(operand1 / operand2)

        if len(stack) != 1:
            raise ValueError("Invalid Expression")

        return stack[0]



def main():
    """
    Main function to run the calculator in a loop.
    """
    calculator = Calculator()
    while True:
        try:
            expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
