class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and proper handling of parentheses with correct operator precedence.
    
    This implementation adheres to ISO/IEC 25010 quality standards by ensuring correctness,
    performance, modularity, security, testability, and readability.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result as a float.
        
        Args:
            expression (str): The arithmetic expression to evaluate.
        
        Returns:
            float: The result of the evaluated expression.
        
        Raises:
            ValueError: If the expression contains invalid characters, is syntactically incorrect,
                        or if parentheses are unbalanced.
            ZeroDivisionError: If a division by zero occurs during evaluation.
        """
        # Normalize the expression by removing whitespace and validating allowed characters.
        normalized_expr = self._normalize_expression(expression)

        # Ensure that the expression contains balanced parentheses.
        if not self._is_balanced(normalized_expr):
            raise ValueError("The expression has unbalanced parentheses.")

        # Tokenize the expression into numbers, operators, and parentheses.
        tokens = self._tokenize(normalized_expr)

        # Convert the infix tokens into a postfix (Reverse Polish Notation) expression.
        postfix_tokens = self._infix_to_postfix(tokens)

        # Evaluate the postfix expression and return the result.
        return self._evaluate_postfix(postfix_tokens)

    @staticmethod
    def _normalize_expression(expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and ensuring all characters are valid.
        
        Args:
            expression (str): The input arithmetic expression.
        
        Returns:
            str: The normalized expression.
        
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")
        return expression.replace(" ", "")

    @staticmethod
    def _is_balanced(expression: str) -> bool:
        """
        Checks whether a mathematical expression has properly paired parentheses.
        
        Args:
            expression (str): The mathematical expression.
        
        Returns:
            bool: True if parentheses are correctly paired, otherwise False.
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
        Tokenizes the normalized expression into numbers (as floats), operators, and parentheses.
        Supports negative (or positive) numbers as unary operators.
        
        Args:
            expression (str): The normalized mathematical expression.
        
        Returns:
            list: A list of tokens (floats for numbers and str for operators/parentheses).
        
        Raises:
            ValueError: If the syntax of the expression is invalid.
        """
        tokens = []
        i = 0
        n = len(expression)
        
        while i < n:
            char = expression[i]

            # Process numbers (integer or float)
            if char.isdigit() or char == '.':
                number_str = ""
                # Accumulate consecutive digits and at most one dot.
                dot_count = 0
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid number format with multiple decimals.")
                    number_str += expression[i]
                    i += 1
                try:
                    tokens.append(float(number_str))
                except ValueError:
                    raise ValueError(f"Invalid number literal: {number_str}")
            
            # Handle unary plus and minus for numbers.
            elif char in "+-" and (
                # At start of expression or preceded by an operator or left parenthesis
                (not tokens) or 
                (isinstance(tokens[-1], str) and tokens[-1] in "+-*/(")
            ):
                sign = char
                i += 1
                # After a unary sign, there must be a number (digit or dot)
                if i < n and (expression[i].isdigit() or expression[i] == '.'):
                    number_str = sign
                    dot_count = 0
                    while i < n and (expression[i].isdigit() or expression[i] == '.'):
                        if expression[i] == '.':
                            dot_count += 1
                            if dot_count > 1:
                                raise ValueError("Invalid number format with multiple decimals.")
                        number_str += expression[i]
                        i += 1
                    try:
                        tokens.append(float(number_str))
                    except ValueError:
                        raise ValueError(f"Invalid number literal: {number_str}")
                else:
                    raise ValueError("Unary operator must be followed by a number.")
            
            # Process binary operators.
            elif char in "+-*/":
                tokens.append(char)
                i += 1
            
            # Process parentheses.
            elif char in "()":
                tokens.append(char)
                i += 1
            
            # If an unexpected character is encountered.
            else:
                raise ValueError(f"Invalid character encountered in expression: {char}")

        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts the list of tokens in infix notation to postfix notation using the Shunting Yard algorithm.
        
        Args:
            tokens (list): A list of tokens in infix order.
        
        Returns:
            list: A list of tokens in postfix order.
        
        Raises:
            ValueError: If there is a problem with mismatched parentheses.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        operator_stack = []

        for token in tokens:
            # If token is a number, add it to the output queue.
            if isinstance(token, float):
                output_queue.append(token)
            # If token is an operator, pop from the operator stack to output queue based on precedence.
            elif token in precedence:
                while (operator_stack and operator_stack[-1] in precedence and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            # Push left parenthesis on the stack.
            elif token == '(':
                operator_stack.append(token)
            # If token is a right parenthesis, pop until matching left parenthesis is found.
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses in expression.")
                operator_stack.pop()  # Remove the '(' from stack
            else:
                raise ValueError(f"Unexpected token encountered: {token}")

        # Pop any remaining operators to the output queue.
        while operator_stack:
            op = operator_stack.pop()
            if op in '()':
                raise ValueError("Mismatched parentheses in expression.")
            output_queue.append(op)

        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix (Reverse Polish Notation) expression.
        
        Args:
            tokens (list): A list of tokens in postfix order.
        
        Returns:
            float: The result of the evaluated expression.
        
        Raises:
            ZeroDivisionError: If a division by zero is encountered.
            ValueError: If the postfix expression is invalid.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in "+-*/":
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient values for operation.")
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
                        raise ZeroDivisionError("Division by zero error.")
                    result = left / right
                stack.append(result)
            else:
                raise ValueError(f"Unexpected token during evaluation: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression: remaining tokens after evaluation.")

        return stack[0]


if __name__ == '__main__':
    calc = Calculator()
    print("Console-based Arithmetic Calculator")
    print("Supported operations: addition (+), subtraction (-), multiplication (*), division (/), and parentheses ().")
    print("Enter 'exit' to quit.\n")

    while True:
        user_input = input("Enter expression: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Exiting calculator. Goodbye!")
            break
        try:
            result = calc.calculate(user_input)
            print("Result:", result)
        except Exception as err:
            print("Error:", err)
