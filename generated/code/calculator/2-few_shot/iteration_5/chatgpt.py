class Calculator:
    """
    A console-based arithmetic calculator that evaluates mathematical expressions.
    
    Supported operations:
      - Addition (+)
      - Subtraction (-)
      - Multiplication (*)
      - Division (/)
      - Parentheses for grouping

    It supports both integers and floating-point numbers (including negative values).
    The algorithm ensures correct operator precedence without using eval() or similar shortcuts.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns its result as a float.

        Args:
            expression (str): A mathematical expression using numbers, operators, and parentheses.

        Returns:
            float: The result of evaluating the expression.

        Raises:
            ValueError: If the expression contains invalid characters or unbalanced parentheses.
            ZeroDivisionError: If the expression results in a division by zero.
        """
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("Expression contains unbalanced parentheses.")
        tokens = self._tokenize(normalized_expr)
        rpn = self._shunting_yard(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.

        Args:
            expression (str): A mathematical expression.

        Returns:
            str: A normalized expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Allowed characters include digits, operators, parentheses, and the decimal point.
        allowed_chars = set("0123456789+-*/().")
        for char in expression:
            if char not in allowed_chars and not char.isspace():
                raise ValueError(f"Invalid character detected: '{char}'")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if the given expression has properly paired parentheses.

        Args:
            expression (str): The mathematical expression as a string.

        Returns:
            bool: True if parentheses are balanced; False otherwise.
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
        Converts an expression string into a list of tokens (numbers and operators).

        This tokenizer handles:
          - Integers and floats.
          - Negative numbers (when '-' appears as a unary operator).
          - Operators and parentheses.

        Args:
            expression (str): A normalized mathematical expression.

        Returns:
            list: A list of tokens where numbers are of type float and operators/parentheses are strings.

        Raises:
            ValueError: If an invalid number format is encountered.
        """
        tokens = []
        i = 0
        n = len(expression)
        while i < n:
            char = expression[i]

            # Handle numbers (including negative numbers indicated by a unary '+' or '-')
            if char.isdigit() or char == '.' or (char in '+-' and (
                    i == 0 or expression[i - 1] in "(+*/-") and (i + 1 < n and (expression[i + 1].isdigit() or expression[i + 1] == '.'))):

                num_str = char
                i += 1

                # Collect subsequent digits and decimal points
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1

                try:
                    # Convert numeric string to float.
                    number = float(num_str)
                except ValueError:
                    raise ValueError(f"Invalid number format: {num_str}")
                tokens.append(number)
            # Handle operators: +, -, *, /
            elif char in "+-*/":
                tokens.append(char)
                i += 1
            # Handle parentheses: ( and )
            elif char in "()":
                tokens.append(char)
                i += 1
            else:
                # This should never happen due to normalization, but safeguards just in case.
                raise ValueError(f"Unexpected character encountered: '{char}'")
        return tokens

    def _shunting_yard(self, tokens: list) -> list:
        """
        Converts a list of tokens from infix notation to Reverse Polish Notation (RPN)
        using the Shunting Yard algorithm.

        Args:
            tokens (list): A list of tokens from _tokenize.

        Returns:
            list: A list of tokens in RPN.

        Raises:
            ValueError: If unbalanced parentheses are detected.
        """
        output_queue = []
        operator_stack = []
        # Operator precedence mapping.
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in precedence:
                # Pop operators from the stack with greater or equal precedence.
                while (operator_stack and operator_stack[-1] in precedence and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                # Pop from the stack to the output queue until a left parenthesis is encountered.
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop()  # Remove the '('
            else:
                raise ValueError(f"Invalid token encountered: {token}")

        # Drain any remaining operators from the stack.
        while operator_stack:
            op = operator_stack.pop()
            if op in '()':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)
        return output_queue

    def _evaluate_rpn(self, tokens: list) -> float:
        """
        Evaluates the expression in Reverse Polish Notation.

        Args:
            tokens (list): A list of tokens in RPN.

        Returns:
            float: The result of the expression.

        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ValueError: If the RPN expression is malformed.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in "+-*/":
                if len(stack) < 2:
                    raise ValueError("Malformed expression; insufficient operands.")
                b = stack.pop()
                a = stack.pop()
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
                raise ValueError(f"Invalid token encountered during evaluation: {token}")

        if len(stack) != 1:
            raise ValueError("Malformed expression; extra operands remain.")
        return stack[0]


def main():
    """
    Runs a console-based loop allowing the user to input arithmetic expressions
    and see their evaluations. The loop will terminate when the user inputs 'exit'.
    """
    calc = Calculator()
    print("Welcome to the console-based arithmetic calculator!")
    print("Enter 'exit' to quit.\n")
    
    while True:
        try:
            expr = input("Enter expression: ").strip()
            if expr.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            result = calc.calculate(expr)
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
