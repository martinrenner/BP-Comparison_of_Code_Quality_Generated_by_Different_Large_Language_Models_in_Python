class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses while respecting the proper order
    of operations. It accepts integers, decimals, and negative numbers and performs
    input validation to ensure safe and correct operation according to ISO/IEC 25010.
    """

    def __init__(self) -> None:
        # Define operator precedence: multiplication/division > addition/subtraction.
        self._precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression provided as a string and returns the result.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, or if the format is incorrect.
            ZeroDivisionError: If a division by zero occurs.
        """
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("Expression has unbalanced parentheses.")

        tokens = self._tokenize(normalized_expr)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Removes whitespace from the expression and validates that only allowed characters exist.

        Args:
            expression (str): The raw arithmetic expression.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains any invalid character.
        """
        allowed_chars = set("0123456789+-*/(). ")
        for char in expression:
            if char not in allowed_chars:
                raise ValueError(f"Expression contains invalid character: '{char}'")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if the parentheses in the expression are balanced.

        Args:
            expression (str): The normalized arithmetic expression.

        Returns:
            bool: True if the parentheses are balanced, otherwise False.
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
        Converts the normalized expression into a list of tokens (numbers, operators, or parentheses).

        Args:
            expression (str): The normalized arithmetic expression.

        Returns:
            list: A list of tokens where numeric tokens are floats and operator/parenthesis tokens are strings.

        Raises:
            ValueError: If a number cannot be correctly parsed.
        """
        tokens = []
        i = 0
        length = len(expression)

        while i < length:
            char = expression[i]

            # Process numbers: digits or decimal point.
            if char.isdigit() or char == '.':
                num_str = char
                i += 1
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                try:
                    tokens.append(float(num_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: {num_str}")
                continue

            # Handle potential unary plus/minus.
            if char in "+-":
                # Determine if this is a unary operator:
                # It is unary if at the start or following an operator or '('.
                if i == 0 or expression[i - 1] in "(-+*/":
                    if i + 1 < length and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                        num_str = char
                        i += 1
                        while i < length and (expression[i].isdigit() or expression[i] == '.'):
                            num_str += expression[i]
                            i += 1
                        try:
                            tokens.append(float(num_str))
                        except ValueError:
                            raise ValueError(f"Invalid number format: {num_str}")
                        continue
                # Otherwise, it's a binary operator.
                tokens.append(char)
                i += 1
                continue

            # Process other operators and parentheses.
            if char in "*/()":
                tokens.append(char)
                i += 1
                continue

            # Should not reach here because expression is prevalidated.
            raise ValueError(f"Unexpected character encountered during tokenization: '{char}'")

        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts the list of tokens from infix notation to postfix (Reverse Polish Notation)
        using the Shunting Yard algorithm.

        Args:
            tokens (list): The list of tokens in infix order.

        Returns:
            list: The list of tokens in postfix order.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in self._precedence:
                while (operator_stack and operator_stack[-1] != '(' and 
                       operator_stack[-1] in self._precedence and
                       self._precedence[operator_stack[-1]] >= self._precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Mismatched parentheses.")
                operator_stack.pop()  # Remove '(' from the stack.
            else:
                # This branch should not be reached.
                raise ValueError(f"Unknown token encountered: {token}")

        # Pop any remaining operators from the stack.
        while operator_stack:
            top_token = operator_stack.pop()
            if top_token in "()":
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(top_token)

        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates the arithmetic expression given in postfix (Reverse Polish Notation).

        Args:
            tokens (list): The list of tokens in postfix order.

        Returns:
            float: The final evaluation result.

        Raises:
            ZeroDivisionError: If a division by zero is encountered.
            ValueError: If the expression is invalid.
        """
        stack = []

        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in self._precedence:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient values for operation.")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero encountered in expression.")
                    stack.append(a / b)
            else:
                raise ValueError(f"Invalid token in postfix evaluation: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression: leftover values after evaluation.")

        return stack[0]


if __name__ == '__main__':
    """
    Console-based interface to the arithmetic calculator.
    Users can input arithmetic expressions to be evaluated.
    Type 'exit' to terminate the program.
    """
    calc = Calculator()
    print("Arithmetic Calculator")
    print("Enter an arithmetic expression to evaluate or type 'exit' to quit.")

    while True:
        try:
            user_input = input("Expression: ")
            if user_input.strip().lower() == 'exit':
                break
            result = calc.calculate(user_input)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
