class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses with proper operator precedence.
    
    Supported operations:
      - Addition: +
      - Subtraction: -
      - Multiplication: *
      - Division: /

    This calculator also accepts both integers and floating-point numbers, including negative values.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression contains invalid characters, is not well-formed (e.g., unbalanced parentheses),
                        or if a numeric token is formatted incorrectly.
            ZeroDivisionError: If the expression attempts division by zero.
        """
        # Normalize and validate the expression.
        normalized = self._normalize_expression(expression)
        if not self._is_balanced(normalized):
            raise ValueError("Unbalanced parentheses in the expression.")
        
        # Tokenize the expression.
        tokens = self._tokenize(normalized)
        
        # Convert the tokens from infix notation to postfix (RPN).
        postfix = self._infix_to_postfix(tokens)
        
        # Evaluate the RPN expression.
        result = self._evaluate_postfix(postfix)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.

        Args:
            expression (str): The arithmetic expression as a string.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains characters other than digits, operators, parentheses, or dot.
        """
        allowed_chars = set("0123456789+-*/(). ")
        for char in expression:
            if char not in allowed_chars:
                raise ValueError("Expression contains invalid characters.")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether the expression has properly paired parentheses.

        Args:
            expression (str): The normalized arithmetic expression.

        Returns:
            bool: True if the parentheses are balanced, False otherwise.
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
        Converts the normalized expression into a list of tokens (numbers, operators, and parentheses).

        Args:
            expression (str): The normalized arithmetic expression.

        Returns:
            list: A list of tokens as strings.

        Raises:
            ValueError: If a number is improperly formatted or if an operator is used incorrectly.
        """
        tokens = []
        i = 0
        n = len(expression)

        while i < n:
            char = expression[i]

            # If the character is a digit or a decimal point, accumulate the complete number.
            if char.isdigit() or char == '.':
                number_str = char
                i += 1
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    number_str += expression[i]
                    i += 1
                if number_str.count('.') > 1:
                    raise ValueError("Invalid number format: too many decimal points.")
                tokens.append(number_str)
            # Handle the '-' operator: may be unary (negative number) or binary (subtraction).
            elif char == '-':
                # Determine if the '-' is a unary minus.
                if i == 0 or (tokens and tokens[-1] in {'+', '-', '*', '/', '('}):
                    # It is a unary minus; the following characters must form a valid number.
                    i += 1
                    if i < n and (expression[i].isdigit() or expression[i] == '.'):
                        number_str = '-' + expression[i]
                        i += 1
                        while i < n and (expression[i].isdigit() or expression[i] == '.'):
                            number_str += expression[i]
                            i += 1
                        if number_str.count('.') > 1:
                            raise ValueError("Invalid number format: too many decimal points.")
                        tokens.append(number_str)
                    else:
                        raise ValueError("Invalid use of unary minus: no number follows '-'.")
                else:
                    # Binary minus operator.
                    tokens.append(char)
                    i += 1
            elif char in {'+', '*', '/'}:
                tokens.append(char)
                i += 1
            elif char in {'(', ')'}:
                tokens.append(char)
                i += 1
            else:
                raise ValueError(f"Unexpected character encountered: {char}")
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts an infix token list into a postfix (Reverse Polish Notation) token list using
        the shunting-yard algorithm.

        Args:
            tokens (list): The list of tokens in infix notation.

        Returns:
            list: The postfix token list.

        Raises:
            ValueError: If the expression is not well-formed.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        operator_stack = []

        for token in tokens:
            # If the token is a number, add it to the output.
            if self._is_number(token):
                output_queue.append(token)
            # If the token is an operator.
            elif token in precedence:
                while (operator_stack and operator_stack[-1] in precedence and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            # If the token is a left parenthesis.
            elif token == "(":
                operator_stack.append(token)
            # If the token is a right parenthesis.
            elif token == ")":
                # Pop operators until a left parenthesis is encountered.
                while operator_stack and operator_stack[-1] != "(":
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1] != "(":
                    raise ValueError("Mismatched parentheses in the expression.")
                operator_stack.pop()  # Remove the '(' from the stack.
            else:
                raise ValueError(f"Invalid token found: {token}")

        # Pop any remaining operators from the stack.
        while operator_stack:
            top = operator_stack.pop()
            if top in {"(", ")"}:
                raise ValueError("Mismatched parentheses in the expression.")
            output_queue.append(top)

        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix (Reverse Polish Notation) expression.

        Args:
            tokens (list): The postfix token list.

        Returns:
            float: The result of the evaluation.

        Raises:
            ZeroDivisionError: If a division by zero occurs.
            ValueError: If the expression is malformed.
        """
        stack = []
        for token in tokens:
            if self._is_number(token):
                stack.append(float(token))
            elif token in {'+', '-', '*', '/'}:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient values in the expression.")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in evaluation: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression: improper evaluation.")

        return stack[0]

    def _apply_operator(self, a: float, b: float, operator: str) -> float:
        """
        Applies an arithmetic operator on two numbers.

        Args:
            a (float): The first operand.
            b (float): The second operand.
            operator (str): The operator as a string ("+", "-", "*", or "/").

        Returns:
            float: The result of applying the operator.

        Raises:
            ZeroDivisionError: If division by zero is attempted.
            ValueError: If an unknown operator is encountered.
        """
        if operator == "+":
            return a + b
        elif operator == "-":
            return a - b
        elif operator == "*":
            return a * b
        elif operator == "/":
            if b == 0:
                raise ZeroDivisionError("Division by zero is undefined.")
            return a / b
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def _is_number(self, token: str) -> bool:
        """
        Determines if a token represents a number.

        Args:
            token (str): The token to check.

        Returns:
            bool: True if the token is a valid number, False otherwise.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    import sys

    def main():
        """
        The main function for the console-based arithmetic calculator.
        It keeps accepting expressions from the user until 'exit' is entered.
        """
        calc = Calculator()
        print("Welcome to the Console-Based Arithmetic Calculator!")
        print("Enter your arithmetic expression below (or type 'exit' to quit).")
        
        while True:
            try:
                expression = input("\nExpression> ").strip()
                if expression.lower() in {"exit", "quit"}:
                    print("Goodbye!")
                    break
                result = calc.calculate(expression)
                print(f"Result: {result}")
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)

    main()
