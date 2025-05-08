class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions with
    support for addition, subtraction, multiplication, division, and parentheses.
    
    The calculator adheres to the ISO/IEC 25010 requirements regarding functionality,
    code quality, modularity, performance, safety, and testability.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression and returns the result as a float.
        
        The expression can include integers, decimals (including negative numbers),
        operators (+, -, *, /), and parentheses. The correct order of operations
        is ensured.
        
        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression contains invalid characters,
                        has unbalanced parentheses, or is otherwise invalid.
            ZeroDivisionError: If division by zero is encountered.
        """
        normalized_expr = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expr):
            raise ValueError("Expression has unbalanced parentheses.")

        tokens = self._tokenize(normalized_expr)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.
        
        Args:
            expression (str): A mathematical expression.
        
        Returns:
            str: The normalized expression (without spaces).
        
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")
        # Remove all whitespace characters
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether a mathematical expression has properly paired parentheses.
        
        Args:
            expression (str): A mathematical expression.
        
        Returns:
            bool: True if the parentheses are balanced, otherwise False.
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
        Converts an arithmetic expression string into a list of tokens (numbers and operators).
        
        This method handles negative numbers (e.g., -5 or 3*-2) by checking the context
        in which a '-' sign appears.
        
        Args:
            expression (str): The normalized arithmetic expression.
        
        Returns:
            list: A list of tokens (strings) representing numbers, operators, and parentheses.
        
        Raises:
            ValueError: If an unexpected character is encountered.
        """
        tokens = []
        i = 0
        length = len(expression)
        
        while i < length:
            char = expression[i]

            # If the character is a digit or a decimal point, parse a number.
            if char.isdigit() or char == '.':
                start = i
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    i += 1
                tokens.append(expression[start:i])
            # Handle '+' and '-' operators: check if '-' is a unary negative.
            elif char in "+-":
                if char == '-' and (i == 0 or expression[i - 1] in "+-*/("):
                    # Unary minus detected; check if following characters form a number.
                    if i + 1 < length and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                        start = i
                        i += 1
                        while i < length and (expression[i].isdigit() or expression[i] == '.'):
                            i += 1
                        tokens.append(expression[start:i])
                    else:
                        # Treat as subtraction if no valid number follows.
                        tokens.append(char)
                        i += 1
                else:
                    tokens.append(char)
                    i += 1
            # Handle multiplication and division.
            elif char in "*/":
                tokens.append(char)
                i += 1
            # Handle parentheses.
            elif char in "()":
                tokens.append(char)
                i += 1
            else:
                raise ValueError(f"Unexpected character encountered: {char}")
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts a list of tokens in infix notation to postfix (Reverse Polish Notation).
        
        This conversion uses the Shunting Yard algorithm to ensure the correct order
        of operations.
        
        Args:
            tokens (list): A list of tokens representing the infix expression.
        
        Returns:
            list: A list of tokens in postfix order.
        
        Raises:
            ValueError: If mismatched parentheses are found.
        """
        output = []
        operators = []
        # Define operator precedence (all operators are left-associative here).
        precedences = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            # Check if token is a number (including negative numbers and decimals).
            try:
                float(token)
                output.append(token)
            except ValueError:
                # Token is an operator or parenthesis.
                if token in precedences:
                    while (operators and operators[-1] != '(' and
                           precedences.get(operators[-1], 0) >= precedences[token]):
                        output.append(operators.pop())
                    operators.append(token)
                elif token == '(':
                    operators.append(token)
                elif token == ')':
                    while operators and operators[-1] != '(':
                        output.append(operators.pop())
                    if not operators:
                        raise ValueError("Mismatched parentheses encountered.")
                    operators.pop()  # Remove the '(' from the stack.
                else:
                    raise ValueError(f"Unknown token: {token}")

        # Pop any remaining operators from the operator stack.
        while operators:
            top = operators.pop()
            if top in '()':
                raise ValueError("Mismatched parentheses encountered.")
            output.append(top)

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates an expression in postfix (Reverse Polish Notation) form.
        
        Args:
            tokens (list): A list of tokens in postfix order.
        
        Returns:
            float: The evaluated result of the expression.
        
        Raises:
            ValueError: If the expression is invalid.
            ZeroDivisionError: If division by zero is attempted.
        """
        stack = []
        for token in tokens:
            # If token is a number, push it to the stack.
            try:
                number = float(token)
                stack.append(number)
            except ValueError:
                # Token must be an operator.
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands.")
                
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
                    raise ValueError(f"Unsupported operator encountered: {token}")

                stack.append(result)

        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands.")
        return stack[0]


def main():
    """
    Main function to run the console-based arithmetic calculator.
    """
    calc = Calculator()
    print("Welcome to the Console-based Arithmetic Calculator!")
    print("Enter an arithmetic expression to evaluate (or 'quit' to exit).")
    
    while True:
        user_input = input(">> ")
        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break
        
        try:
            result = calc.calculate(user_input)
            print("Result:", result)
        except Exception as error:
            print("Error:", error)


if __name__ == '__main__':
    main()
