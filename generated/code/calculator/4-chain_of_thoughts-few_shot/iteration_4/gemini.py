import re  # Used for more robust tokenization


class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions.

    This calculator supports addition (+), subtraction (-), multiplication (*),
    and division (/), as well as parentheses. It handles operator precedence
    and provides error handling for invalid input.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the expression.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, division by zero).
        """
        try:
            normalized_expression = self._normalize_expression(expression)
            if not self._is_balanced(normalized_expression):
                raise ValueError("Unbalanced parentheses.")

            tokens = self._tokenize(normalized_expression)
            postfix_tokens = self._shunting_yard(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except ValueError as e:
            raise e  # Re-raise ValueErrors for consistent error handling
        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {e}")

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

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if the parentheses in the expression are balanced.

        Args:
            expression (str): The expression to check.

        Returns:
            bool: True if balanced, False otherwise.
        """
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        return not stack  # Stack should be empty if balanced


    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the expression into a list of numbers, operators, and parentheses.

        Args:
            expression (str): The normalized expression.

        Returns:
            list: A list of tokens.
        
        Raises:
            ValueError: If token is invalid.
        """
        # Use regular expression to handle numbers(integers and decimals, also negative numbers), operators, and parentheses
        tokens = re.findall(r'-?\d+\.?\d*|\+|-|\*|/|\(|\)', expression)
        for token in tokens:
            if not re.match(r'^-?\d+\.?\d*$|^\+$|^-$|^\*$|^/$|^\($|^\)$', token):
                raise ValueError(f"Invalid token found: {token}")
        return tokens

    def _shunting_yard(self, tokens: list) -> list:
        """
        Converts the infix expression (tokens) to postfix notation using the
        Shunting Yard Algorithm.

        Args:
            tokens (list): The list of tokens in infix notation.

        Returns:
            list: The list of tokens in postfix notation.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        operator_stack = []

        for token in tokens:
            if re.match(r'^-?\d+\.?\d*$', token):  # If it's a number
                output_queue.append(float(token))
            elif token in precedence:  # If it's an operator
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Pop the '('

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())

        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            tokens (list): The list of tokens in postfix notation.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If division by zero is attempted.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            else:  # It's an operator
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
          raise ValueError("Invalid Expression: Incorrect number of operators or operands")
        return stack[0]

if __name__ == "__main__":
    calculator = Calculator()

    # Valid expressions
    print(calculator.calculate("2 + 3 * 4"))  # Output: 14.0
    print(calculator.calculate("(2 + 3) * 4")) # Output: 20.0
    print(calculator.calculate("-5 + 10 / 2"))  # Output: 0.0
    print(calculator.calculate("10 / (2 + 3)"))  # Output: 2.0
    print(calculator.calculate("1.5 * 2 + 3"))  # Output: 6.0
    print(calculator.calculate("-1.5 * -2 + 3")) # Output: 6.0

    # Invalid expressions (should raise ValueErrors)
    try:
        print(calculator.calculate("2 + (3 * 4"))  # Unbalanced parentheses
    except ValueError as e:
        print(e)

    try:
        print(calculator.calculate("2 + + 3"))  # Invalid expression
    except ValueError as e:
        print(e)

    try:
        print(calculator.calculate("10 / 0"))  # Division by zero
    except ValueError as e:
        print(e)
        
    try:
        print(calculator.calculate("2 & 3")) # Invalid character
    except ValueError as e:
        print(e)

    try:
        print(calculator.calculate("2 + 3 4")) # Invalid token
    except ValueError as e:
        print(e)    
