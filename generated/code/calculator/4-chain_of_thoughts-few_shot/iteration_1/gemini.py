class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions.
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
            TypeError: If the input expression is not a string.
        """
        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        normalized_expression = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expression):
            raise ValueError("Unbalanced parentheses.")

        return self._evaluate_expression(normalized_expression)

    # --- Helper Methods (to be implemented in subsequent steps) ---

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression (removes spaces, validates characters).
        See Example 2 in the prompt.
        """
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")
    
    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if parentheses are balanced.  See Example 3.
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

    def _evaluate_expression(self, expression: str) -> float:
        """
        Evaluates the normalized expression (no spaces, valid characters, balanced parentheses).
        This is where the core logic resides.
        """
        tokens = self._tokenize(expression)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result
    
    def _tokenize(self, expression: str) -> list:
        """
        Converts the expression string into a list of tokens (numbers, operators, parentheses).
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
                if char in "+-*/()":
                    tokens.append(char)
                elif char != " ":  # Should have been removed by normalize, but extra safety
                    raise ValueError(f"Unexpected character: {char}")
        if current_number:
            tokens.append(current_number)
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts infix notation to postfix notation (Reverse Polish Notation) using the Shunting Yard algorithm.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit():  # Check if it's a number (handle decimals and negatives)
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
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            else:
                raise ValueError(f"Invalid token: {token}")

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression.
        """
        stack = []
        for token in tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit():
                stack.append(float(token))
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
                else:
                    raise ValueError(f"Invalid operator: {token}")  #Should not happen, but included for safety
        if len(stack) != 1:
            raise ValueError("Invalid Expression")
            
        return stack[0]


class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions.
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
            TypeError: If the input expression is not a string.
        """
        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        normalized_expression = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expression):
            raise ValueError("Unbalanced parentheses.")

        return self._evaluate_expression(normalized_expression)

    # --- Helper Methods ---

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression (removes spaces, validates characters).
        """
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if parentheses are balanced.
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

    def _evaluate_expression(self, expression: str) -> float:
        """
        Evaluates the normalized expression.
        """
        tokens = self._tokenize(expression)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _tokenize(self, expression: str) -> list:
        """
        Converts the expression string into a list of tokens.
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
                if char in "+-*/()":
                    tokens.append(char)
                elif char != " ":
                    raise ValueError(f"Unexpected character: {char}")
        if current_number:
            tokens.append(current_number)
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts infix notation to postfix notation (Shunting Yard algorithm).
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit():
                output.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            else:
                raise ValueError(f"Invalid token: {token}")

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression.
        """
        stack = []
        for token in tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit():
                stack.append(float(token))
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
                else:
                    raise ValueError(f"Invalid operator: {token}")
        if len(stack) != 1:
            raise ValueError("Invalid Expression")

        return stack[0]

# Example Usage (and basic testing):
if __name__ == "__main__":
    calculator = Calculator()

    test_cases = [
      ("2 + 2", 4.0),
      ("10 - 5", 5.0),
      ("3 * 4", 12.0),
      ("20 / 5", 4.0),
      ("2 + 3 * 4", 14.0),
      ("(2 + 3) * 4", 20.0),
      ("10 / (2 + 3)", 2.0),
      ("1 + 2 * (3 + 4) / 2 - 1", 7.0),
      ("-5 + 3", -2.0),
      ("1.5 * 2", 3.0),
      ("5 / 2", 2.5),
      ("(1 + 2) * (3 + 4)", 21.0),
        ("-(2)", -2.0),
    ("5 * -2.2", -11.0)

    ]

    for expression, expected in test_cases:
        try:
            result = calculator.calculate(expression)
            print(f"Expression: {expression}, Result: {result}, Expected: {expected}, Pass: {result == expected}")
            assert result == expected, f"Test failed for {expression}: expected {expected}, got {result}"  # add simple assertions

        except ValueError as e:
            print(f"Expression: {expression}, Error: {e}, Expected: {expected}, Pass: False") # Expected to fail.

    # Test error cases:

    error_cases = [
        "1 / 0",
        "2 + (3 * 4",
        "2 + )3 * 4(",
        "a + b",
        "2 ++ 3",
        "  ",
         22       
    ]

    for expression in error_cases:
        try:
            if isinstance(expression, str):
                calculator.calculate(expression)
                print(f"Test failed for {expression}: expected error, got result")  # Should not reach here
            else:
                calculator.calculate(expression)
        except (ValueError, TypeError) as e:
            print(f"Test passed for error case: Expression: '{expression}', Error: {e}")  # Expected behavior
        except Exception as e:
            print(f"Test failed. Expected ValueError or TypeError. Expression:'{expression}', Error received: {e}")

    print("All test cases finished.")
