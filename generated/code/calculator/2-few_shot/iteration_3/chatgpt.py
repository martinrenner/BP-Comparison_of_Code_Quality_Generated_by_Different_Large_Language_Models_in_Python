class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions.
    Supports addition (+), subtraction (-), multiplication (*), division (/),
    parentheses for grouping, and handles both integers and floating-point numbers,
    including negative values. The calculator implements proper operator precedence.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression and returns the result as a float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The computed result.

        Raises:
            ValueError: If the expression contains invalid characters,
                        unbalanced parentheses, or is otherwise malformed.
            ZeroDivisionError: If a division by zero is attempted.
        """
        normalized_expr = self._normalize(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("Unbalanced parentheses in the expression.")

        tokens = self._tokenize(normalized_expr)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _normalize(self, expression: str) -> str:
        """
        Normalizes the mathematical expression by removing spaces and validating its characters.

        Args:
            expression (str): A mathematical expression as a string.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether the parentheses in the expression are correctly paired.

        Args:
            expression (str): A normalized mathematical expression.

        Returns:
            bool: True if parentheses are balanced, otherwise False.
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
        Tokenizes the arithmetic expression into a list of numbers and operators.
        Supports detection of negative numbers (unary minus) when needed.

        Args:
            expression (str): A normalized mathematical expression.

        Returns:
            list: List of tokens (as strings) representing numbers and operators.

        Raises:
            ValueError: If an invalid token is encountered.
        """
        tokens = []
        i = 0
        length = len(expression)
        while i < length:
            char = expression[i]
            # If the character is a digit or a decimal point, parse the full number.
            if char.isdigit() or char == '.':
                num_str = ''
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                tokens.append(num_str)
            # Handle potential unary plus or minus.
            elif char in "+-":
                # Determine if this is a unary operator by checking the previous token.
                if (i == 0 or expression[i - 1] in "+-*/(") and (i + 1 < length and (expression[i + 1].isdigit() or expression[i + 1] == '.')):
                    sign = char
                    i += 1
                    num_str = sign
                    # Must be followed by a valid number.
                    if i < length and (expression[i].isdigit() or expression[i] == '.'):
                        while i < length and (expression[i].isdigit() or expression[i] == '.'):
                            num_str += expression[i]
                            i += 1
                        tokens.append(num_str)
                    else:
                        raise ValueError("Invalid syntax: sign not followed by a number.")
                else:
                    # Otherwise, it is a binary operator.
                    tokens.append(char)
                    i += 1
            elif char in "*/()":
                tokens.append(char)
                i += 1
            else:
                # This clause should not be reached because of prior normalization.
                raise ValueError(f"Invalid token: {char}")
        return tokens

    def _to_rpn(self, tokens: list) -> list:
        """
        Converts a list of tokens in infix notation to Reverse Polish Notation (RPN)
        using the Shunting Yard algorithm.

        Args:
            tokens (list): List of tokens in infix order.

        Returns:
            list: List of tokens in RPN order.

        Raises:
            ValueError: If the parentheses are mismatched.
        """
        output = []
        op_stack = []
        # Define operator precedence.
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            # If token is a number, add it to the output.
            try:
                float(token)
                output.append(token)
                continue
            except ValueError:
                pass

            if token in precedence:
                while op_stack and op_stack[-1] in precedence and precedence[op_stack[-1]] >= precedence[token]:
                    output.append(op_stack.pop())
                op_stack.append(token)
            elif token == '(':
                op_stack.append(token)
            elif token == ')':
                found_left_paren = False
                while op_stack:
                    top = op_stack.pop()
                    if top == '(':
                        found_left_paren = True
                        break
                    else:
                        output.append(top)
                if not found_left_paren:
                    raise ValueError("Unbalanced parentheses in the expression.")
            else:
                raise ValueError(f"Invalid token encountered: {token}")

        while op_stack:
            top = op_stack.pop()
            if top in "()":
                raise ValueError("Unbalanced parentheses in the expression.")
            output.append(top)
        return output

    def _evaluate_rpn(self, tokens: list) -> float:
        """
        Evaluates an expression in Reverse Polish Notation (RPN).

        Args:
            tokens (list): List of tokens in RPN order.

        Returns:
            float: The evaluation result.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: If the RPN expression is invalid.
        """
        stack = []
        for token in tokens:
            try:
                # Attempt to parse the token as a number and push it onto the stack.
                number = float(token)
                stack.append(number)
            except ValueError:
                # Token is assumed to be an operator.
                if len(stack) < 2:
                    raise ValueError("Invalid expression.")
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
                        raise ZeroDivisionError("Division by zero.")
                    stack.append(a / b)
                else:
                    raise ValueError(f"Unknown operator: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression.")
        return stack[0]


if __name__ == "__main__":
    calculator = Calculator()
    print("Console-based Arithmetic Calculator")
    print("Supported operations: +, -, *, /")
    print("You can use parentheses for grouping. Enter 'quit' to exit.")
    
    while True:
        user_input = input("Enter expression: ")
        if user_input.lower() == "quit":
            break
        try:
            result = calculator.calculate(user_input)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
