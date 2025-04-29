import re


class Calculator:
    """
    A class to represent a console-based arithmetic calculator.

    This calculator supports addition, subtraction, multiplication, division,
    parentheses, and handles operator precedence. It accepts both integers and
    floating-point numbers (including negative values).
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the given arithmetic expression.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                parentheses, invalid characters, division by zero).
        """
        try:
            expression = self._clean_expression(expression)
            self._validate_expression(expression)
            return self._evaluate(expression)
        except ZeroDivisionError:
            raise ValueError("Division by zero error.")
        except (ValueError, IndexError) as e:  # Catching IndexError for stack-related issues.
            raise ValueError(f"Invalid expression: {e}")

    def _clean_expression(self, expression: str) -> str:
        """Removes whitespace and ensures consistent formatting."""
        expression = expression.replace(" ", "")
        return expression


    def _validate_expression(self, expression: str):
        """
        Validates the input expression.  Checks for balanced parentheses,
        invalid characters, and consecutive operators.

        Raises:
            ValueError: If the expression is invalid.
        """

        # Check for balanced parentheses
        paren_count = 0
        for char in expression:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            if paren_count < 0:
                raise ValueError("Unbalanced parentheses.")
        if paren_count != 0:
            raise ValueError("Unbalanced parentheses.")

        # Check for invalid characters using regular expressions
        if not re.match(r"^[0-9+\-*/().-]+$", expression):
            raise ValueError("Invalid characters in expression.")

        # Check for consecutive operators (e.g., "++", "+-", etc.)
        if re.search(r"([+\-*/][+\-*/])", expression):
            raise ValueError("Consecutive operators are not allowed.")

         # Check for operators at the beginning or end.
        if re.match(r"^[*/]", expression) or re.match(r".*[+\-*/]$", expression):
            raise ValueError("Expression cannot start or end with an operator (* or / at the start, any at the end).")
        
        # Check for empty parentheses
        if "()" in expression:
            raise ValueError("Empty parentheses are not allowed")
        


    def _evaluate(self, expression: str) -> float:
        """
        Evaluates the expression using a stack-based approach
        to handle operator precedence and parentheses.

        Args:
            expression: The cleaned and validated arithmetic expression.

        Returns:
            The result of the evaluation.
        """
        tokens = self._tokenize(expression)
        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if isinstance(token, (int, float)):
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
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Pop the '('

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())

        return self._evaluate_postfix(output_queue)


    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the expression string into a list of numbers, operators,
        and parentheses.  Handles multi-digit numbers and floating-point numbers.

        Args:
            expression: The arithmetic expression string.

        Returns:
            A list of tokens.
        """
        tokens = []
        current_number = ""
        for char in expression:
            if char.isdigit() or char == '.':
                current_number += char
            elif char in ('+', '-', '*', '/', '(', ')'):
                if current_number:
                    try:
                        tokens.append(float(current_number) if '.' in current_number else int(current_number))
                    except ValueError:
                        raise ValueError(f"Invalid number: {current_number}")

                    current_number = ""
                tokens.append(char)
        if current_number:
            try:
                tokens.append(float(current_number) if '.' in current_number else int(current_number))
            except ValueError:
             raise ValueError(f"Invalid number: {current_number}")

        # Handle unary minus/plus
        modified_tokens = []
        prev_token = None
        
        for i, token in enumerate(tokens):
            if token == '-' or token == '+':
                if i == 0 or (prev_token and prev_token in ('+', '-', '*', '/', '(')):
                  if token == '-':
                    modified_tokens.append(-1)
                    modified_tokens.append('*')
                  # else: We can ignore it
                else:
                    modified_tokens.append(token)
            else:
              modified_tokens.append(token)
            prev_token = token

        return modified_tokens


    def _evaluate_postfix(self, postfix_expression: list) -> float:
        """
        Evaluates a postfix expression (Reverse Polish Notation).

        Args:
            postfix_expression: The expression in postfix notation as a list.

        Returns:
            The result of the evaluation.
        """
        stack = []
        for token in postfix_expression:
            if isinstance(token, (int, float)):
                stack.append(token)
            else:
                try:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                except IndexError:
                    raise ValueError("Invalid postfix expression structure. Not enough operands.")

                if token == '+':
                    stack.append(operand1 + operand2)
                elif token == '-':
                    stack.append(operand1 - operand2)
                elif token == '*':
                    stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero.")
                    stack.append(operand1 / operand2)
                else:  # Should never reach here due to validation
                    raise ValueError(f"Unknown operator {token}")
        
        if len(stack) != 1:
          raise ValueError("Invalid postfix expression structure. Too many operands")
        return stack.pop()



def main():
    """
    Main function to run the calculator in a loop.
    """
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

