class Calculator:
    """
    A console-based arithmetic calculator that supports addition (+), subtraction (-),
    multiplication (*), division (/), and parentheses for grouping. It correctly handles
    operator precedence, as well as integer and floating-point numbers (including negative values).

    The evaluation is performed in three main steps:
      1. Normalization and validation of the input expression.
      2. Conversion of the expression into tokens and then to Reverse Polish Notation (RPN)
         using the shunting-yard algorithm.
      3. Evaluation of the RPN expression.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the computed result.

        Args:
            expression (str): A string representing the arithmetic expression, e.g., "3 + 4*(2-1)".

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression contains invalid characters, has unbalanced parentheses,
                        or is malformed.
            ZeroDivisionError: If a division by zero occurs.
        """
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("Unbalanced parentheses in expression")
        tokens = self._tokenize(normalized_expr)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the input expression by removing whitespace and ensuring that the
        expression contains only allowed characters.

        Args:
            expression (str): The original arithmetic expression.

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
        Checks if the provided expression has properly paired and balanced parentheses.

        Args:
            expression (str): The arithmetic expression.

        Returns:
            bool: True if the parentheses are balanced; otherwise, False.
        """
        stack = []
        for char in expression:
            if char == "(":
                stack.append(char)
            elif char == ")":
                if not stack:
                    return False
                stack.pop()
        return not stack

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the arithmetic expression into numbers and operator tokens.
        It also handles unary operators for negative (or positive) numbers.

        Args:
            expression (str): The normalized arithmetic expression.

        Returns:
            list: A list of tokens where numbers are of type float and operators/parentheses are str.

        Raises:
            ValueError: If an invalid token format is encountered.
        """
        tokens = []
        i = 0
        last_token_type = None  # Tracks the type of the last processed token: "number", "operator", or "(".
        length = len(expression)

        while i < length:
            char = expression[i]

            # Process numbers: integer or floating-point (including cases like "3.14")
            if char.isdigit() or char == ".":
                start = i
                dot_count = 0
                while i < length and (expression[i].isdigit() or expression[i] == "."):
                    if expression[i] == ".":
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid number format: multiple decimal points")
                    i += 1
                try:
                    number = float(expression[start:i])
                except ValueError:
                    raise ValueError("Invalid number format")
                tokens.append(number)
                last_token_type = "number"

            # Handle '+' or '-' which can be either unary or binary operators
            elif char in "+-":
                # Determine if operator is unary:
                if last_token_type in (None, "operator", "("):
                    # Unary operator detected.
                    sign = -1 if char == "-" else 1
                    i += 1
                    if i < length and (expression[i].isdigit() or expression[i] == "."):
                        start = i
                        dot_count = 0
                        while i < length and (expression[i].isdigit() or expression[i] == "."):
                            if expression[i] == ".":
                                dot_count += 1
                                if dot_count > 1:
                                    raise ValueError("Invalid number format: multiple decimal points")
                            i += 1
                        try:
                            number = float(expression[start:i])
                        except ValueError:
                            raise ValueError("Invalid number format after unary operator")
                        tokens.append(sign * number)
                        last_token_type = "number"
                    else:
                        raise ValueError("Invalid expression: unary operator not followed by a number")
                else:
                    # Binary operator.
                    tokens.append(char)
                    last_token_type = "operator"
                    i += 1

            # Process multiplication and division operators.
            elif char in "*/":
                tokens.append(char)
                last_token_type = "operator"
                i += 1

            # Process left parenthesis.
            elif char == "(":
                tokens.append(char)
                last_token_type = "("
                i += 1

            # Process right parenthesis.
            elif char == ")":
                tokens.append(char)
                # After a closing parenthesis, we treat the subexpression as a complete number.
                last_token_type = "number"
                i += 1

            else:
                raise ValueError(f"Invalid character '{char}' in expression")

        return tokens

    def _to_rpn(self, tokens: list) -> list:
        """
        Converts the token list from infix notation to Reverse Polish Notation (RPN)
        using the shunting-yard algorithm.

        Args:
            tokens (list): A list of tokens (numbers and operators).

        Returns:
            list: A list of tokens arranged in RPN order.

        Raises:
            ValueError: If there is an issue with matched parentheses.
        """
        output_queue = []
        operator_stack = []
        precedence = {"+": 1, "-": 1, "*": 2, "/": 2}

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in precedence:
                while (
                    operator_stack
                    and operator_stack[-1] in precedence
                    and precedence[operator_stack[-1]] >= precedence[token]
                ):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == "(":
                operator_stack.append(token)
            elif token == ")":
                while operator_stack and operator_stack[-1] != "(":
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Unbalanced parentheses in expression")
                operator_stack.pop()  # Remove the '(' from the stack.
            else:
                raise ValueError("Unknown token encountered")

        # Pop any remaining operators from the stack.
        while operator_stack:
            op = operator_stack.pop()
            if op == "(" or op == ")":
                raise ValueError("Unbalanced parentheses in expression")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, tokens: list) -> float:
        """
        Evaluates an arithmetic expression provided in Reverse Polish Notation (RPN).

        Args:
            tokens (list): A list of tokens in RPN order.

        Returns:
            float: The calculated result of the RPN expression.

        Raises:
            ValueError: If the RPN expression is invalid.
            ZeroDivisionError: If a division by zero occurs.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in ("+", "-", "*", "/"):
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient values for operation")
                # Note: For binary operators, the order matters.
                right = stack.pop()
                left = stack.pop()
                if token == "+":
                    stack.append(left + right)
                elif token == "-":
                    stack.append(left - right)
                elif token == "*":
                    stack.append(left * right)
                elif token == "/":
                    if right == 0:
                        raise ZeroDivisionError("Division by zero encountered in expression")
                    stack.append(left / right)
            else:
                raise ValueError("Invalid token in RPN expression")

        if len(stack) != 1:
            raise ValueError("Invalid expression: too many values remaining after evaluation")

        return stack[0]


if __name__ == "__main__":
    # Console-based interactive loop for the calculator.
    calc = Calculator()
    print("Arithmetic Calculator")
    print("Enter an arithmetic expression to evaluate or type 'exit' to quit.")

    while True:
        try:
            user_input = input("Expression > ").strip()
            if user_input.lower() in {"exit", "quit"}:
                break
            result = calc.calculate(user_input)
            print("Result:", result)
        except Exception as error:
            print("Error:", error)
