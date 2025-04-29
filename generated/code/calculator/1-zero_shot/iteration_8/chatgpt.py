class Calculator:
    """
    A console-based arithmetic calculator that supports addition (+), subtraction (-),
    multiplication (*), division (/), and parentheses. It correctly handles operator 
    precedence and accepts both integers and floating-point numbers (including negatives).
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result as a float.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The computed result of the expression.

        Raises:
            ValueError: If the expression contains invalid characters or is malformed.
            SyntaxError: If the expression has unbalanced parentheses.
            ZeroDivisionError: If division by zero occurs.
        """
        # Remove spaces for easier processing
        expr = expression.replace(" ", "")
        # Tokenize the input expression and validate it
        tokens = self._tokenize(expr)
        # Convert the token list from infix to postfix notation using the shunting yard algorithm
        postfix_tokens = self._infix_to_postfix(tokens)
        # Evaluate the postfix expression to obtain the result
        return self._evaluate_postfix(postfix_tokens)

    def _tokenize(self, expression: str) -> list:
        """
        Converts the input expression string into a list of tokens (numbers, operators, parentheses).

        Args:
            expression (str): A sanitized arithmetic expression (without spaces).

        Returns:
            list: A list of tokens where numbers are represented as floats and operators as strings.

        Raises:
            ValueError: If an invalid character is encountered or a number is malformed.
        """
        tokens = []
        i = 0
        valid_chars = "0123456789.+-*/()"
        length = len(expression)
        
        while i < length:
            char = expression[i]
            if char not in valid_chars:
                raise ValueError(f"Invalid character encountered: '{char}'")
            
            # Determine if we are parsing a number. A number can start with a digit, a dot, or a '-' 
            # sign indicating a negative number when at the start or following an operator/parenthesis.
            if char.isdigit() or char == '.' or (
                char == '-' and (
                    i == 0 or expression[i-1] in "(-+*/"
                ) and i + 1 < length and (expression[i+1].isdigit() or expression[i+1] == '.')
            ):
                num_str = char
                i += 1
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                try:
                    num_value = float(num_str)
                except ValueError:
                    raise ValueError(f"Malformed number: '{num_str}'")
                tokens.append(num_value)
            elif char in "+-*/()":
                tokens.append(char)
                i += 1
            else:
                # This branch should not be reached due to the valid_chars check above.
                raise ValueError(f"Unexpected character: '{char}'")
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts tokens from infix notation to postfix notation (Reverse Polish Notation)
        using the Shunting Yard algorithm.

        Args:
            tokens (list): List of tokens in infix order.

        Returns:
            list: List of tokens in postfix order.

        Raises:
            SyntaxError: If the expression contains unbalanced parentheses.
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
                # Pop operators until an opening parenthesis is encountered.
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise SyntaxError("Unbalanced parentheses detected: missing '('")
                operator_stack.pop()  # Remove the '(' from the stack
            else:
                raise ValueError(f"Unknown token encountered: {token}")

        # Any remaining operators in the stack should now be appended to the output.
        while operator_stack:
            op = operator_stack.pop()
            if op in '()':
                raise SyntaxError("Unbalanced parentheses detected.")
            output_queue.append(op)
        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix (RPN) expression represented as a list of tokens.

        Args:
            tokens (list): The list of tokens in postfix notation.

        Returns:
            float: The result of the evaluated postfix expression.

        Raises:
            ZeroDivisionError: If a division by zero is encountered.
            ValueError: If the postfix expression is malformed.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in "+-*/":
                if len(stack) < 2:
                    raise ValueError("Malformed expression: insufficient operands.")
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
                raise ValueError(f"Unexpected token during evaluation: {token}")

        if len(stack) != 1:
            raise ValueError("Malformed expression: too many values remaining.")
        return stack[0]


if __name__ == "__main__":
    """
    Console interface for the arithmetic calculator.
    
    Users can enter expressions to evaluate. Type 'exit' or 'quit' to terminate the program.
    """
    calc = Calculator()
    print("Arithmetic Calculator")
    print("Enter an expression to evaluate or type 'exit' to quit.")
    
    while True:
        try:
            user_input = input(">>> ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("Exiting calculator. Goodbye!")
                break
            result = calc.calculate(user_input)
            print("Result:", result)
        except Exception as e:
            # Display any errors encountered during evaluation.
            print("Error:", e)
