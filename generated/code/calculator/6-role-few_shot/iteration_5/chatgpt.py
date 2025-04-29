class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions including
    addition (+), subtraction (-), multiplication (*), division (/), and parentheses.
    It supports integers and floating-point numbers (including negatives) with proper
    operator precedence and validation.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression contains invalid characters or mismatched parentheses.
            ZeroDivisionError: If a division by zero occurs during evaluation.
        """
        # Normalize the expression (remove spaces and validate characters)
        normalized_expr = self._normalize_expression(expression)
        # Validate that parentheses are properly balanced
        if not self._is_balanced(normalized_expr):
            raise ValueError("Unbalanced parentheses in the expression.")

        # Tokenize the expression into numbers and operators
        tokens = self._tokenize(normalized_expr)
        # Convert the list of tokens to Reverse Polish Notation (RPN) using the shunting yard algorithm
        rpn = self._to_rpn(tokens)
        # Evaluate the RPN expression to compute the result
        result = self._evaluate_rpn(rpn)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression by removing spaces and validating allowed characters.

        Args:
            expression (str): The raw arithmetic expression.

        Returns:
            str: The normalized expression with spaces removed.

        Raises:
            ValueError: If an invalid character is encountered.
        """
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")
        # Remove spaces before further processing
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if parentheses in the expression are properly balanced.

        Args:
            expression (str): The arithmetic expression.

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
        return not stack

    def _tokenize(self, expression: str) -> list:
        """
        Converts the normalized expression string into a list of tokens.

        Tokens may be numbers (as strings) or operators/parentheses.
        Handles negative numbers by checking the context of '-' signs.

        Args:
            expression (str): The normalized arithmetic expression.

        Returns:
            list: A list of tokens.
        """
        tokens = []
        i = 0
        length = len(expression)

        while i < length:
            char = expression[i]
            if char.isdigit() or char == '.':
                # Process a numeric literal (integer or float)
                num_str = ""
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                tokens.append(num_str)
            elif char in "+-*/()":
                if char == '-' and (i == 0 or expression[i - 1] in "(+-*/"):
                    # Handle potential unary minus
                    # If the next character starts a number, combine it as a negative number token.
                    if i + 1 < length and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                        num_str = "-"
                        i += 1
                        while i < length and (expression[i].isdigit() or expression[i] == '.'):
                            num_str += expression[i]
                            i += 1
                        tokens.append(num_str)
                        continue
                    # If a '-' is followed by '(' (e.g., "-(2+3)"), insert an explicit "0" to represent unary minus.
                    elif i + 1 < length and expression[i + 1] == '(':
                        tokens.append("0")
                        tokens.append("-")
                        i += 1
                        continue
                    else:
                        # Fall back to binary minus if nothing specific to combine.
                        tokens.append(char)
                        i += 1
                else:
                    tokens.append(char)
                    i += 1
            else:
                # Should not reach here due to normalization
                raise ValueError(f"Invalid character encountered: {char}")
        return tokens

    def _to_rpn(self, tokens: list) -> list:
        """
        Converts a list of tokens into Reverse Polish Notation (RPN) using the shunting yard algorithm.

        Args:
            tokens (list): The list of tokens representing the expression.

        Returns:
            list: The RPN (postfix) representation of the expression.

        Raises:
            ValueError: If there are mismatched parentheses.
        """
        output_queue = []
        operator_stack = []
        # Define operator precedences; all binary operators are left-associative.
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            # Try converting token to a float; if successful, it's a number.
            try:
                float(token)
                output_queue.append(token)
            except ValueError:
                if token in precedence:
                    # Process operator token: pop operators with higher or equal precedence
                    while operator_stack and operator_stack[-1] in precedence and \
                          precedence[operator_stack[-1]] >= precedence[token]:
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(token)
                elif token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    # Pop operators until a matching '(' is found.
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    if not operator_stack:
                        raise ValueError("Mismatched parentheses.")
                    operator_stack.pop()  # Remove the '(' from the stack
                else:
                    # Should not occur because of previous validations.
                    raise ValueError(f"Unknown token: {token}")

        # Pop any remaining operators in the stack.
        while operator_stack:
            top = operator_stack.pop()
            if top in ('(', ')'):
                raise ValueError("Mismatched parentheses.")
            output_queue.append(top)
        return output_queue

    def _evaluate_rpn(self, tokens: list) -> float:
        """
        Evaluates an expression in Reverse Polish Notation (RPN).

        Args:
            tokens (list): The RPN expression as a list of tokens.

        Returns:
            float: The result of the evaluation.

        Raises:
            ZeroDivisionError: If a division by zero occurs.
            ValueError: If the RPN expression is invalid.
        """
        stack = []
        for token in tokens:
            try:
                # If token represents a number, push onto the stack.
                value = float(token)
                stack.append(value)
            except ValueError:
                # Otherwise, the token must be an operator; pop two numbers.
                if len(stack) < 2:
                    raise ValueError("Invalid expression.")
                right = stack.pop()
                left = stack.pop()
                if token == '+':
                    result = left + right
                elif token == '-':
                    result = left - right
                elif token == '*':
                    result = left * right
                elif token == '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero.")
                    result = left / right
                else:
                    raise ValueError(f"Unknown operator: {token}")
                stack.append(result)
        if len(stack) != 1:
            raise ValueError("Invalid expression.")
        return stack[0]


if __name__ == '__main__':
    # Create an instance of Calculator
    calc = Calculator()
    print("Console-Based Arithmetic Calculator")
    print("Enter an arithmetic expression (or type 'quit' to exit).")
    while True:
        try:
            user_input = input(">> ")
            if user_input.strip().lower() == 'quit':
                print("Exiting the calculator.")
                break
            # Compute and display the result
            result = calc.calculate(user_input)
            print("Result:", result)
        except Exception as error:
            # Catch and display any errors (e.g., invalid expression, division by zero)
            print("Error:", error)
