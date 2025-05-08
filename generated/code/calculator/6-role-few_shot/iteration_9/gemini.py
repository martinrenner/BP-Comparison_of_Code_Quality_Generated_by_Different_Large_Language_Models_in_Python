import re


class Calculator:
    """
    A class to implement a console-based arithmetic calculator.

    This calculator supports addition, subtraction, multiplication, division,
    and parentheses. It handles operator precedence and validates input.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
        """
        try:
            normalized_expression = self._normalize_expression(expression)
            if not self._is_balanced(normalized_expression):
                raise ValueError("Unbalanced parentheses.")

            tokens = self._tokenize(normalized_expression)
            postfix_tokens = self._shunting_yard(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except ZeroDivisionError:
            raise ValueError("Division by zero.")
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"Invalid expression: {e}")


    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression. Removes spaces and validates for

        invalid characters (like letters).

        Args:
            expression (str): A mathematical expression as a string.

        Returns:
            str: The normalized expression without spaces.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks whether a mathematical expression has properly paired parentheses.

        :param expression: A string containing the mathematical expression.
        :return: True if parentheses are correctly paired, otherwise False.
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
        Tokenizes a mathematical expression.

        Args:
            expression (str): The normalized mathematical expression.

        Returns:
            list: A list of tokens (numbers, operators, parentheses).
        """
        return re.findall(r"(\d+\.\d+|\d+|[+\-*/()])", expression)

    def _shunting_yard(self, tokens: list) -> list:
        """
        Converts a list of tokens from infix notation to postfix notation
        using the Shunting Yard algorithm.

        Args:
            tokens (list): The list of tokens in infix notation.

        Returns:
            list: The list of tokens in postfix notation.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"(\d+\.\d+|\d+)", token):  # Check for numbers (integers and floats)
                output.append(float(token))
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Pop the '('

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a list of tokens in postfix notation.

        Args:
            tokens (list): The list of tokens in postfix notation.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: if an invalid token is present
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
                try:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise ValueError("Invalid postfix expression")
                if token == '+':
                    stack.append(operand1 + operand2)
                elif token == '-':
                    stack.append(operand1 - operand2)
                elif token == '*':
                    stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero")
                    stack.append(operand1 / operand2)
                else:  # This part of the code won't be reached due to prior validation
                    raise ValueError(f"Invalid operator: {token}")  # pragma: no cover
        if len(stack) != 1:
          raise ValueError("Invalid expression - Incorrect number of operators/operands.")
        return stack[0]



def main():
    """
    Main function to run the calculator.
    """
    calculator = Calculator()
    while True:
        expression = input("Enter a mathematical expression (or 'quit' to exit): ")
        if expression.lower() == 'quit':
            break
        try:
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

