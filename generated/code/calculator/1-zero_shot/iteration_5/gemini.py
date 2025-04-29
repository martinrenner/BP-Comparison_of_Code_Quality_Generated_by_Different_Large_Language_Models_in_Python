import re


class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses.  It adheres to standard operator
    precedence and handles both integer and floating-point numbers.  The design
    emphasizes correctness, performance, modularity, security, testability,
    readability, and maintainability, aligning with aspects of ISO/IEC 25010.
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression and returns the result.

        Args:
            expression: The mathematical expression as a string.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced
                        parentheses, invalid characters, division by zero, 
                        or consecutive operators).
        """
        try:
            tokens = self._tokenize(expression)
            postfix = self._infix_to_postfix(tokens)
            result = self._evaluate_postfix(postfix)
            return result
        except (ValueError, TypeError, ZeroDivisionError) as e:
            raise e  # Re-raise for consistent error handling

    def _tokenize(self, expression: str) -> list:
        """
        Tokenizes the input expression into a list of numbers, operators, and
        parentheses.

        Args:
            expression: The mathematical expression string.

        Returns:
            A list of tokens.

        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Remove whitespace
        expression = expression.replace(" ", "")
        
        # Use regular expression to split the expression into tokens
        pattern = r"(\d+\.?\d*|[\+\-\*/\(\)])" # Updated regex
        tokens = re.findall(pattern, expression)

        # Validate characters and consecutive operators
        valid_chars = r"^[\d\+\-\*/\(\)\.]+$"
        if not re.match(valid_chars, expression):
            raise ValueError("Invalid characters in expression.")

        for i in range(len(tokens) - 1):
            if tokens[i] in "+-*/" and tokens[i+1] in "+-*/":
              raise ValueError(f"Invalid expression: Consecutive operators '{tokens[i]}' and '{tokens[i+1]}'")
        
        return tokens
        

    def _infix_to_postfix(self, tokens: list) -> list:
        """
        Converts a list of tokens from infix notation to postfix notation
        (Reverse Polish Notation) using the Shunting Yard algorithm.

        Args:
            tokens: A list of tokens in infix notation.

        Returns:
            A list of tokens in postfix notation.

        Raises:
             ValueError: If parentheses are unbalanced.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operator_stack = []

        for token in tokens:
            if re.match(r"^-?\d+\.?\d*$", token):  # Match integers and floats
                output.append(float(token))  # Convert to float here
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
                     raise ValueError("Unbalanced parentheses (missing '(').")
                operator_stack.pop()  # Pop the '('
            
        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Unbalanced parentheses (missing ')').")
            output.append(operator_stack.pop())
        return output

    def _evaluate_postfix(self, tokens: list) -> float:
        """
        Evaluates a list of tokens in postfix notation.

        Args:
            tokens: A list of tokens in postfix notation.

        Returns:
            The result of the evaluation as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., division by zero).
        """
        
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid postfix expression.")
                try:
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
                            raise ZeroDivisionError("Division by zero.")
                        stack.append(operand1 / operand2)
                except ZeroDivisionError as e:
                      raise e
                except Exception as e:
                    raise ValueError(f"Error during evaluation: {e}")

        if len(stack) != 1:
             raise ValueError("Invalid postfix expression.")           
        return stack.pop()



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
        except (ValueError, TypeError, ZeroDivisionError) as e:
            print("Error:", e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

