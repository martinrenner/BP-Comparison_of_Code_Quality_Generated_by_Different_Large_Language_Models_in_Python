class Calculator:
    """
    A console-based arithmetic calculator that supports basic arithmetic operations:
    addition (+), subtraction (-), multiplication (*), and division (/), including the use
    of parentheses and negative/decimal numbers. The calculator respects the standard order 
    of operations.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result as a float.

        Args:
            expression (str): A string containing the mathematical expression.

        Returns:
            float: The evaluated result.

        Raises:
            ValueError: If the expression contains invalid characters, improper formatting,
                        or unbalanced parentheses.
            ZeroDivisionError: If the expression attempts division by zero.
        """
        # Normalize and validate the expression first.
        normalized_expr = self._normalize_expression(expression)
        # Tokenize the expression into numbers and operators.
        tokens = self._tokenize(normalized_expr)
        # Convert the token list from infix to postfix notation.
        postfix_tokens = self._infix_to_postfix(tokens)
        # Evaluate the postfix expression and return the result.
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the mathematical expression by removing spaces and validating allowed characters.
        
        Args:
            expression (str): The input expression.
        
        Returns:
            str: The normalized expression.
        
        Raises:
            ValueError: If the expression contains disallowed characters or if its parentheses
                        are not balanced.
        """
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")
        
        # Remove spaces
        normalized = expression.replace(" ", "")
        
        # Validate balanced parentheses
        if not self._is_balanced(normalized):
            raise ValueError("Expression has unbalanced parentheses.")
        
        return normalized

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether the parentheses in the expression are balanced.

        Args:
            expression (str): The mathematical expression.
        
        Returns:
            bool: True if the parentheses are balanced; False otherwise.
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
        Tokenizes the normalized mathematical expression into numbers and operators.
        
        Args:
            expression (str): The normalized input expression.
        
        Returns:
            list: List of tokens where numbers are converted to floats and operators/parentheses remain as str.
        
        Raises:
            ValueError: If an invalid number format is encountered.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            # Process a number (which may include a decimal point) or a unary sign.
            if char.isdigit() or char == '.':
                number_str = char
                i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    number_str += expression[i]
                    i += 1
                try:
                    tokens.append(float(number_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: {number_str}")
            elif char in '+-':
                # Identify if the operator is unary: if it appears at the beginning or after another operator or '('.
                if i == 0 or expression[i - 1] in "(+*/-":
                    # Check if a number follows (allowing for decimal numbers)
                    if i + 1 < len(expression) and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                        sign = -1 if char == '-' else 1
                        i += 1
                        number_str = ""
                        while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                            number_str += expression[i]
                            i += 1
                        try:
                            tokens.append(sign * float(number_str))
                        except ValueError:
                            raise ValueError(f"Invalid number format: {char}{number_str}")
                    else:
                        # It's a unary plus/minus without an attached number; treat it as an operator.
                        tokens.append(char)
                        i += 1
                else:
                    tokens.append(char)
                    i += 1
            elif char in "*/()":
                tokens.append(char)
                i += 1
            else:
                raise ValueError(f"Invalid character encountered: {char}")
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts an infix token list to a postfix token list using the Shunting Yard algorithm.
        
        Args:
            tokens (list): The list of tokens in infix order.
        
        Returns:
            list: The list of tokens in postfix notation.
        
        Raises:
            ValueError: If there is a mismatched parenthesis.
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
                # Pop operators until the matching '(' is found.
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses encountered.")
                operator_stack.pop()  # Remove the '(' from the stack.
            else:
                raise ValueError(f"Unexpected token: {token}")
        
        # Empty any remaining operators from the stack.
        while operator_stack:
            top = operator_stack.pop()
            if top == '(' or top == ')':
                raise ValueError("Mismatched parentheses encountered in the expression.")
            output_queue.append(top)
        
        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix (Reverse Polish Notation) expression.
        
        Args:
            tokens (list): The list of tokens in postfix order.
        
        Returns:
            float: The evaluated result.
        
        Raises:
            ZeroDivisionError: If division by zero occurs.
            ValueError: If the postfix expression is malformed.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in {'+', '-', '*', '/'}:
                if len(stack) < 2:
                    raise ValueError("Insufficient values in the expression.")
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
                raise ValueError(f"Invalid token in postfix expression: {token}")
        if len(stack) != 1:
            raise ValueError("The expression is malformed.")
        return stack[0]


if __name__ == "__main__":
    # Console-based usage of the Calculator.
    calc = Calculator()
    try:
        expression = input("Enter arithmetic expression: ")
        result = calc.calculate(expression)
        print("Result:", result)
    except Exception as e:
        print(f"Error: {e}")
