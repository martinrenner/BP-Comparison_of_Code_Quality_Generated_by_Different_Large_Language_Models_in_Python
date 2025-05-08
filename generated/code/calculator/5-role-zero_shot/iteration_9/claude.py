from typing import List, Dict, Union, Optional
import re
from abc import ABC, abstractmethod


class Token:
    """Base class for tokens in the arithmetic expression."""
    pass


class NumberToken(Token):
    """Token representing a numeric value."""
    
    def __init__(self, value: Union[int, float]):
        """
        Initialize a number token.
        
        Args:
            value: The numeric value of the token.
        """
        self.value = value
    
    def __str__(self) -> str:
        return str(self.value)


class OperatorToken(Token):
    """Token representing an arithmetic operator."""
    
    def __init__(self, operator: str):
        """
        Initialize an operator token.
        
        Args:
            operator: The operator symbol (+, -, *, /).
        """
        self.operator = operator
    
    def __str__(self) -> str:
        return self.operator


class ParenthesisToken(Token):
    """Token representing a parenthesis."""
    
    def __init__(self, parenthesis: str):
        """
        Initialize a parenthesis token.
        
        Args:
            parenthesis: The parenthesis symbol (either '(' or ')').
        """
        self.parenthesis = parenthesis
    
    def __str__(self) -> str:
        return self.parenthesis


class Operation(ABC):
    """Abstract base class for arithmetic operations."""
    
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """
        Execute the operation on two operands.
        
        Args:
            a: The first operand.
            b: The second operand.
            
        Returns:
            The result of the operation.
        """
        pass


class Addition(Operation):
    """Addition operation."""
    
    def execute(self, a: float, b: float) -> float:
        """
        Execute the addition operation.
        
        Args:
            a: The first operand.
            b: The second operand.
            
        Returns:
            The sum of a and b.
        """
        return a + b


class Subtraction(Operation):
    """Subtraction operation."""
    
    def execute(self, a: float, b: float) -> float:
        """
        Execute the subtraction operation.
        
        Args:
            a: The first operand.
            b: The second operand.
            
        Returns:
            The result of a - b.
        """
        return a - b


class Multiplication(Operation):
    """Multiplication operation."""
    
    def execute(self, a: float, b: float) -> float:
        """
        Execute the multiplication operation.
        
        Args:
            a: The first operand.
            b: The second operand.
            
        Returns:
            The product of a and b.
        """
        return a * b


class Division(Operation):
    """Division operation."""
    
    def execute(self, a: float, b: float) -> float:
        """
        Execute the division operation.
        
        Args:
            a: The first operand.
            b: The second operand.
            
        Returns:
            The result of a / b.
            
        Raises:
            ZeroDivisionError: If b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        return a / b


class ExpressionTokenizer:
    """Class responsible for tokenizing arithmetic expressions."""
    
    def __init__(self):
        """Initialize the tokenizer with a regular expression pattern for tokens."""
        # Pattern to match numbers, operators, and parentheses
        self.pattern = r'(\d+\.\d+|\d+|[+\-*/()])'
        
    def tokenize(self, expression: str) -> List[Token]:
        """
        Tokenize an arithmetic expression.
        
        Args:
            expression: The arithmetic expression to tokenize.
            
        Returns:
            A list of tokens.
            
        Raises:
            ValueError: If the expression contains invalid characters.
        """
        # Remove all whitespace from the expression
        expression = expression.replace(" ", "")
        
        # Check for invalid characters
        clean_expression = re.sub(self.pattern, '', expression)
        if clean_expression:
            invalid_chars = ', '.join(f"'{c}'" for c in set(clean_expression))
            raise ValueError(f"Expression contains invalid characters: {invalid_chars}")
        
        # Extract tokens
        token_strings = re.findall(self.pattern, expression)
        tokens = []
        
        for token_str in token_strings:
            if token_str in ['+', '-', '*', '/']:
                tokens.append(OperatorToken(token_str))
            elif token_str in ['(', ')']:
                tokens.append(ParenthesisToken(token_str))
            else:
                # It's a number
                try:
                    # Handle decimal numbers
                    if '.' in token_str:
                        tokens.append(NumberToken(float(token_str)))
                    else:
                        tokens.append(NumberToken(int(token_str)))
                except ValueError:
                    raise ValueError(f"Failed to parse number: {token_str}")
        
        # Handle unary minus by transforming -N to 0-N
        processed_tokens = []
        i = 0
        
        while i < len(tokens):
            current_token = tokens[i]
            
            # Check for unary minus
            if (isinstance(current_token, OperatorToken) and 
                current_token.operator == '-' and 
                (i == 0 or 
                 (isinstance(tokens[i-1], OperatorToken) or 
                  (isinstance(tokens[i-1], ParenthesisToken) and tokens[i-1].parenthesis == '(')))):
                
                # Insert 0 before unary minus
                processed_tokens.append(NumberToken(0))
                processed_tokens.append(current_token)
            else:
                processed_tokens.append(current_token)
            
            i += 1
            
        return processed_tokens


class ExpressionValidator:
    """Class responsible for validating arithmetic expressions."""
    
    def validate_parentheses(self, tokens: List[Token]) -> None:
        """
        Validate balanced parentheses in the expression.
        
        Args:
            tokens: The list of tokens to validate.
            
        Raises:
            ValueError: If parentheses are unbalanced.
        """
        stack = []
        
        for token in tokens:
            if isinstance(token, ParenthesisToken):
                if token.parenthesis == '(':
                    stack.append(token)
                elif token.parenthesis == ')':
                    if not stack:
                        raise ValueError("Unbalanced parentheses: too many closing parentheses")
                    stack.pop()
        
        if stack:
            raise ValueError("Unbalanced parentheses: missing closing parentheses")
    
    def validate_syntax(self, tokens: List[Token]) -> None:
        """
        Validate the syntax of the expression.
        
        Args:
            tokens: The list of tokens to validate.
            
        Raises:
            ValueError: If the syntax is invalid.
        """
        if not tokens:
            raise ValueError("Empty expression")
            
        for i, token in enumerate(tokens):
            # Check for consecutive operators
            if (isinstance(token, OperatorToken) and i < len(tokens) - 1 and 
                isinstance(tokens[i+1], OperatorToken)):
                raise ValueError(f"Invalid syntax: consecutive operators '{token.operator}{tokens[i+1].operator}'")
            
            # Check for operators at the end
            if isinstance(token, OperatorToken) and i == len(tokens) - 1:
                raise ValueError(f"Invalid syntax: expression ends with an operator '{token.operator}'")
            
            # Check for missing operands
            if (isinstance(token, ParenthesisToken) and token.parenthesis == '(' and 
                i < len(tokens) - 1 and isinstance(tokens[i+1], ParenthesisToken) and 
                tokens[i+1].parenthesis == ')'):
                raise ValueError("Invalid syntax: empty parentheses '()'")


class ExpressionEvaluator:
    """Class responsible for evaluating arithmetic expressions using the Shunting Yard algorithm."""
    
    def __init__(self):
        """Initialize the evaluator with operations and operator precedence."""
        self.operations: Dict[str, Operation] = {
            '+': Addition(),
            '-': Subtraction(),
            '*': Multiplication(),
            '/': Division()
        }
        
        self.precedence: Dict[str, int] = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }
    
    def _to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Convert infix expression to postfix using the Shunting Yard algorithm.
        
        Args:
            tokens: The list of tokens in infix notation.
            
        Returns:
            The list of tokens in postfix notation.
        """
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            if isinstance(token, NumberToken):
                output_queue.append(token)
                
            elif isinstance(token, OperatorToken):
                while (operator_stack and isinstance(operator_stack[-1], OperatorToken) and 
                       self.precedence[operator_stack[-1].operator] >= self.precedence[token.operator]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
                
            elif isinstance(token, ParenthesisToken):
                if token.parenthesis == '(':
                    operator_stack.append(token)
                else:  # token.parenthesis == ')'
                    while operator_stack and not (isinstance(operator_stack[-1], ParenthesisToken) and 
                                                 operator_stack[-1].parenthesis == '('):
                        output_queue.append(operator_stack.pop())
                    
                    # Pop the left parenthesis
                    if operator_stack and isinstance(operator_stack[-1], ParenthesisToken):
                        operator_stack.pop()
        
        # Pop any remaining operators from the stack to the output queue
        while operator_stack:
            output_queue.append(operator_stack.pop())
            
        return output_queue
    
    def evaluate(self, tokens: List[Token]) -> float:
        """
        Evaluate a tokenized arithmetic expression.
        
        Args:
            tokens: The list of tokens to evaluate.
            
        Returns:
            The result of the evaluation.
            
        Raises:
            ValueError: If the expression is invalid.
            ZeroDivisionError: If division by zero is attempted.
        """
        postfix_tokens = self._to_postfix(tokens)
        stack = []
        
        for token in postfix_tokens:
            if isinstance(token, NumberToken):
                stack.append(token.value)
            elif isinstance(token, OperatorToken):
                if len(stack) < 2:
                    raise ValueError("Invalid expression: not enough operands")
                
                b = stack.pop()
                a = stack.pop()
                
                operation = self.operations[token.operator]
                result = operation.execute(a, b)
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands")
            
        return stack[0]


class Calculator:
    """A calculator that evaluates arithmetic expressions."""
    
    def __init__(self):
        """Initialize the calculator with its components."""
        self.tokenizer = ExpressionTokenizer()
        self.validator = ExpressionValidator()
        self.evaluator = ExpressionEvaluator()
    
    def calculate(self, expression: str) -> float:
        """
        Calculate the result of an arithmetic expression.
        
        Args:
            expression: The arithmetic expression to evaluate.
            
        Returns:
            The result of the evaluation.
            
        Raises:
            ValueError: If the expression is invalid.
            ZeroDivisionError: If division by zero is attempted.
        """
        # Tokenize the expression
        tokens = self.tokenizer.tokenize(expression)
        
        # Validate the expression
        self.validator.validate_parentheses(tokens)
        self.validator.validate_syntax(tokens)
        
        # Evaluate the expression
        return self.evaluator.evaluate(tokens)


def main():
    """Main function to run the calculator."""
    calculator = Calculator()
    
    print("Arithmetic Calculator")
    print("Type 'exit' to quit")
    print("Examples of valid expressions: '2+2', '(3.5+4)*2', '10/5'")
    
    while True:
        try:
            expression = input("\nEnter an expression: ")
            if expression.lower() == 'exit':
                break
                
            result = calculator.calculate(expression)
            print(f"Result: {result}")
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    print("Calculator closed.")


if __name__ == "__main__":
    main()
