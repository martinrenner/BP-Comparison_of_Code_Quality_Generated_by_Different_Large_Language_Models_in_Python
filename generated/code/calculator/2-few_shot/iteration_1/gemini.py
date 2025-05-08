import re  # Used for efficient splitting of the expression

class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions with
    addition, subtraction, multiplication, division, and parentheses.  It
    adheres to operator precedence and handles both integer and floating-point
    numbers.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the expression.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                parentheses, invalid characters, division by zero).
            TypeError:  If expression is not a string.
        """

        if not isinstance(expression, str):
            raise TypeError("Expression must be a string.")

        normalized_expression = self._normalize_expression(expression)
        self._validate_parentheses(normalized_expression)

        try:
            result = self._evaluate(normalized_expression)
            return float(result)  # Ensure float return
        except ZeroDivisionError:
            raise ValueError("Division by zero encountered.")
        except (SyntaxError, ValueError) as e:
            raise ValueError(f"Invalid expression: {e}")


    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression by removing spaces and validating characters.

        Args:
            expression (str):  Input mathematical expression.

        Returns:
            str: Normalized expression (spaces removed).

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")


    def _validate_parentheses(self, expression: str) -> None:
        """
        Validates that parentheses in the expression are balanced.

        Args:
            expression (str): The expression to validate.

        Raises:
            ValueError: If parentheses are unbalanced.
        """
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise ValueError("Unbalanced parentheses: unmatched ')'")
                stack.pop()
        if stack:
            raise ValueError("Unbalanced parentheses: unmatched '('")

    def _evaluate(self, expression: str) -> float:
        """
        Evaluates a normalized mathematical expression using the Shunting Yard algorithm.

        Args:
            expression: The normalized mathematical expression.

        Returns:
            The result of the evaluation.
        
        Raises:
             ValueError: On division by zero
        """

        tokens = re.findall(r"(\b\d+\.\d+|\b\d+|[+\-*/()])", expression) # Tokenize, keeps floats together
        
        output_queue = []
        operator_stack = []

        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if re.match(r"(\b\d+\.\d+|\b\d+)", token):  # Check for numbers (integers and floats).
                output_queue.append(float(token)) # Convert to float immediately
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise SyntaxError("Mismatched parentheses") # Should not happen, but good to check
                operator_stack.pop()  # Remove the '('

        while operator_stack:
            if operator_stack[-1] == '(': #  Handle unmatched opening parenthesis.
                raise SyntaxError("Mismatched parentheses")  # Should technically be caught earlier
            output_queue.append(operator_stack.pop())

        return self._evaluate_postfix(output_queue)

    def _evaluate_postfix(self, postfix_expression: list) -> float:
        """
        Evaluates a postfix (Reverse Polish Notation) expression.

        Args:
            postfix_expression: The expression in postfix notation.

        Returns:
            The result of the evaluation.

        Raises:
            ValueError: If there is division by zero.
        """

        stack = []
        for token in postfix_expression:
            if isinstance(token, float):
                stack.append(token)
            else:
                try:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise SyntaxError("Invalid expression: insufficient operands")

                if token == '+':
                    stack.append(operand1 + operand2)
                elif token == '-':
                    stack.append(operand1 - operand2)
                elif token == '*':
                    stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero") #  Explicitly check here.
                    stack.append(operand1 / operand2)

        if len(stack) != 1:
            raise SyntaxError("Invalid expression: too many operands") #  Not enough operators.
        return stack[0]
def main():
    """
    Main function to run the calculator in a loop.
    """
    calculator = Calculator()
    while True:
        try:
            expression = input("Enter a mathematical expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")
        except TypeError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
