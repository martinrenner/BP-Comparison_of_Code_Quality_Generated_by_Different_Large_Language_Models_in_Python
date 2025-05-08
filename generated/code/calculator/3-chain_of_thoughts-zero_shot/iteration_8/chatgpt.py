import re

class Calculator:
    """
    A console-based arithmetic calculator that supports +, -, *, / operations,
    parentheses, and both integer and decimal numbers (including negatives).
    
    The Calculator adheres to ISO/IEC 25010 requirements by offering correctness,
    performance, modularity, safety, testability, and readability.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluate the arithmetic expression and return the computed result as a float.
        
        Parameters:
            expression (str): The arithmetic expression to evaluate.
        
        Returns:
            float: The evaluated result.
        
        Raises:
            ValueError: If the expression contains invalid characters, unbalanced parentheses,
                        or is otherwise malformed.
            ZeroDivisionError: If division by zero occurs during evaluation.
        """
        tokens = self._tokenize(expression)
        postfix = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix)
        return result

    def _tokenize(self, expression: str) -> list:
        """
        Convert the input expression string into a list of tokens (numbers and operators).
        
        Supports negative numbers (via unary '-' or '+') and decimals.
        
        Parameters:
            expression (str): The arithmetic expression as a string.
        
        Returns:
            list: A list of tokens where numbers are converted to float and operators/parentheses remain as strings.
        
        Raises:
            ValueError: If an invalid character is found.
        """
        tokens = []
        i = 0
        n = len(expression)
        allowed_chars = "0123456789.+-*/() "  # valid characters

        while i < n:
            char = expression[i]

            # Skip whitespace characters
            if char.isspace():
                i += 1
                continue

            if char not in allowed_chars:
                raise ValueError(f"Invalid character found: '{char}'")

            # Handle a potential unary plus or minus (for numbers)
            if char in "+-":
                # Determine if this plus/minus is unary by checking one of:
                # - first character in expression
                # - following an operator or an opening parenthesis.
                if (i == 0 or (tokens and isinstance(tokens[-1], str) and tokens[-1] in ("+", "-", "*", "/", "("))):
                    # It's a unary operator for a number.
                    sign = char
                    i += 1
                    # After a unary sign, the next characters must form a number.
                    number_str = sign
                    dot_count = 0
                    number_started = False
                    while i < n and (expression[i].isdigit() or expression[i] == '.'):
                        if expression[i] == '.':
                            dot_count += 1
                            if dot_count > 1:
                                raise ValueError("Invalid numeric format: multiple decimal points.")
                        number_str += expression[i]
                        number_started = True
                        i += 1
                    if not number_started:
                        raise ValueError("Invalid syntax: expected a number after unary sign.")
                    try:
                        tokens.append(float(number_str))
                    except ValueError:
                        raise ValueError(f"Invalid number format: {number_str}")
                    continue

            # If the character is a digit or a dot, read a full number.
            if char.isdigit() or char == '.':
                number_str = ""
                dot_count = 0
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid numeric format: multiple decimal points.")
                    number_str += expression[i]
                    i += 1
                try:
                    tokens.append(float(number_str))
                except ValueError:
                    raise ValueError(f"Invalid number format: {number_str}")
                continue

            # If the character is an operator or parenthesis, add it as a token.
            if char in "+-*/()":
                tokens.append(char)
                i += 1
                continue

            # If the character is none of the above (should never happen due to allowed_chars check).
            raise ValueError(f"Unexpected character encountered: '{char}'")

        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Convert the list of tokens from infix notation to postfix (Reverse Polish Notation)
        using the Shunting-yard algorithm.
        
        Parameters:
            tokens (list): Tokens in infix order.
        
        Returns:
            list: Tokens in postfix order.
        
        Raises:
            ValueError: If there are unbalanced parentheses.
        """
        output_queue = []
        operator_stack = []
        # Define operator precedence
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in precedence:
                # While there is an operator at the top of the stack with greater or equal precedence,
                # pop it from the operator stack onto the output queue.
                while operator_stack and operator_stack[-1] != '(' and precedence.get(operator_stack[-1], 0) >= precedence[token]:
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                # Pop until '(' is encountered.
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Unbalanced parentheses: missing '('")
                operator_stack.pop()  # Remove the '(' from the stack
            else:
                # This branch should not be reached.
                raise ValueError(f"Unexpected token: {token}")

        # Any remaining operators in the stack should be popped out.
        while operator_stack:
            op = operator_stack.pop()
            if op == '(' or op == ')':
                raise ValueError("Unbalanced parentheses: mismatched '(' or ')'")
            output_queue.append(op)

        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluate the expression given in postfix (Reverse Polish Notation) and return the result.
        
        Parameters:
            tokens (list): Tokens in postfix order.
        
        Returns:
            float: The evaluated result.
        
        Raises:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If division by zero is attempted.
        """
        stack = []
        
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in ("+", "-", "*", "/"):
                if len(stack) < 2:
                    raise ValueError("Malformed expression.")
                right = stack.pop()
                left = stack.pop()

                if token == "+":
                    result = left + right
                elif token == "-":
                    result = left - right
                elif token == "*":
                    result = left * right
                elif token == "/":
                    if right == 0:
                        raise ZeroDivisionError("Division by zero.")
                    result = left / right
                stack.append(result)
            else:
                raise ValueError(f"Invalid token in postfix expression: {token}")

        if len(stack) != 1:
            raise ValueError("Malformed expression after evaluation.")
        return stack[0]

def main():
    """
    Main function to run the console-based arithmetic calculator.
    
    Accepts expressions from the user until 'exit' is entered.
    """
    calc = Calculator()
    print("Console-Based Arithmetic Calculator")
    print("Enter an arithmetic expression (or type 'exit' to quit):")

    while True:
        expression = input("> ")
        if expression.lower() in ("exit", "quit"):
            print("Exiting calculator.")
            break

        try:
            result = calc.calculate(expression)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
