import sys

class Calculator:
    """
    A console-based arithmetic calculator that supports addition (+), subtraction (-),
    multiplication (*), division (/), parentheses for grouping, and both integer and
    floating-point numbers (including negatives). Input expressions are validated
    for balanced parentheses and allowed characters.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates an arithmetic expression and returns the result as a float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression contains invalid characters or unbalanced parentheses.
            ZeroDivisionError: If a division by zero is attempted.
        """
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("Unbalanced parentheses in the expression.")
        tokens = self._tokenize(normalized_expr)
        rpn_tokens = self._to_rpn(tokens)
        result = self._evaluate_rpn(rpn_tokens)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression by removing spaces and validating allowed characters.

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
        Checks if the parentheses in the expression are properly balanced.

        Args:
            expression (str): The arithmetic expression.

        Returns:
            bool: True if parentheses are balanced; otherwise, False.
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
        Converts the normalized expression string into a list of tokens. Tokens are either
        numbers (as float) or operator/parentheses characters as strings.

        This method handles unary minus (and unary plus) operators. Specifically, if a '-' 
        (or '+') occurs at the start of the expression or immediately after an operator or 
        an opening parenthesis, and is followed by a digit or a dot, it is treated as part of 
        a numeric literal. If a unary '-' is encountered immediately before a parenthesis, it is 
        converted into multiplication by -1 (e.g., "-(3+2)" becomes "-1 * (3+2)").

        Args:
            expression (str): The normalized arithmetic expression.

        Returns:
            list: A list of tokens (numbers as floats and operators as str).

        Raises:
            ValueError: If the number format is invalid.
        """
        tokens = []
        i = 0
        length = len(expression)
        while i < length:
            char = expression[i]

            # Handle unary plus or minus.
            if char in "+-" and (i == 0 or expression[i - 1] in "(-+*/"):
                # If next character is an opening parenthesis, handle unary minus specifically.
                if i + 1 < length and expression[i + 1] == '(':
                    if char == '-':
                        # Transform "-(" into "(-1)*(".
                        tokens.append(-1.0)
                        tokens.append('*')
                        i += 1  # Skip the '-' and let '(' be processed normally.
                        continue
                    elif char == '+':
                        # Skip the unary plus.
                        i += 1
                        continue
                # Otherwise, if the next character is a digit or a dot, parse as a signed number.
                elif i + 1 < length and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                    start = i
                    i += 1
                    while i < length and (expression[i].isdigit() or expression[i] == '.'):
                        i += 1
                    num_str = expression[start:i]
                    try:
                        number = float(num_str)
                    except ValueError:
                        raise ValueError(f"Invalid number format: {num_str}")
                    tokens.append(number)
                    continue
                else:
                    # Otherwise, treat the sign as a binary operator.
                    tokens.append(char)
                    i += 1
                    continue

            # Parse numbers (including those starting with a digit or dot).
            if char.isdigit() or char == '.':
                start = i
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    i += 1
                num_str = expression[start:i]
                try:
                    number = float(num_str)
                except ValueError:
                    raise ValueError(f"Invalid number format: {num_str}")
                tokens.append(number)
                continue

            # For operators and parentheses.
            if char in "+-*/()":
                tokens.append(char)
                i += 1
                continue

            # Should not reach here due to normalization.
            raise ValueError(f"Unexpected character encountered: {char}")

        return tokens

    def _to_rpn(self, tokens: list) -> list:
        """
        Converts a list of tokens in infix notation to Reverse Polish Notation (RPN)
        using the shunting-yard algorithm.

        Args:
            tokens (list): The list of tokens in infix notation.

        Returns:
            list: A list of tokens in RPN.

        Raises:
            ValueError: If there are mismatched parentheses.
        """
        output_queue = []
        operator_stack = []
        # Define operator precedence.
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if isinstance(token, (float, int)):
                output_queue.append(token)
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], 0) >= precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                # Pop operators until an opening parenthesis is encountered.
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses in the expression.")
                operator_stack.pop()  # Discard the '('.
            else:
                raise ValueError(f"Unknown token encountered: {token}")

        while operator_stack:
            top = operator_stack.pop()
            if top in '()':
                raise ValueError("Mismatched parentheses in the expression.")
            output_queue.append(top)

        return output_queue

    def _evaluate_rpn(self, tokens: list) -> float:
        """
        Evaluates an expression in Reverse Polish Notation (RPN).

        Args:
            tokens (list): A list of tokens in RPN.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If there is an error in the expression format.
            ZeroDivisionError: If a division by zero is attempted.
        """
        stack = []
        for token in tokens:
            if isinstance(token, (float, int)):
                stack.append(token)
            elif token in "+-*/":
                if len(stack) < 2:
                    raise ValueError("Insufficient operands in the expression.")
                right_operand = stack.pop()
                left_operand = stack.pop()
                if token == '+':
                    result = left_operand + right_operand
                elif token == '-':
                    result = left_operand - right_operand
                elif token == '*':
                    result = left_operand * right_operand
                elif token == '/':
                    if right_operand == 0:
                        raise ZeroDivisionError("Division by zero encountered.")
                    result = left_operand / right_operand
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in RPN expression: {token}")

        if len(stack) != 1:
            raise ValueError("The expression could not be evaluated properly.")
        return stack[0]


def main():
    """
    Main function to run the console-based arithmetic calculator.
    Reads an arithmetic expression from the user and prints the evaluated result.
    """
    calc = Calculator()

    if len(sys.argv) > 1:
        # Expression provided as command-line argument.
        expression = " ".join(sys.argv[1:])
        try:
            result = calc.calculate(expression)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        # Interactive mode.
        print("Console-based Arithmetic Calculator")
        print("Enter an arithmetic expression to evaluate (or 'quit' to exit).")
        while True:
            expression = input(">>> ")
            if expression.lower() in {"quit", "exit"}:
                break
            try:
                result = calc.calculate(expression)
                print(f"Result: {result}")
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
