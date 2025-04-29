"""
Console-based 2D ASCII Art Application

This module defines the AsciiArt class which provides methods to draw
various filled ASCII shapes: square, rectangle, parallelogram, right-angled triangle,
and pyramid.

All drawing functions return a multi-line string representing the ASCII art.
Input parameters (dimensions and symbol) are validated to ensure they are positive integers
and the symbol is a single, non-whitespace character.

Author: Senior Software Developer
"""

import math

class AsciiArt:
    """
    Class to generate various ASCII art shapes.
    """

    def __init__(self):
        # No instance-specific initialization is needed.
        pass

    @staticmethod
    def _validate_dimensions(*dimensions):
        """
        Validates that each dimension provided is an integer greater than zero.

        Args:
            *dimensions: One or more dimension values.

        Raises:
            ValueError: If any dimension is not a positive integer.
        """
        for dim in dimensions:
            if not isinstance(dim, int) or dim <= 0:
                raise ValueError("Dimensions must be positive integers.")

    @staticmethod
    def _validate_symbol(symbol: str):
        """
        Validates that the symbol is a single, non-whitespace character.

        Args:
            symbol (str): The symbol to use for drawing.

        Raises:
            ValueError: If symbol is not a single printable character or is whitespace.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single, non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of size (width x width) using the specified symbol.

        Args:
            width (int): The number of symbols per side.
            symbol (str): The drawing symbol (a single character).

        Returns:
            str: A multi-line string representing the square.
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)

        # Create each row as a string with 'width' copies of symbol.
        rows = [symbol * width for _ in range(width)]
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle using the specified dimensions and symbol.

        Args:
            width (int): The number of symbols per row.
            height (int): The number of rows.
            symbol (str): The drawing symbol (a single character).

        Returns:
            str: A multi-line string representing the rectangle.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        rows = [symbol * width for _ in range(height)]
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that shifts one space to the right each row,
        starting from the top-left corner.

        Args:
            width (int): The number of symbols per row (without indentation).
            height (int): The number of rows.
            symbol (str): The drawing symbol (a single character).

        Returns:
            str: A multi-line string representing the parallelogram.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        # Each row is indented according to its row number.
        rows = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle that grows in width from top to bottom.
        The triangle is defined by the given 'width' for the bottom row and 'height'
        number of rows. The number of symbols in each row grows linearly from 1 in the first row
        to 'width' in the last row.

        For height == 1, the single row will use the 'width' number of symbols.

        Args:
            width (int): The number of symbols in the bottom row.
            height (int): The number of rows.
            symbol (str): The drawing symbol (a single character).

        Returns:
            str: A multi-line string representing the right-angled triangle.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        rows = []
        if height == 1:
            rows.append(symbol * width)
        else:
            # Use a linear interpolation so that the top row has 1 symbol and the bottom row exactly 'width' symbols.
            for i in range(height):
                # Ensure the first row has 1 symbol and the last row has exactly 'width' symbols.
                num_symbols = 1 + int(i * (width - 1) / (height - 1))
                rows.append(symbol * num_symbols)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical, filled pyramid with the specified height.
        The pyramid has 'height' rows and the width of the bottom row is (2 * height - 1).
        Each row is centered to form the pyramid shape.

        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): The drawing symbol (a single character).

        Returns:
            str: A multi-line string representing the pyramid.
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)

        total_width = 2 * height - 1  # The width of the pyramid's base.
        rows = []
        for i in range(height):
            # Each row i has an odd number of symbols: 2*i + 1.
            row_symbols = symbol * (2 * i + 1)
            rows.append(row_symbols.center(total_width))
        return "\n".join(rows)


# Optional demo code to illustrate usage of the AsciiArt class.
if __name__ == "__main__":
    art = AsciiArt()

    try:
        print("Square (width=5):")
        print(art.draw_square(5, "#"))
        print("\nRectangle (width=10, height=4):")
        print(art.draw_rectangle(10, 4, "*"))
        print("\nParallelogram (width=7, height=4):")
        print(art.draw_parallelogram(7, 4, "@"))
        print("\nRight-angled Triangle (width=8, height=4):")
        print(art.draw_triangle(8, 4, "$"))
        print("\nPyramid (height=5):")
        print(art.draw_pyramid(5, "+"))
    except ValueError as e:
        print("Error:", e)
