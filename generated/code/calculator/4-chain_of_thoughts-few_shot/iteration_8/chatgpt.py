class Calculator:
    """
    A console-based arithmetic calculator supporting addition, subtraction,
    multiplication, division, and parentheses for grouping. The calculator
    accepts integers or decimal numbers (including negative numbers) and
    validates the expression based on ISO/IEC 25010 quality requirements.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result as a float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the expression.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, or an invalid number format.
            ZeroDivisionError: If there is an attempt to divide by zero.
        """
        # Normalize and validate expression
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("Unbalanced parentheses in expression.")

        # Tokenize the expression into numbers and operators
        tokens = self._tokenize(normalized_expr)

        # Convert infix tokens to postfix (Reverse Polish Notation) for evaluation
        postfix_tokens = self._infix_to_postfix(tokens)

        # Evaluate the postfix expression and return the result
        return self._evaluate_postfix(postfix_tokens)

    def _normalize_expression(self, expression: str) -> str:
        """
        Removes whitespace and validates characters in the expression.

        Args:
            expression (str): The input arithmetic expression.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().")
        for char in expression:
            if char not in allowed_chars and not char.isspace():
                raise ValueError("Expression contains invalid characters.")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether the expression has properly paired parentheses.

        Args:
            expression (str): The arithmetic expression.

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

    def _tokenize(self, expression: str) -> list:
        """
        Splits the arithmetic expression into tokens (numbers and operators).

        Args:
            expression (str): The normalized expression.

        Returns:
            list: List of tokens where numbers are of type float and operators are str.

        Raises:
            ValueError: If a number is formatted incorrectly (e.g., multiple decimal points).
        """
        tokens = []
        i = 0
        length = len(expression)
        while i < length:
            char = expression[i]
            # Parse numbers (including decimals). A number may also be prefixed by a unary minus.
            if char.isdigit() or char == '.':
                number_str = ""
                dot_count = 0
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid number format: multiple decimal points.")
                    number_str += expression[i]
                    i += 1
                try:
                    number = float(number_str)
                except ValueError:
                    raise ValueError(f"Invalid number format: {number_str}")
                tokens.append(number)
            # Handle potential unary minus for negative numbers
            elif char in "+-":
                # Determine if '-' is acting as a unary minus.
                # It is considered unary if it is at the start of the expression or
                # if the previous character is an operator or an opening parenthesis.
                if char == '-' and (i == 0 or expression[i - 1] in "(+-*/"):
                    # Check if the '-' is immediately followed by a digit or a dot
                    if i + 1 < length and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                        i += 1
                        number_str = "-"  # start with negative sign
                        dot_count = 0
                        while i < length and (expression[i].isdigit() or expression[i] == '.'):
                            if expression[i] == '.':
                                dot_count += 1
                                if dot_count > 1:
                                    raise ValueError("Invalid number format: multiple decimal points.")
                            number_str += expression[i]
                            i += 1
                        try:
                            number = float(number_str)
                        except ValueError:
                            raise ValueError(f"Invalid number format: {number_str}")
                        tokens.append(number)
                        continue
                    else:
                        # Treat as a binary operator if not followed by a number (edge case)
                        tokens.append(char)
                        i += 1
                else:
                    tokens.append(char)
                    i += 1
            elif char in "*/()":
                tokens.append(char)
                i += 1
            else:
                # This should not occur because of prior normalization.
                raise ValueError(f"Invalid character encountered: {char}")
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts a list of tokens from infix notation to postfix notation
        using the Shunting-Yard algorithm.

        Args:
            tokens (list): The tokenized arithmetic expression.

        Returns:
            list: The postfix (RPN) token list.

        Raises:
            ValueError: If there are mismatched parentheses.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in precedence:
                while (operator_stack and operator_stack[-1] in precedence and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValueError("Unbalanced parentheses in expression.")
                operator_stack.pop()  # Remove the '(' from the stack
            else:
                raise ValueError(f"Invalid token encountered during conversion: {token}")

        while operator_stack:
            op = operator_stack.pop()
            if op in '()':
                raise ValueError("Unbalanced parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix (Reverse Polish Notation) expression.

        Args:
            tokens (list): The postfix token list.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid.
            ZeroDivisionError: If there is an attempt to divide by zero.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in {'+', '-', '*', '/'}:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient values.")
                b = stack.pop()
                a = stack.pop()
                result = None
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero encountered.")
                    result = a / b
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in evaluation: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression: too many values.")
        return stack[0]


if __name__ == '__main__':
    import sys

    def main():
        """
        Main loop for the console-based arithmetic calculator.
        Users can input an arithmetic expression to evaluate or type 'exit' to quit.
        """
        calc = Calculator()
        print("Console-based Arithmetic Calculator")
        print("Enter an arithmetic expression to evaluate or type 'exit' to quit.")
        while True:
            try:
                expression = input("Expression > ")
            except (EOFError, KeyboardInterrupt):
                print("\nExiting calculator.")
                break

            if expression.strip().lower() == 'exit':
                print("Exiting calculator.")
                break

            try:
                result = calc.calculate(expression)
                print("Result:", result)
            except (ValueError, ZeroDivisionError) as e:
                print("Error:", e, file=sys.stderr)

    main()
