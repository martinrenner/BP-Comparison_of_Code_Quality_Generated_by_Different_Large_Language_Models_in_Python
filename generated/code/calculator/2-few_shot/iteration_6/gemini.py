import re  # Used for efficient splitting of the expression

class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses, adhering to operator precedence.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
            TypeError: If expression is not a string
        """
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string.")

        normalized_expression = self._normalize_expression(expression)
        self._validate_parentheses(normalized_expression)
        tokens = self._tokenize(normalized_expression)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result


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
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")

    def _validate_parentheses(self, expression: str) -> None:
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
                    raise ValueError("Unbalanced parentheses: unmatched ')' found.")
                stack.pop()
        if stack:
            raise ValueError("Unbalanced parentheses: unmatched '(' found.")

    def _tokenize(self, expression: str) -> list[str]:
        """
        Tokenizes the expression into a list of numbers and operators.  Handles
        multi-digit numbers and floating-point numbers correctly.  Uses a regex
        for efficient and correct splitting.

        Args:
            expression (str): The normalized expression.

        Returns:
            list[str]: A list of tokens.
        """
        # Split the expression by operators, keeping the operators and handling negative numbers correctly
        return re.findall(r"(\d+\.?\d*|[\+\-\*\/\(\)])", expression)

    def _infix_to_postfix(self, tokens: list[str]) -> list[str]:
        """
        Converts an infix expression (represented as a list of tokens) to
        postfix notation using the Shunting Yard algorithm.

        Args:
            tokens (list[str]): The list of tokens in infix notation.

        Returns:
            list[str]: The list of tokens in postfix notation.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"(\d+\.?\d*)", token):  # If it's a number
                output.append(token)
            elif token in precedence:  # If it's an operator
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")  # Extra ')'
                operator_stack.pop()  # Remove the '('

        while operator_stack:
            if operator_stack[-1] == '(':
                 raise ValueError("Mismatched parentheses") # Extra '('
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list[str]) -> float:
        """
        Evaluates a postfix expression represented as a list of tokens.

        Args:
            tokens (list[str]): The list of tokens in postfix notation.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., division by zero).
        """
        stack = []
        for token in tokens:
            if re.match(r"(\d+\.?\d*)", token):  # If it's a number
                stack.append(float(token))
            else:  # It's an operator
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands.")
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
                        raise ZeroDivisionError("Division by zero.")
                    stack.append(operand1 / operand2)

        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands.")
        return stack.pop()

def main():
    """
    Main function to run the calculator in a loop.
    """
    calculator = Calculator()
    while True:
        try:
            expression = input("Enter a mathematical expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
