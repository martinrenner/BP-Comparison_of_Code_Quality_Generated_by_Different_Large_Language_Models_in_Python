class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.

    This class implements basic arithmetic operations (+, -, *, /), supports parentheses,
    and handles the correct order of operations.  It performs input validation and
    raises appropriate exceptions for invalid input.
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
        """
        normalized_expression = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expression):
            raise ValueError("Unbalanced parentheses.")

        return self._evaluate(normalized_expression)

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression. Removes spaces and validates characters.

        Args:
            expression (str): The mathematical expression.

        Returns:
            str: The normalized expression.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if the parentheses in the expression are balanced.

        Args:
            expression (str): The mathematical expression.

        Returns:
            bool: True if parentheses are balanced, False otherwise.
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


    def _evaluate(self, expression: str) -> float:
        """
        Evaluates the normalized mathematical expression.

        Args:
            expression: The normalized mathematical expression.

        Returns:
             float: The result of evaluating the expression.
        """
        tokens = self._tokenize(expression)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _tokenize(self, expression: str) -> list:
        """
        Converts the expression string into a list of tokens (numbers and operators).

        Args:
            expression (str): The mathematical expression.

        Returns:
            list: List of tokens.
        """
        tokens = []
        current_number = ""
        for char in expression:
            if char.isdigit() or char == '.':
                current_number += char
            else:
                if current_number:
                    tokens.append(float(current_number))
                    current_number = ""
                if char in "+-*/()":
                    tokens.append(char)
                elif char != " ":
                    raise ValueError(f"Invalid character: {char}")
        if current_number:
            tokens.append(float(current_number))
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts a list of tokens from infix notation to postfix notation (Reverse Polish Notation).

        Args:
            tokens (list): List of tokens in infix notation.

        Returns:
            list: List of tokens in postfix notation.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Pop the '('
            elif token in precedence:
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], 0) >= precedence.get(token, 0)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a list of tokens in postfix notation.

        Args:
            tokens (list): List of tokens in postfix notation.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If division by zero is attempted.
        """
        stack = []
        for token in tokens:
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
            raise ValueError("Invalid expression")
        return stack[0]



# Example Usage
if __name__ == "__main__":
    calculator = Calculator()

    while True:
        try:
            expression = input("Enter a mathematical expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print("Result:", result)
        except ValueError as e:
            print("Error:", e)
