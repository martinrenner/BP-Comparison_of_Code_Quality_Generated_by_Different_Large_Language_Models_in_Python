import re  # Importing the regular expression module


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It handles operator precedence
    and both integer and floating-point numbers.  The calculator avoids using
    eval() or equivalent functions for security and control.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression.

        Args:
            expression: The arithmetic expression string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                parentheses, invalid characters, division by zero).
            TypeError: If input is not a string

        ISO/IEC 25010 Considerations (within this method and other methods):
            - Correctness:  Thorough handling of operator precedence, parentheses,
                           and various number types (integers, floats, negatives).
            - Performance:  Uses the shunting yard algorithm which is efficient for parsing
            - Modularity: Calculation logic segmented for operations, parsing
            - Security:  No use of eval(). Input validation to prevent injection.
            - Testability:  Methods are self-contained and logically distinct to facilitate testing
            - Readability: Docstrings, clear naming, and concise code improve readability
        """

        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        try:
            tokens = self._tokenize(expression)
            postfix_tokens = self._shunting_yard(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except ZeroDivisionError:
            raise ValueError("Division by zero encountered.")
        except (ValueError, TypeError) as e:  # Catch other potential errors during parsing and evaluation
            raise ValueError(f"Invalid expression: {e}")

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the input expression string.

        Args:
            expression: The arithmetic expression string.

        Returns:
            A list of tokens (numbers, operators, parentheses).

        Raises:
            ValueError: If there is an invalid character in the expression.
        """
        # Regular expression improved to capture:
        # - Leading plus/minus signs for numbers (e.g., -1, +2)
        # - Multi-digit numbers with or without decimals
        # - Operators and parentheses as separate tokens
        token_pattern = r"(-?\d+\.?\d*|\+|-|\*|/|\(|\))"  # +? is handled correctly now

        tokens = re.findall(token_pattern, expression)

        # Validate for the unexpected characters:
        allowed_chars = r"^[0-9+\-*/().\s-]+$"
        if not re.match(allowed_chars, expression):
            raise ValueError("Invalid characters in expression.")

        # Remove spaces, handle consecutive + and -:
        cleaned_tokens = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.isspace(): # skip space token
                i+=1
                continue
            if token in ('+', '-'):
                if i == 0 or (i > 0 and tokens[i-1] in ('(', '*', '/', '+', '-')):
                    # Handle unary plus/minus by combining it with the next token.
                    if i + 1 < len(tokens) and re.match(r"^\d+\.?\d*$", tokens[i+1]):
                        cleaned_tokens.append(token + tokens[i+1])
                        i += 2  # Skip the next token, as we've combined it
                        continue
                    else:
                        # If not followed by a number, it's an error unless it's like (+ or (-
                        if i + 1 < len(tokens) and tokens[i+1] not in ('(',):
                            raise ValueError(f"Invalid use of operator '{token}'.")
            cleaned_tokens.append(token)
            i += 1


        return cleaned_tokens

    def _shunting_yard(self, tokens: list) -> list:
        """
        Converts the tokenized expression to postfix notation (Reverse Polish Notation)
        using the Shunting Yard algorithm.

        Args:
            tokens: A list of tokens.

        Returns:
            A list of tokens in postfix notation.

        Raises:
          ValueError: For unbalanced parentheses.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        operator_stack = []

        for token in tokens:
            if re.match(r"^-?\d+\.?\d*$", token):  # Check for numbers (including negative numbers)
                output_queue.append(float(token))  # Convert to float here
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                try:
                    while operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    operator_stack.pop()  # Remove the '('
                except IndexError:  # Empty stack means unbalanced parentheses
                    raise ValueError("Unbalanced parentheses: Mismatched ')'")
            else:
                raise ValueError(f"Invalid token during shunting yard: {token}")


        while operator_stack:
            if operator_stack[-1] == '(':  # Check for unclosed '('
                raise ValueError("Unbalanced parentheses: Unclosed '('")
            output_queue.append(operator_stack.pop())

        return output_queue

    def _evaluate_postfix(self, postfix_tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            postfix_tokens: A list of tokens in postfix notation.

        Returns:
            The result of the expression.

        Raises:
            ValueError: If the expression contains division by zero and for malformed expressions.

        """
        operand_stack = []

        for token in postfix_tokens:
            if isinstance(token, float):  # Check if it's a number (already converted to float)
                operand_stack.append(token)
            else:  # It's an operator
                try:
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                except IndexError:
                    raise ValueError("Malformed postfix expression (not enough operands).")

                if token == '+':
                    operand_stack.append(operand1 + operand2)
                elif token == '-':
                    operand_stack.append(operand1 - operand2)
                elif token == '*':
                    operand_stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero")  # Explicitly raise ZeroDivisionError
                    operand_stack.append(operand1 / operand2)

        if len(operand_stack) != 1:
            raise ValueError("Malformed postfix expression (too many operands).")

        return operand_stack[0]



def main():
    """
    Main function to run the calculator in a console loop.
    """
    calculator = Calculator()

    while True:
        try:
            expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print("Result:", result)
        except ValueError as e:
            print("Error:", e)
        except TypeError as e:
            print("Error", e)


if __name__ == "__main__":
    main()
