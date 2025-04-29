class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, and division operations with proper operator precedence 
    and parentheses. It accepts both integers and floating-point numbers (including
    negative values) and validates the input strictly.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression is malformed, contains invalid characters,
                        or has unbalanced parentheses.
            ZeroDivisionError: If division by zero is encountered.
        """
        normalized_expr = self._normalize_expression(expression)

        if not self._is_balanced(normalized_expr):
            raise ValueError("Unbalanced parentheses in expression.")

        tokens = self._tokenize(normalized_expr)
        postfix_tokens = self._to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the mathematical expression by removing spaces and validating
        that only allowed characters are present.

        Args:
            expression (str): The raw expression to normalize.

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
        Checks if the expression has properly paired parentheses.

        Args:
            expression (str): The expression to check.

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
        Tokenizes the expression into numbers and operators.

        This function supports negative numbers by treating a '-' as a unary
        negative sign when it occurs at the start of the expression or immediately
        after an opening parenthesis or another operator.

        Args:
            expression (str): The normalized mathematical expression.

        Returns:
            list: A list of tokens where numbers are floats and operators/parentheses
                  are represented as strings.

        Raises:
            ValueError: If an invalid number format or character misuse is detected.
        """
        tokens = []
        idx = 0
        n = len(expression)

        while idx < n:
            ch = expression[idx]
            # Check for start of a number or unary minus
            if ch.isdigit() or ch == '.' or (ch == '-' and (idx == 0 or expression[idx - 1] in "(+-*/")):
                num_str = ""
                # If the current '-' is a unary operator, include it in the number
                if ch == '-' and (idx == 0 or expression[idx - 1] in "(+-*/"):
                    num_str += ch
                    idx += 1
                    if idx >= n or (not expression[idx].isdigit() and expression[idx] != '.'):
                        raise ValueError("Invalid use of '-' sign.")
                # Process the numeric part (integer and fractional part)
                decimal_found = '.' in num_str
                while idx < n and (expression[idx].isdigit() or (expression[idx] == '.' and not decimal_found)):
                    if expression[idx] == '.':
                        decimal_found = True
                    num_str += expression[idx]
                    idx += 1
                try:
                    number = float(num_str)
                except ValueError:
                    raise ValueError(f"Invalid number format: {num_str}")
                tokens.append(number)
            elif ch in "+-*/()":
                tokens.append(ch)
                idx += 1
            else:
                raise ValueError(f"Unexpected character '{ch}' encountered in expression.")
        return tokens

    def _to_postfix(self, tokens: list) -> list:
        """
        Converts the list of tokens from infix notation to postfix notation using
        the Shunting-yard algorithm. This ensures proper operator precedence.

        Args:
            tokens (list): A list of tokens (numbers and operators) in infix order.

        Returns:
            list: A list of tokens arranged in postfix (Reverse Polish Notation) order.

        Raises:
            ValueError: If mismatched parentheses are detected.
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
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop()  # Remove the '(' from the stack
            else:
                raise ValueError("Invalid token encountered.")
        
        while operator_stack:
            if operator_stack[-1] in "()":
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(operator_stack.pop())

        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates the postfix expression (Reverse Polish Notation) and returns
        the computed result.

        Args:
            tokens (list): The list of tokens in postfix order.

        Returns:
            float: The result of the evaluation.

        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: If the postfix expression is malformed.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in "+-*/":
                if len(stack) < 2:
                    raise ValueError("Insufficient values for operation.")
                right = stack.pop()
                left = stack.pop()
                if token == '+':
                    stack.append(left + right)
                elif token == '-':
                    stack.append(left - right)
                elif token == '*':
                    stack.append(left * right)
                elif token == '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero.")
                    stack.append(left / right)
            else:
                raise ValueError("Invalid token in postfix expression.")
        
        if len(stack) != 1:
            raise ValueError("Malformed expression.")
        return stack[0]


if __name__ == "__main__":
    import sys

    def main():
        """
        Runs the console-based arithmetic calculator. It repeatedly reads
        expressions from the user and prints their evaluated results. Entering
        'exit' or 'quit' terminates the program.
        """
        calculator = Calculator()
        print("Console-based Arithmetic Calculator")
        print("Supported operations: +, -, *, / with proper precedence and parentheses.")
        print("Enter 'exit' or 'quit' to terminate the calculator.")

        while True:
            try:
                expression = input("Enter expression: ")
                if expression.strip().lower() in {"exit", "quit"}:
                    print("Exiting calculator. Goodbye!")
                    break
                result = calculator.calculate(expression)
                print("Result:", result)
            except Exception as e:
                print("Error:", e, file=sys.stderr)

    main()
