class Calculator:
    """
    A console-based arithmetic calculator that evaluates expressions.

    This class implements a calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It follows the correct order
    of operations and handles various error conditions.
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
        """
        try:
            normalized_expression = self._normalize_expression(expression)
            if not self._is_balanced(normalized_expression):
                raise ValueError("Unbalanced parentheses.")
            tokens = self._tokenize(normalized_expression)
            postfix_tokens = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix_tokens)
            return result
        except ZeroDivisionError:
            raise ValueError("Division by zero.")
        except ValueError as e:
            raise ValueError(f"Invalid expression: {e}")
        except Exception as e:
             raise ValueError(f"An unexpected error occurred: {e}")

    def _normalize_expression(self, expression: str) -> str:
        """
        Normalizes a mathematical expression by removing whitespaces and
        validating characters to prevent unexpected issues.

        Args:
            expression (str): The mathematical expression.

        Returns:
            str: Normalized expression.

        Raises:
              ValueError: If input contains invalid characters.
        """
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")
        return expression.replace(" ", "")

    def _is_balanced(self, expression: str) -> bool:
        """
        Verifies balanced parentheses within an expression to maintain
        syntactical correctness.

        Args:
            expression (str): Expression to check.

        Returns:
            bool: Parentheses are balanced (True) or not (False)
        """
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        return not stack  # Stack should be empty if balanced

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes a normalized mathematical expression.

        Args:
            expression (str): The normalized expression.

        Returns:
            list: A list of tokens (numbers, operators, parentheses).
        """
        tokens = []
        current_number = ""
        for char in expression:
            if char.isdigit() or char == '.':
                current_number += char
            else:
                if current_number:
                    tokens.append(current_number)
                    current_number = ""
                tokens.append(char)
        if current_number:
            tokens.append(current_number)
        return tokens

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts an infix expression (list of tokens) to postfix notation.

        Args:
            tokens (list): The list of tokens in infix notation.

        Returns:
            list: The list of tokens in postfix notation.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if token.replace('.', '', 1).lstrip('-').isdigit():  # Check if it's a number
                output.append(float(token))
            elif token in precedence:
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
            else:
                raise ValueError(f"Invalid token: {token}")


        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a postfix expression.

        Args:
            tokens (list): The list of tokens in postfix notation.

        Returns:
            float: The result of the evaluation.
        """
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")
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
                        raise ZeroDivisionError("Division by zero")
                    stack.append(operand1 / operand2)
                else:
                    raise ValueError(f"Invalid operator: {token}")
        if len(stack) != 1:
             raise ValueError("Invalid expression: too many operands")       
        return stack.pop()

# Example usage (and basic testing):
if __name__ == "__main__":
    calculator = Calculator()

    test_cases = [
      ("2 + 2", 4.0),
      ("10 - 5", 5.0),
      ("3 * 4", 12.0),
      ("20 / 5", 4.0),
      ("2 + 3 * 4", 14.0),
      ("(2 + 3) * 4", 20.0),
      ("10 / (2 + 3)", 2.0),
      ("1 + 2 * (3 + 4) / 2 - 1", 7.0),
      ("-5 + 2", -3.0),
      ("2.5 * 4", 10.0),
      ("10 / 2.5", 4.0),
      ("   1 + 2  ", 3.0),  # Whitespace handling
      ("2+(3*4)", 14.0),  # Test for combined operations
      ("2+3*4/2", 8.0),   # Test for precedence handling
      ("2.5 + 3.5", 6.0), # Decimal addition test
      ("4-6", -2.0),   #Test case for negative result.
      ("4*6-10/5",22.0), #Test case for combine operations with precedence.
      ("(4*6)-10/5",22.0), #Test case with parentheses.
      ("2*-3", -6.0),
      ("(-5+2)*3",-9.0),
      (".1 * 5", 0.5),
      ("5 * -.1", -0.5)
    ]

    error_cases = [
        "2 ++ 2",
        "10 / 0",
        "2 + (3 * 4",
        ")2 + 2(",
        "2 + a",
        "2 & 2",
        "3 + * 4",   #Missing Operand
        "3+4)+2", #Extra closing parantheses
        "10/(5-5)", #Division by zero
        "2+-*/3" #Multiple operators together

    ]

    all_passed = True
    for expression, expected in test_cases:
        try:
            result = calculator.calculate(expression)
            if result != expected:
                print(f"FAIL: Expression '{expression}', Expected: {expected}, Got: {result}")
                all_passed = False
        except Exception as e:
            print(f"FAIL (Unexpected Error): Expression '{expression}', Error: {e}")
            all_passed = False


    for expression in error_cases:
        try:
            calculator.calculate(expression)
            print(f"FAIL: Expression '{expression}' should have raised an error.")
            all_passed = False
        except ValueError:
            pass  # Expected error
        except Exception as e:
            print(f"FAIL (Wrong Error Type):Expression '{expression}',Error: {e}")
            all_passed = False
            
    if all_passed:
        print("All test cases passed!")
    
     #Interactive usage
    while True:
        user_input = input("Enter a mathematical expression (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        try:
            result = calculator.calculate(user_input)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")


