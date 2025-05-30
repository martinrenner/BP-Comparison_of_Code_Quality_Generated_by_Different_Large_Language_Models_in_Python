#!/usr/bin/env python3
"""
Console-based 2D ASCII ART app implemented using OOP.
This module provides the AsciiArt class which implements methods for drawing various
filled ASCII shapes (square, rectangle, parallelogram, right-angled triangle, and pyramid)
with input validation to ensure correct parameters. Each method returns a multi-line string
representing the ASCII art.

ISO/IEC 25010 Requirements Addressed:
- Functionality: Provides multiple drawing methods as specified.
- Correctness & Performance: Uses efficient string operations and list comprehensions.
- Modularity: Code is organized in a class with helper (validation) methods.
- Security: Validates inputs against invalid/malicious values.
- Testability: Each function returns a string; sample usage is provided in the __main__ block.
- Readability & Documentation: Contains docstrings, comments, and clear variable names.
"""

import math

class AsciiArt:
    """
    A class for generating various ASCII art shapes.
    """

    @staticmethod
    def _validate_positive_int(value: int, name: str) -> None:
        """
        Validates that a given value is a positive integer.
        
        Args:
            value (int): The value to validate.
            name (str): The name of the variable (for error messages).
        
        Raises:
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer, got {value}.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that a symbol is a single, non-whitespace character.
        
        Args:
            symbol (str): The symbol to validate.
        
        Raises:
            ValueError: If symbol is not a single printable character or is whitespace.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single, non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of given width using the specified symbol.
        
        Args:
            width (int): The side length of the square.
            symbol (str): The character used to draw the square.
        
        Returns:
            str: A multi-line string representing the filled square.
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)

        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle with given width and height using the specified symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character used to draw the rectangle.
        
        Returns:
            str: A multi-line string representing the filled rectangle.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that shifts one space to the right on each subsequent row.
        
        Args:
            width (int): The width of each row of the parallelogram.
            height (int): The number of rows (height) of the parallelogram.
            symbol (str): The character used to draw the parallelogram.
        
        Returns:
            str: A multi-line string representing the filled parallelogram.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        # Each row is indented by an additional space to create a parallelogram effect.
        lines = [(" " * row) + (symbol * width) for row in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle that "grows" diagonally to the right.
        The triangle is constructed over a grid of 'height' rows and scaled so that the
        base contains exactly 'width' symbols.
        
        Each row is additionally indented by a number of spaces equal to the row index,
        enhancing the diagonal growth effect.
        
        Args:
            width (int): The number of symbols in the base (last row) of the triangle.
            height (int): The number of rows in the triangle.
            symbol (str): The character used to draw the triangle.
        
        Returns:
            str: A multi-line string representing the filled triangle.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        # Calculate the number of symbols for each row so that the last row has exactly 'width' symbols.
        for row in range(height):
            # Using math.ceil ensures at least one symbol is drawn on the first row.
            symbols_count = math.ceil((row + 1) * width / height)
            line = (" " * row) + (symbol * symbols_count)
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid using the specified symbol.
        The pyramid consists of 'height' rows and is centered horizontally.
        
        Args:
            height (int): The height (number of rows) of the pyramid.
            symbol (str): The character used to draw the pyramid.
        
        Returns:
            str: A multi-line string representing the filled pyramid.
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            # Calculate spaces to left-align the pyramid centrally.
            spaces_count = height - row - 1
            symbols_count = 2 * row + 1
            line = (" " * spaces_count) + (symbol * symbols_count)
            lines.append(line)
        return "\n".join(lines)

# Sample usage and testing
if __name__ == "__main__":
    art = AsciiArt()

    try:
        print("Square (width=5):")
        print(art.draw_square(5, "#"))
        print("\nRectangle (width=8, height=3):")
        print(art.draw_rectangle(8, 3, "*"))
        print("\nParallelogram (width=6, height=4):")
        print(art.draw_parallelogram(6, 4, "@"))
        print("\nRight-Angled Triangle (width=10, height=5):")
        print(art.draw_triangle(10, 5, "$"))
        print("\nPyramid (height=5):")
        print(art.draw_pyramid(5, "^"))
    except ValueError as e:
        print("Error:", e)
