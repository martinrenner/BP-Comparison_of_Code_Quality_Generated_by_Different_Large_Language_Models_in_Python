class Calculator:
    """
    A console-based arithmetic calculator that supports basic arithmetic operations,
    parentheses, and both integer and decimal numbers (including negative numbers).

    Supported operations:
      - Addition (+)
      - Subtraction (-)
      - Multiplication (*)
      - Division (/)

    This class implements the functionality using an object-oriented approach.
    The main public method is calculate(expression: str) -> float.
    """

    def __init__(self):
        # Define operator precedence; all operators here are left-associative.
        self.operators = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
        }

    def calculate(self, expression: str) -> float:
        """
        Evaluate the arithmetic expression provided as a string.

        Args:
            expression (str): A string representing the arithmetic expression.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression contains invalid characters or has unbalanced parentheses.
            ZeroDivisionError: If a division by zero is attempted.
        """
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn)
        return result

    def _tokenize(self, expression: str) -> list:
        """
        Convert the input expression string into a list of tokens.

        Tokens include numbers (which may be decimals and/or negative),
        operators, and parentheses.

        Args:
            expression (str): The arithmetic expression as a string.

        Returns:
            list: A list of string tokens.

        Raises:
            ValueError: If an invalid character is encountered.
        """
        # Remove all whitespace for easier processing.
        expression = expression.replace(" ", "")
        tokens = []
        i = 0
        length = len(expression)

        while i < length:
            char = expression[i]

            # Handle parentheses directly.
            if char in '()':
                tokens.append(char)
                i += 1
                continue

            # Handle a potential unary plus or minus.
            if char in '+-':
                # Determine if this is a unary operator.
                # It is unary if it's at the start or if the previous token is an operator or "(".
                if (i == 0) or (expression[i - 1] in "(+-*/"):
                    # Look ahead to see if a number follows.
                    if i + 1 < length and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                        # It's a unary operator attached to a number.
                        num_str = char
                        i += 1
                        # Collect the digits and the decimal point.
                        while i < length and (expression[i].isdigit() or expression[i] == '.'):
                            num_str += expression[i]
                            i += 1
                        tokens.append(num_str)
                        continue
                    else:
                        # If no number follows, treat it as a binary operator.
                        tokens.append(char)
                        i += 1
                        continue

            # Handle numbers (integer or decimal).
            if char.isdigit() or char == '.':
                num_str = ""
                # Collect characters that form the number.
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                tokens.append(num_str)
                continue

            # Handle other binary operators.
            if char in self.operators or char in "*/":
                tokens.append(char)
                i += 1
                continue

            # If the character is not recognized, raise an error.
            raise ValueError(f"Invalid character encountered in expression: '{char}'")

        return tokens

    def _to_rpn(self, tokens: list) -> list:
        """
        Convert the list of tokens into Reverse Polish Notation (RPN)
        using the shunting-yard algorithm.

        Args:
            tokens (list): A list of tokens representing the arithmetic expression.

        Returns:
            list: A list of tokens in RPN order.

        Raises:
            ValueError: If there are unbalanced parentheses.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            # If token is a number, put it directly into the output queue.
            try:
                float(token)
                output_queue.append(token)
                continue
            except ValueError:
                pass  # Not a number; must be an operator or parenthesis.

            if token in self.operators:
                # Pop operators from the operator stack to the output queue
                # as long as they have higher or equal precedence.
                while operator_stack and operator_stack[-1] in self.operators and \
                        self.operators[operator_stack[-1]] >= self.operators[token]:
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == "(":
                operator_stack.append(token)
            elif token == ")":
                # Pop from the stack until a left parenthesis is encountered.
                while operator_stack and operator_stack[-1] != "(":
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != "(":
                    raise ValueError("Unbalanced parentheses in expression.")
                # Pop the left parenthesis.
                operator_stack.pop()
            else:
                raise ValueError(f"Unknown token encountered: {token}")

        # After processing all tokens, there should be no parentheses left.
        while operator_stack:
            top = operator_stack.pop()
            if top in '()':
                raise ValueError("Unbalanced parentheses in expression.")
            output_queue.append(top)

        return output_queue

    def _evaluate_rpn(self, rpn: list) -> float:
        """
        Evaluate the expression given in Reverse Polish Notation (RPN).

        Args:
            rpn (list): A list of tokens in RPN order.

        Returns:
            float: The numerical result of the expression.

        Raises:
            ValueError: If the expression is invalid.
            ZeroDivisionError: If a division by zero occurs.
        """
        stack = []

        for token in rpn:
            # Try interpreting the token as a number.
            try:
                value = float(token)
                stack.append(value)
                continue
            except ValueError:
                # Not a number, so it must be an operator.
                pass

            if token in self.operators:
                if len(stack) < 2:
                    raise ValueError("Insufficient operands for the operator.")
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
                        raise ZeroDivisionError("Division by zero is undefined.")
                    result = left / right
                else:
                    raise ValueError(f"Unsupported operator encountered: {token}")

                stack.append(result)
            else:
                raise ValueError(f"Unknown token in evaluation: {token}")

        if len(stack) != 1:
            raise ValueError("The expression is invalid or incomplete.")

        return stack[0]


if __name__ == '__main__':
    import sys

    calc = Calculator()
    print("Console-based Arithmetic Calculator (Enter 'q' or 'quit' to exit)")
    
    # If expressions are provided as command line arguments, evaluate them once.
    if len(sys.argv) > 1:
        expression = ' '.join(sys.argv[1:])
        try:
            result = calc.calculate(expression)
            print(f"Expression: {expression}\nResult: {result}")
        except Exception as e:
            print(f"Error in calculation: {e}")
    else:
        # Interactive loop for user input.
        while True:
            user_input = input("\nEnter expression: ")
            if user_input.lower() in {'q', 'quit'}:
                print("Exiting calculator. Goodbye!")
                break
            try:
                result = calc.calculate(user_input)
                print("Result:", result)
            except Exception as e:
                print("Error in calculation:", e)
