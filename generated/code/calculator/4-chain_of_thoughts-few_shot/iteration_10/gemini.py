class Calculator:
    """
    A console-based arithmetic calculator that supports basic operations,
    parentheses, and decimal/negative numbers.  Adheres to principles
    of ISO/IEC 25010 for software quality.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, division by zero).
            TypeError: If input is not a string
        """
        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        normalized_expression = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expression):
            raise ValueError("Unbalanced parentheses.")

        return self._evaluate_expression(normalized_expression)


    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression.
          - Removes spaces.
          - Validates characters.

        Args:
            expression (str): The mathematical expression.

        Returns:
            str: The normalized expression.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if parentheses in the expression are balanced.

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
        return not stack  # True if stack is empty (all balanced)


    def _evaluate_expression(self, expression: str) -> float:
        """
        Evaluates a normalized mathematical expression using a modified
        Shunting Yard algorithm.

        Args:
            expression (str):  The normalized mathematical expression.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If there's a division by zero.
        """
        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isdigit() or (char == '-' and (i == 0 or expression[i-1] in '+-*/(')):
                # Handle numbers (including decimals and negatives)
                j = i
                num_str = ""
                if char == '-':  # Negative sign handling
                    num_str += '-'
                    j += 1
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    num_str += expression[j]
                    j += 1

                if num_str.count('.') > 1:   # Check that number contains no more that 1 dot character
                    raise ValueError(f'Invalid number format:  {num_str}')

                output_queue.append(float(num_str))
                i = j - 1  # Adjust index after number parsing

            elif char in precedence:
                # Handle operators
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], 0) >= precedence.get(char, 0)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(char)

            elif char == '(':
                # Handle opening parenthesis
                operator_stack.append(char)

            elif char == ')':
                # Handle closing parenthesis
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Discard the '('
                else:
                     raise ValueError("Unbalanced parentheses") # Extra closing parenthesis
            i += 1

        # Pop any remaining operators from the stack
        while operator_stack:
            if operator_stack[-1] == '(':  # Check in case of missing closing parenthesis
                raise ValueError("Unbalanced parentheses")
            output_queue.append(operator_stack.pop())


        # Evaluate the postfix expression (Reverse Polish Notation)
        evaluation_stack = []
        for token in output_queue:
            if isinstance(token, float):
                evaluation_stack.append(token)
            else:  # It's an operator
                try:
                    operand2 = evaluation_stack.pop()
                    operand1 = evaluation_stack.pop()
                except IndexError:
                    raise ValueError("Invalid expression format.") # Not enough operands for operators.

                if token == '+':
                    evaluation_stack.append(operand1 + operand2)
                elif token == '-':
                    evaluation_stack.append(operand1 - operand2)
                elif token == '*':
                    evaluation_stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ValueError("Division by zero.")
                    evaluation_stack.append(operand1 / operand2)

        if len(evaluation_stack) != 1: # Check for invalid format
            raise ValueError("Invalid expression format")
        return evaluation_stack[0]


class Calculator:
    """
    A console-based arithmetic calculator that supports basic operations,
    parentheses, and decimal/negative numbers.  Adheres to principles
    of ISO/IEC 25010 for software quality.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, division by zero).
            TypeError: If input is not a string
        """
        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        normalized_expression = self._normalize_expression(expression)
        if not self._is_balanced(normalized_expression):
            raise ValueError("Unbalanced parentheses.")

        return self._evaluate_expression(normalized_expression)

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression.
          - Removes spaces.
          - Validates characters.

        Args:
            expression (str): The mathematical expression.

        Returns:
            str: The normalized expression.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")

        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if parentheses in the expression are balanced.

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
        return not stack  # True if stack is empty (all balanced)

    def _evaluate_expression(self, expression: str) -> float:
        """
        Evaluates a normalized mathematical expression using a modified
        Shunting Yard algorithm.

        Args:
            expression (str):  The normalized mathematical expression.

        Returns:
            float: The result of the evaluation.

        Raises:
            ValueError: If there's a division by zero.
        """
        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isdigit() or (char == '-' and (i == 0 or expression[i-1] in '+-*/(')):
                # Handle numbers (including decimals and negatives)
                j = i
                num_str = ""
                if char == '-':  # Negative sign handling
                    num_str += '-'
                    j += 1
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    num_str += expression[j]
                    j += 1

                if num_str.count('.') > 1:   # Check that number contains no more that 1 dot character
                    raise ValueError(f'Invalid number format:  {num_str}')

                output_queue.append(float(num_str))
                i = j - 1  # Adjust index after number parsing

            elif char in precedence:
                # Handle operators
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], 0) >= precedence.get(char, 0)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(char)

            elif char == '(':
                # Handle opening parenthesis
                operator_stack.append(char)

            elif char == ')':
                # Handle closing parenthesis
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Discard the '('
                else:
                     raise ValueError("Unbalanced parentheses") # Extra closing parenthesis
            i += 1

        # Pop any remaining operators from the stack
        while operator_stack:
            if operator_stack[-1] == '(':  # Check in case of missing closing parenthesis
                raise ValueError("Unbalanced parentheses")
            output_queue.append(operator_stack.pop())


        # Evaluate the postfix expression (Reverse Polish Notation)
        evaluation_stack = []
        for token in output_queue:
            if isinstance(token, float):
                evaluation_stack.append(token)
            else:  # It's an operator
                try:
                    operand2 = evaluation_stack.pop()
                    operand1 = evaluation_stack.pop()
                except IndexError:
                    raise ValueError("Invalid expression format.") # Not enough operands for operators.

                if token == '+':
                    evaluation_stack.append(operand1 + operand2)
                elif token == '-':
                    evaluation_stack.append(operand1 - operand2)
                elif token == '*':
                    evaluation_stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ValueError("Division by zero.")
                    evaluation_stack.append(operand1 / operand2)

        if len(evaluation_stack) != 1: # Check for invalid format
            raise ValueError("Invalid expression format")
        return evaluation_stack[0]
# Example usage
if __name__ == "__main__":
    calculator = Calculator()

    while True:
        try:
            expression = input("Enter a mathematical expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print("Result:", result)
        except ValueError as e:
            print("Error:", e)
        except TypeError as e:
            print("Error:", e)
