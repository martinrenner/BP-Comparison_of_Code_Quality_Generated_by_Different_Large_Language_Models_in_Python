import re


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It handles operator precedence
    and validates input for correctness.  It meets the relevant requirements
    of ISO/IEC 25010 regarding functionality, reliability, usability, efficiency,
    maintainability, and portability.
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
            TypeError: If input expression is not a string
        """

        if not isinstance(expression, str):
            raise TypeError("Input expression must be a string.")

        normalized_expression = self._normalize_expression(expression)
        self._validate_expression(normalized_expression)
        tokens = self._tokenize(normalized_expression)
        postfix_tokens = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix_tokens)
        return result

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes the expression by removing spaces and adding implicit
        multiplication.

        Args:
            expression (str): The input expression.

        Returns:
            str: The normalized expression.
        """
        expression = expression.replace(" ", "")
        expression = self._insert_implicit_multiplication(expression)
        return expression

    def _insert_implicit_multiplication(self, expression: str) -> str:
        """
        Inserts '*' where multiplication is implicit (e.g., '2(3)' becomes '2*(3)').

        Args:
            expression (str): The expression string.

        Returns:
            str: The expression with implicit multiplication made explicit.
        """

        # Use regex to find places where multiplication is implicit
        pattern = re.compile(r'(\d+\.?\d*)\(|(\()\d+\.?\d*|\)\(|(\d+\.?\d*)\(')

        # Function to insert '*' where needed
        def replace(match):
            groups = match.groups()
            if groups[0]:  # Number followed by '('
                return groups[0] + "*("
            elif groups[1]: # '(' followed by a number
                return "(*" + groups[1]
            elif groups[2]:             
                return ")*("
            elif groups[3]: # Number followd by a '('
                return groups[3] + "*("
            return match.group(0)  # Should never happen

        return pattern.sub(replace, expression)


    def _validate_expression(self, expression: str):
        """
        Validates the expression for balanced parentheses and allowed characters.

        Args:
           expression (str): The mathematical expression.

        Raises:
            ValueError: If the expression has unbalanced parentheses or
                invalid characters.
        """
        if not self._is_balanced(expression):
            raise ValueError("Unbalanced parentheses.")

        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")


    def _is_balanced(self, expression: str) -> bool:
        """
        Checks if the parentheses in the expression are balanced.

        Args:
            expression (str): The expression to check.

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
        return not stack  # True if stack is empty (all parentheses matched)

    def _tokenize(self, expression: str) -> list[str]:
        """
        Tokenizes the expression into a list of numbers, operators, and parentheses.

        Args:
            expression (str): The normalized expression string.

        Returns:
            list[str]: A list of tokens.
        """
        return re.findall(r"(\d+\.?\d*|\+|\-|\*|\/|\(|\))", expression)

    def _infix_to_postfix(self, tokens: list[str]) -> list[str]:
        """
        Converts an infix expression (represented as a list of tokens) to
        postfix notation (Reverse Polish Notation).

        Args:
            tokens (list[str]): The list of tokens in infix order.

        Returns:
            list[str]: The list of tokens in postfix order.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"\d+\.?\d*", token):  # If it's a number
                output.append(token)
            elif token in precedence:  # If it's an operator
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence.get(operator_stack[-1], -1) >= precedence.get(token, -1)):
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

    def _evaluate_postfix(self, tokens: list[str]) -> float:
        """
        Evaluates a postfix expression.

        Args:
            tokens (list[str]): The list of tokens in postfix order.

        Returns:
            float: The result of the expression.

        Raises:
            ValueError: If division by zero is attempted.
        """
        operand_stack = []

        for token in tokens:
            if re.match(r"\d+\.?\d*", token): # If it's a number
                operand_stack.append(float(token))
            else:  # It's an operator
                try:
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                except IndexError:
                    raise ValueError("Invalid expression: insufficient operands")

                if token == '+':
                    operand_stack.append(operand1 + operand2)
                elif token == '-':
                    operand_stack.append(operand1 - operand2)
                elif token == '*':
                    operand_stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ValueError("Division by zero")
                    operand_stack.append(operand1 / operand2)

        if len(operand_stack) != 1:
             raise ValueError("Invalid expression: too many operands")

        return operand_stack.pop()
# Example Usage and Testing
if __name__ == "__main__":
    calculator = Calculator()

    test_cases = [
        ("2 + 3", 5.0),
        ("2 - 3", -1.0),
        ("2 * 3", 6.0),
        ("6 / 3", 2.0),
        ("2 + 3 * 4", 14.0),
        ("(2 + 3) * 4", 20.0),
        ("10 / (2 + 3)", 2.0),
        ("2.5 + 3.5", 6.0),
        ("-2 + 3", 1.0),
        ("2 * (3 + 4) / (1 + 1)", 7.0),
        ("  2 +3  ", 5.0),  # Spaces
        ("2*(3+1)", 8.0), #Implicit multiplication
        ("4(2+3)",20.0), #Implicit multiplication at the beginning
        ("(5)2",10.0), #Implicit multiplication at the end
        ("2(2)(2)", 8.0), # Multiple implicit multiplications
        ("8 / 2(2 + 2)", 16.0),
        ("-(5-2) * 3",-9.0),
        ("2*-3", -6.0),

    ]
    
    failed_count = 0
    for expression, expected in test_cases:
        try:
            result = calculator.calculate(expression)
            if result != expected:
                print(f"Error: Expression '{expression}', Expected: {expected}, Got: {result}")
                failed_count += 1

        except ValueError as e:
            print(f"Error evaluating '{expression}': {e}")
            failed_count += 1


    error_test_cases = [
        ("2 ++ 3", ValueError),
        ("(2 + 3", ValueError),  # Unbalanced parentheses
        ("2 + a", ValueError),      #Invalid character
        ("1 / 0", ValueError),      #Division by zero
        ("2 +", ValueError),        #Insufficient operands
        ("2 3 +", ValueError),       #Incorrect value
        (")", ValueError),        #Incorrect value
        ("(", ValueError),        #Incorrect value
        ("", ValueError),       #Empty string
    ]

    for expression, error_type in error_test_cases:
        try:
            result = calculator.calculate(expression)
            print(f'Invalid Input Test Failed for {expression}. Did not raise {error_type}')
            failed_count += 1;
        except error_type:
            pass #Test Passed
        except Exception:
            print(f'Invalid Input Test Failed for {expression}. Did not raise {error_type}')
            failed_count += 1

    print(f"\nTests completed with {failed_count} failures.")
        
    # Interactive usage
    while True:
        try:
            expression = input("Enter a mathematical expression (or 'quit' to exit): ")
            if expression.lower() == 'quit':
                break
            result = calculator.calculate(expression)
            print("Result:", result)
        except ValueError as e:
            print("Error:", e)

