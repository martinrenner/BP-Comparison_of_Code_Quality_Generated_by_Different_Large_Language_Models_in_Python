class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses, following the correct order
    of operations.  Handles integer and decimal inputs (including negatives).
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
        """
        tokens = self._tokenize(expression)
        result = self._parse_expression(tokens)
        return result

    def _tokenize(self, expression: str) -> list:
        """
        Converts the expression string into a list of tokens (numbers, operators, parentheses).
        """
        pass  # Implementation in Step 2

    def _parse_expression(self, tokens: list) -> float:
        """
        Parses the token list and evaluates the expression using the shunting yard algorithm.
        """
        pass # Implementation in Step 3

    def _parse_number(self, tokens:list, index: int) -> (float, int):
        """
        Parses numbers, supporting integer and decimal formats
        """
        pass # Implementation in Step 2

    def _apply_operator(self, operator: str, operand1: float, operand2: float) -> float:
        """
        Applies the specified operator to the two operands.
        """
        pass # Implementation in Step 3


    def _tokenize(self, expression: str) -> list:
        """
        Converts the expression string into a list of tokens.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isspace():
                i += 1
                continue
            elif char.isdigit() or (char == '-' and (i == 0 or expression[i-1] in '+-*/(')):
                number, next_index = self._parse_number(expression, i)
                tokens.append(number)
                i = next_index
                continue
            elif char in '+-*/()':
                tokens.append(char)
                i += 1
            else:
                raise ValueError(f"Invalid character: {char}")
        return tokens

    def _parse_number(self, expression: str, index: int) -> (float, int):
        """
        Parses a number (integer or decimal) from the expression string.
        """
        number_str = ""
        is_decimal = False
        if expression[index] == '-':
            number_str += '-'
            index += 1

        while index < len(expression):
            char = expression[index]
            if char.isdigit():
                number_str += char
            elif char == '.':
                if is_decimal:
                    raise ValueError("Invalid number format: Multiple decimal points")
                is_decimal = True
                number_str += char
            else:
                break
            index += 1
        
        if number_str == '-' or number_str == '' or number_str.endswith('.'):
            raise ValueError(f"Invalid number format: {number_str}")
        return float(number_str), index



    def _parse_expression(self, tokens: list) -> float:
        """
        Parses the token list and evaluates the expression.  Uses a simplified
        Shunting Yard algorithm.
        """
        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in '+-*/':
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
                    raise ValueError("Unbalanced parentheses")
                operator_stack.pop()  # Remove the '('
            else: # This should be unreachable due to prior validation
                raise ValueError(f"Unexpected token: {token}")

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Unbalanced parentheses")
            output_queue.append(operator_stack.pop())

        # Evaluate the RPN expression
        evaluation_stack = []
        for token in output_queue:
            if isinstance(token, float):
                evaluation_stack.append(token)
            else:  # It's an operator
                if len(evaluation_stack) < 2:
                    raise ValueError("Invalid expression: Not enough operands")
                operand2 = evaluation_stack.pop()
                operand1 = evaluation_stack.pop()
                result = self._apply_operator(token, operand1, operand2)
                evaluation_stack.append(result)

        if len(evaluation_stack) != 1:
             raise ValueError("Invalid expression: Too many operands")
        return evaluation_stack[0]
    
    def _apply_operator(self, operator: str, operand1: float, operand2: float) -> float:
        """Applies the specified operator to the two operands."""
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                raise ZeroDivisionError("Division by zero")
            return operand1 / operand2
        else: # This should never be reached given the prior checks
            raise ValueError(f"Invalid operator: {operator}")



class Calculator:
    """
    A console-based arithmetic calculator that supports addition, subtraction,
    multiplication, division, and parentheses, following the correct order
    of operations.  Handles integer and decimal inputs (including negatives).
    """

    def calculate(self, expression: str) -> float:
        """
        Evaluates the arithmetic expression and returns the result.

        Args:
            expression: The arithmetic expression as a string.

        Returns:
            The result of the expression as a float.

        Raises:
            ValueError: If the expression is invalid (e.g., unbalanced parentheses,
                        invalid characters, division by zero).
            ZeroDivisionError: If there's a division by zero.
        """
        tokens = self._tokenize(expression)
        result = self._parse_expression(tokens)
        return result

    def _tokenize(self, expression: str) -> list:
        """
        Converts the expression string into a list of tokens.
        """
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isspace():
                i += 1
                continue
            elif char.isdigit() or (char == '-' and (i == 0 or expression[i-1] in '+-*/(')):
                number, next_index = self._parse_number(expression, i)
                tokens.append(number)
                i = next_index
                continue
            elif char in '+-*/()':
                tokens.append(char)
                i += 1
            else:
                raise ValueError(f"Invalid character: {char}")
        return tokens

    def _parse_number(self, expression: str, index: int) -> (float, int):
        """
        Parses a number (integer or decimal) from the expression string.
        """
        number_str = ""
        is_decimal = False
        if expression[index] == '-':
            number_str += '-'
            index += 1

        while index < len(expression):
            char = expression[index]
            if char.isdigit():
                number_str += char
            elif char == '.':
                if is_decimal:
                    raise ValueError("Invalid number format: Multiple decimal points")
                is_decimal = True
                number_str += char
            else:
                break
            index += 1
        
        if number_str == '-' or number_str == '' or number_str.endswith('.'):
            raise ValueError(f"Invalid number format: {number_str}")
        return float(number_str), index

    def _parse_expression(self, tokens: list) -> float:
        """
        Parses the token list and evaluates the expression.  Uses a simplified
        Shunting Yard algorithm.
        """
        output_queue = []
        operator_stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in '+-*/':
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
                    raise ValueError("Unbalanced parentheses")
                operator_stack.pop()  # Remove the '('
            else: # This should be unreachable due to prior validation
                raise ValueError(f"Unexpected token: {token}")

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Unbalanced parentheses")
            output_queue.append(operator_stack.pop())

        # Evaluate the RPN expression
        evaluation_stack = []
        for token in output_queue:
            if isinstance(token, float):
                evaluation_stack.append(token)
            else:  # It's an operator
                if len(evaluation_stack) < 2:
                    raise ValueError("Invalid expression: Not enough operands")
                operand2 = evaluation_stack.pop()
                operand1 = evaluation_stack.pop()
                result = self._apply_operator(token, operand1, operand2)
                evaluation_stack.append(result)

        if len(evaluation_stack) != 1:
             raise ValueError("Invalid expression: Too many operands")
        return evaluation_stack[0]
    
    def _apply_operator(self, operator: str, operand1: float, operand2: float) -> float:
        """Applies the specified operator to the two operands."""
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                raise ZeroDivisionError("Division by zero")
            return operand1 / operand2
        else: #This should never be reached given our prior checks
            raise ValueError(f"Invalid operator: {operator}")



# --- Testing ---
if __name__ == "__main__":
    calculator = Calculator()

    test_cases = [
        ("1 + 2", 3.0),
        ("1 - 2", -1.0),
        ("2 * 3", 6.0),
        ("8 / 4", 2.0),
        ("1 + 2 * 3", 7.0),
        ("(1 + 2) * 3", 9.0),
        ("10 - 2 * (4 + 1)", 0.0),
        ("1.5 + 2.5", 4.0),
        ("-1 + 3", 2.0),
        ("-(1 + 2)", -3.0),
        ("2 * ( -3 + 5 )", 4.0),
        ("10 / (2 + 3) * 2", 4.0),
        ("10/(2+3)*2", 4.0),
    ]
    
    for expression, expected in test_cases:
        try:
            result = calculator.calculate(expression)
            print(f"Expression: {expression}, Result: {result}, Expected: {expected}, Pass: {result == expected}")
            assert result == expected, f"Failed for {expression}: Expected {expected}, got {result}"
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Expression: {expression}, Error: {e}, Expected: {expected}, Pass: False")

    # Test cases for errors
    error_test_cases = [
        ("1 + ", ValueError),
        ("1 ++ 2", ValueError),
        ("(1 + 2", ValueError),
        ("1 + 2)", ValueError),
        ("1 / 0", ZeroDivisionError),
        ("1.2.3 + 4", ValueError),
        ("a + 2", ValueError),
        ("2 -", ValueError),
        ("-(", ValueError),
        ("2 * ()", ValueError),
    ]
    
    for expression, expected_error in error_test_cases:
        try:
            calculator.calculate(expression)
            print(f"Expression: {expression}, Expected Error: {expected_error}, Pass: False")
        except expected_error as e:
            print(f"Expression: {expression}, Error: {e}, Expected Error: {expected_error}, Pass: True")  
        except Exception as e: # Catch other exceptions to prevent unexpected behavior
             print(f"Expression: {expression}, Unexpected Error: {e}, Expected Error: {expected_error}, Pass: False")   

    #Interactive testing
    while True:
        expression = input("Enter an arithmetic expression (or 'quit' to exit): ")
        if expression.lower() == 'quit':
            break
        try:
            result = calculator.calculate(expression)
            print(f"Result: {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
