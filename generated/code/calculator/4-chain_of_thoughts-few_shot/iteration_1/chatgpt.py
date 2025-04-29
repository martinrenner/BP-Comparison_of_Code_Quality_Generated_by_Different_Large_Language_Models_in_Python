from typing import List, Union

class Calculator:
    """
    A simple console-based arithmetic calculator supporting addition, subtraction,
    multiplication, division, and parentheses. The calculator adheres to ISO/IEC 25010
    quality standards including modularity, safety, performance, and testability.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression provided as a string.

        The expression can contain integers, decimals (including negative numbers),
        operators (+, -, *, /), and parentheses. The method normalizes, validates,
        tokenizes, converts to Reverse Polish Notation (RPN), and evaluates the expression.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression contains invalid characters, has unbalanced
                        parentheses, or is otherwise malformed.
            ZeroDivisionError: If a division by zero is attempted.
        """
        # Normalize and validate the expression
        expression = self._normalize_expression(expression)
        if not self._is_balanced(expression):
            raise ValueError("The expression has unbalanced parentheses.")

        # Tokenize the expression into numbers and operators
        tokens = self._tokenize(expression)
        # Convert the tokens from infix to postfix notation
        postfix_tokens = self._to_postfix(tokens)
        # Evaluate the postfix expression and return the result
        return self._evaluate_postfix(postfix_tokens)

    @staticmethod
    def _normalize_expression(expression: str) -> str:
        """
        Normalizes a mathematical expression by removing spaces and validating characters.

        Args:
            expression (str): The original mathematical expression.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains any invalid characters.
        """
        allowed_chars = set("0123456789+-*/(). ")
        for char in expression:
            if char not in allowed_chars:
                raise ValueError(f"Invalid character '{char}' found in expression.")
        return expression.replace(" ", "")

    @staticmethod
    def _is_balanced(expression: str) -> bool:
        """
        Checks whether the expression has properly balanced parentheses.

        Args:
            expression (str): The mathematical expression.

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

    @staticmethod
    def _tokenize(expression: str) -> List[Union[float, str]]:
        """
        Tokenizes the normalized expression into numbers and operators.

        The method handles integer and decimal numbers, including negative numbers
        when a '-' sign represents a unary operator.

        Args:
            expression (str): The normalized arithmetic expression.

        Returns:
            List[Union[float, str]]: A list where numbers are represented as floats
                                     and operators/parentheses as strings.

        Raises:
            ValueError: If a number is malformed (e.g., multiple decimal points).
        """
        tokens: List[Union[float, str]] = []
        i = 0
        n = len(expression)
        
        while i < n:
            char = expression[i]
            # Check if the character represents the start of a number.
            # A '-' is considered a unary minus if it appears at the beginning
            # or immediately after an operator or an opening parenthesis.
            if (char.isdigit() or char == '.') or (
                char == '-' and (i == 0 or expression[i - 1] in "+-*/(") and (i + 1 < n and (expression[i + 1].isdigit() or expression[i + 1] == '.'))
            ):
                num_str = ""
                # If a unary minus is detected, include it in the number string.
                if char == '-':
                    num_str += char
                    i += 1
                    if i >= n:
                        raise ValueError("Invalid number format: '-' at the end of expression.")
                
                dot_count = 0
                # Build the number string including digits and at most one decimal point.
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid number format: multiple decimal points.")
                    num_str += expression[i]
                    i += 1
                
                try:
                    number = float(num_str)
                except ValueError as e:
                    raise ValueError(f"Invalid number: '{num_str}'.") from e
                tokens.append(number)
            elif char in "+-*/()":
                tokens.append(char)
                i += 1
            else:
                # This should not occur because of prior normalization.
                raise ValueError(f"Unexpected character '{char}' in expression.")
        
        return tokens

    @staticmethod
    def _to_postfix(tokens: List[Union[float, str]]) -> List[Union[float, str]]:
        """
        Converts a list of tokens in infix notation to postfix (Reverse Polish Notation)
        using the Shunting-yard algorithm.

        Args:
            tokens (List[Union[float, str]]): The tokenized infix expression.

        Returns:
            List[Union[float, str]]: The expression converted to postfix notation.

        Raises:
            ValueError: If the expression contains mismatched parentheses.
        """
        output: List[Union[float, str]] = []
        op_stack: List[str] = []
        # Define operator precedence
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if isinstance(token, float):
                output.append(token)
            elif token in "+-*/":
                while op_stack and op_stack[-1] != '(' and precedence.get(op_stack[-1], 0) >= precedence[token]:
                    output.append(op_stack.pop())
                op_stack.append(token)
            elif token == '(':
                op_stack.append(token)
            elif token == ')':
                # Pop operators until the matching '(' is found
                while op_stack and op_stack[-1] != '(':
                    output.append(op_stack.pop())
                if not op_stack:
                    raise ValueError("Mismatched parentheses detected.")
                op_stack.pop()  # Discard the '('
            else:
                raise ValueError(f"Unknown token encountered: {token}")

        # Append any remaining operators from the stack
        while op_stack:
            token = op_stack.pop()
            if token in "()":
                raise ValueError("Mismatched parentheses detected.")
            output.append(token)

        return output

    @staticmethod
    def _evaluate_postfix(postfix_tokens: List[Union[float, str]]) -> float:
        """
        Evaluates an expression in postfix notation.

        Args:
            postfix_tokens (List[Union[float, str]]): The postfix (RPN) expression tokens.

        Returns:
            float: The evaluated result.

        Raises:
            ZeroDivisionError: If division by zero is encountered.
            ValueError: If the expression is malformed.
        """
        stack: List[float] = []
        
        for token in postfix_tokens:
            if isinstance(token, float):
                stack.append(token)
            elif token in "+-*/":
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands.")
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
                raise ValueError(f"Unknown token during evaluation: {token}")
        
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands.")
        
        return stack[0]

def main():
    """
    Main function to run the console-based arithmetic calculator.
    
    Users can enter expressions in the console. The calculator will evaluate the expressions
    and display the result. To exit the program, type 'exit' or 'quit'.
    """
    calc = Calculator()
    print("Console-based Arithmetic Calculator")
    print("Enter an expression to evaluate or type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("Expression> ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("Exiting calculator. Goodbye!")
                break

            result = calc.calculate(user_input)
            print("Result:", result)
        except (ValueError, ZeroDivisionError) as error:
            print("Error:", error)
        except KeyboardInterrupt:
            print("\nExiting calculator. Goodbye!")
            break

if __name__ == '__main__':
    main()
