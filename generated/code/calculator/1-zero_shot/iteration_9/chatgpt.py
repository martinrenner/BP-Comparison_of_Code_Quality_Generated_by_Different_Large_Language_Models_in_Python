#!/usr/bin/env python3
"""
Console-based arithmetic calculator that meets ISO/IEC 25010 requirements.

Supported Operations:
    - Addition (+)
    - Subtraction (-)
    - Multiplication (*)
    - Division (/)
    - Parentheses for grouping ( )

Features:
    - Correct operator precedence and associativity.
    - Support for both integers and floating-point numbers, including negative values.
    - Input validation for unbalanced parentheses and invalid characters.
    - Uses exceptions (e.g. ValueError, ZeroDivisionError) to signal errors.
    - Implemented using object-oriented design.

Usage:
    calc = Calculator()
    result = calc.calculate("3 + 4 * (2 - 1) / 2")
    print(result)
    
A simple console loop is provided when this module is run as the main program.
"""

class Calculator:
    """
    A calculator supporting basic arithmetic operations with proper operator precedence.
    """
    
    def calculate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression and return the result as a float.
        
        Args:
            expression (str): The arithmetic expression to evaluate.
        
        Returns:
            float: The result of evaluating the expression.
        
        Raises:
            ValueError: If the expression contains invalid characters, unbalanced parentheses,
                        or a syntax error in the expression.
            ZeroDivisionError: If there is an attempt to divide by zero.
        """
        # Validate the expression for allowed characters and balanced parentheses.
        self._validate(expression)
        
        # Remove whitespace for simpler parsing.
        self.expression = expression.replace(" ", "")
        self.pos = 0  # Current position in the expression string.
        
        # Begin recursive descent parsing.
        result = self._parse_expression()
        
        # If we haven't consumed the entire expression, there's an error.
        if self.pos != len(self.expression):
            raise ValueError(f"Unexpected character at position {self.pos}: '{self.expression[self.pos]}'")
        return result
    
    def _validate(self, expression: str) -> None:
        """
        Validate the expression to ensure it contains only allowed characters and balanced parentheses.
        
        Args:
            expression (str): The expression string to validate.
        
        Raises:
            ValueError: If there is an invalid character or the parentheses are unbalanced.
        """
        allowed_chars = set("0123456789.+-*/() \t")
        parentheses_count = 0
        
        for idx, char in enumerate(expression):
            if char not in allowed_chars:
                raise ValueError(f"Invalid character '{char}' found at position {idx}.")
            if char == '(':
                parentheses_count += 1
            elif char == ')':
                parentheses_count -= 1
                if parentheses_count < 0:
                    raise ValueError("Unbalanced parentheses: missing an opening parenthesis.")
        if parentheses_count != 0:
            raise ValueError("Unbalanced parentheses: missing a closing parenthesis.")
    
    def _current_char(self):
        """Return the current character in the expression, or None if at the end."""
        if self.pos < len(self.expression):
            return self.expression[self.pos]
        return None
    
    def _consume_char(self):
        """Consume and return the current character, advancing the cursor."""
        current = self._current_char()
        self.pos += 1
        return current
    
    def _parse_expression(self) -> float:
        """
        Parse and evaluate an expression.
        Grammar: expression = term { ("+"|"-") term }
        """
        result = self._parse_term()
        while True:
            char = self._current_char()
            if char == '+' or char == '-':
                operator = self._consume_char()
                next_term = self._parse_term()
                if operator == '+':
                    result += next_term
                else:
                    result -= next_term
            else:
                break
        return result
    
    def _parse_term(self) -> float:
        """
        Parse and evaluate a term.
        Grammar: term = factor { ("*"|"/") factor }
        """
        result = self._parse_factor()
        while True:
            char = self._current_char()
            if char == '*' or char == '/':
                operator = self._consume_char()
                next_factor = self._parse_factor()
                if operator == '*':
                    result *= next_factor
                else:
                    # Check for division by zero.
                    if next_factor == 0:
                        raise ZeroDivisionError("Division by zero encountered.")
                    result /= next_factor
            else:
                break
        return result
    
    def _parse_factor(self) -> float:
        """
        Parse and evaluate a factor.
        Grammar: factor = ["+"|"-"] ( number | "(" expression ")" )
        Handles optional unary operators.
        """
        char = self._current_char()
        # Handle unary plus and minus.
        if char == '+' or char == '-':
            operator = self._consume_char()
            factor = self._parse_factor()
            return factor if operator == '+' else -factor
        
        # Parentheses: "(" expression ")"
        if char == '(':
            self._consume_char()  # consume '('
            result = self._parse_expression()
            if self._current_char() != ')':
                raise ValueError("Missing closing parenthesis.")
            self._consume_char()  # consume ')'
            return result
        
        # Parse a number (integer or floating-point).
        return self._parse_number()
    
    def _parse_number(self) -> float:
        """
        Parse a sequence of digits (and a decimal point) into a float.
        
        Returns:
            float: The parsed number.
            
        Raises:
            ValueError: If no valid number is present at the current parsing position.
        """
        start_pos = self.pos

        # There may be a leading minus sign which should have already been handled as unary.
        dot_encountered = False
        while self._current_char() is not None and (self._current_char().isdigit() or self._current_char() == '.'):
            if self._current_char() == '.':
                if dot_encountered:
                    # Two dots in the same number.
                    raise ValueError(f"Invalid number format at position {self.pos}: multiple decimal points.")
                dot_encountered = True
            self._consume_char()
            
        number_str = self.expression[start_pos:self.pos]
        if not number_str:
            raise ValueError(f"Number expected but not found at position {self.pos}.")
        
        try:
            return float(number_str)
        except ValueError:
            raise ValueError(f"Invalid number format: '{number_str}'")
        
if __name__ == "__main__":
    import sys
    
    def main():
        """
        Main function to run the console-based arithmetic calculator.
        """
        calc = Calculator()
        print("Arithmetic Calculator. Type 'exit' to quit.")
        while True:
            try:
                user_input = input("Enter expression> ")
            except (EOFError, KeyboardInterrupt):
                print("\nExiting calculator.")
                break
            if user_input.strip().lower() == "exit":
                break
            if user_input.strip() == "":
                continue
            try:
                result = calc.calculate(user_input)
                print("Result:", result)
            except Exception as e:
                print("Error:", e, file=sys.stderr)
    
    main()
