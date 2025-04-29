import re


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It handles operator precedence
    and both integer and floating-point numbers.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression and returns the result.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
        """

        # 1. Input Validation & Preprocessing
        expression = expression.replace(" ", "")  # Remove spaces
        if not self._is_valid_expression(expression):
            raise ValueError("Invalid characters in expression.")

        if not self._are_parentheses_balanced(expression):
            raise ValueError("Unbalanced parentheses.")

        # 2. Tokenization
        tokens = self._tokenize(expression)

        # 3. Shunting Yard Algorithm (Convert Infix to Postfix)
        postfix_tokens = self._shunting_yard(tokens)

        # 4. Evaluation of Postfix Expression
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _is_valid_expression(self, expression: str) -> bool:
        """Checks if the expression contains only valid characters."""
        return bool(re.match(r"^[\d\+\-\*\/\(\)\.]+$", expression))

    def _are_parentheses_balanced(self, expression: str) -> bool:
        """Checks if parentheses in the expression are balanced."""
        count = 0
        for char in expression:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
            if count < 0:
                return False  # More closing than opening parentheses
        return count == 0

    def _tokenize(self, expression: str) -> list:
        """
        Converts the expression string into a list of tokens.
        Handles multi-digit numbers (integers and floats) and negative numbers.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isdigit() or (char == '.' and i + 1 < len(expression) and expression[i+1].isdigit()):  # Handle floats
                j = i
                num_str = ""
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    num_str += expression[j]
                    j += 1

                # Handle edge case: decimal at the very end. Should not happen in valid expressions
                if num_str.endswith('.'):
                    raise ValueError(f"Invalid decimal number format at position {i}.")

                tokens.append(float(num_str))  # Store as float
                i = j - 1  # Adjust index

            # Handling negative numbers. This also handles subsequent negative values.
            elif char == '-' and (i == 0 or expression[i-1] in '+-*/('):  # Negative number
                if i + 1 < len(expression) and (expression[i+1].isdigit() or expression[i+1] =='.'): # Next is digit or a '.'
                   j = i + 1
                   num_str = "-"
                   while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                        num_str += expression[j]
                        j += 1
                   # Handle edge case: decimal at the very end.
                   if num_str.endswith('.'):
                       raise ValueError(f"Invalid decimal number format at position {i}.")
                   tokens.append(float(num_str))
                   i = j - 1  # Corrected index

                else: # Invalid use of "-"
                    raise ValueError(f"Invalid use of '-' operator, the next char is not a digit. position: {i}")

            elif char in '+-*/()':
                tokens.append(char)
            else:
                # This should ideally never hit because _is_valid_expression checks first
                raise ValueError(f"Invalid character '{char}' at position {i}")
            i += 1
        return tokens
    def _shunting_yard(self, tokens: list) -> list:
        """
        Converts the infix token list to postfix using the Shunting Yard algorithm.

        Args:
            tokens: The list of tokens in infix notation.

        Returns:
            A list of tokens in postfix notation.
        """
        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")  # Should not happen if _are_parentheses_balanced is called
                operator_stack.pop()  # Pop the '('

        while operator_stack:
            if operator_stack[-1] == '(':  # Should also not happen if _are_parentheses_balanced is called
                 raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())

        return output_queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            tokens: The list of tokens in postfix notation.

        Returns:
            The result of the evaluation.

        Raises:
            ValueError: If division by zero is attempted.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands.")
                operand2 = stack.pop()
                operand1 = stack.pop()
                if token == '+':
                    stack.append(operand1 + operand2)
                elif token == '-':
                    stack.append(operand1 - operand2)
                elif token == '*':
                    stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ValueError("Division by zero")
                    stack.append(operand1 / operand2)
        if len(stack) != 1:
            raise ValueError("Invalid expression, result should be a single value.")

        return stack[0]


def main():
    """Main function to run the calculator."""
    calculator = Calculator()
    while True:
        try:
            expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

