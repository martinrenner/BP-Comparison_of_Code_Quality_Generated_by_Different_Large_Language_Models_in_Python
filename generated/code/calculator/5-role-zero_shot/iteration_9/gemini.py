import re


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, parentheses, and operator precedence.  It handles
    both integers and floating-point numbers.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression and returns the result.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                parentheses, invalid characters, division by zero).
        """
        # Pre-process: Remove whitespace to handle spaces gracefully
        expression = expression.replace(" ", "")

        # Validate input
        self._validate_expression(expression)

        # Tokenize the expression
        tokens = self._tokenize(expression)

        # Convert to postfix notation (Reverse Polish Notation)
        postfix_tokens = self._infix_to_postfix(tokens)

        # Evaluate the postfix expression
        result = self._evaluate_postfix(postfix_tokens)

        return result

    def _validate_expression(self, expression: str):
        """Validates the input expression for common errors."""

        # Check for invalid characters
        if not re.match(r"^[\d+\-*/().-]+$", expression):
            raise ValueError("Invalid characters in expression.")

        # Check for unbalanced parentheses
        paren_balance = 0
        for char in expression:
            if char == '(':
                paren_balance += 1
            elif char == ')':
                paren_balance -= 1
            if paren_balance < 0:
                raise ValueError("Unbalanced parentheses (too many closing).")
        if paren_balance != 0:
            raise ValueError("Unbalanced parentheses (too many opening).")

        # Check for consecutive operators (e.g., "++" or "*-")  excluding valid cases like "+-", "-+" (sign after operator).
        if re.search(r"([+\-*/])\s*([*/+])", expression) or re.search(r"[/]\s*[-]", expression) or re.search(r"([*])\s*([*])", expression):
            raise ValueError("Invalid consecutive operators.")
        
        # Simple check for division by zero at the beginning
        if re.match(r"^[0.]+/0", expression):
           raise ValueError("Division by zero.")

        return


    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the expression string into a list of tokens.

        Args:
            expression: The expression string.

        Returns:
            A list of tokens (numbers, operators, parentheses).
        """
        return re.findall(r"(\d+\.\d+|\d+|[+\-*/()])", expression)
        # Improved regex above. Handles floating point numbers correctly.


    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts a list of tokens from infix notation to postfix notation
        (Reverse Polish Notation).

        Args:
            tokens: The list of tokens in infix notation.

        Returns:
            A list of tokens in postfix notation.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r'\d+(\.\d+)?', token):  # Check if it's a number (integer or float)
                output.append(float(token))  # Convert to float directly
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if not operator_stack:
                  raise ValueError("Mismatched Parentheses")
                operator_stack.pop()  # Pop the '('
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)

        while operator_stack:
            if operator_stack[-1] == '(':
              raise ValueError("Mismatched Parentheses")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a list of tokens in postfix notation.

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
                    raise ValueError("Invalid expression (not enough operands).")
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
                        raise ValueError("Division by zero.")
                    stack.append(operand1 / operand2)


        if len(stack) != 1:
            raise ValueError("Invalid expression (too many operands).")

        return stack.pop()



def main():
    """Main function to run the calculator."""
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
        except Exception as e:
          print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
