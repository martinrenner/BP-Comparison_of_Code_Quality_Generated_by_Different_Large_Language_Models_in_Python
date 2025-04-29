import math

class AsciiArt:
    """
    A class to generate 2D ASCII art shapes.

    This class implements several methods to create ASCII shapes:
      - draw_square: Draws a filled square.
      - draw_rectangle: Draws a filled rectangle.
      - draw_parallelogram: Draws a filled parallelogram with each row shifted right.
      - draw_triangle: Draws a filled right-angled triangle that grows diagonally.
      - draw_pyramid: Draws a centered, symmetrical pyramid.

    Each method validates its inputs to ensure:
      • Dimensions (width/height) are positive integers.
      • The symbol is a single, non-whitespace character.

    This design adheres to modularity, readability, and security practices,
    and makes the module easily testable.
    """

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validates that a given dimension is a positive integer.

        Args:
            value (int): The dimension value.
            name (str): The name of the dimension (for error messages).

        Raises:
            ValueError: If the dimension is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the provided symbol is a single, non-whitespace character.

        Args:
            symbol (str): The symbol to be used for drawing.

        Raises:
            ValueError: If symbol is not a single printable character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of side length 'width' filled with 'symbol'.

        Args:
            width (int): The side length of the square.
            symbol (str): The character used to fill the square.

        Returns:
            str: A multi-line string representing the square.
        """
        self._validate_dimension(width, "Width")
        self._validate_symbol(symbol)

        # Each row consists of 'width' symbols, and there are 'width' rows.
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with 'symbol'.

        Args:
            width (int): The horizontal dimension.
            height (int): The vertical dimension.
            symbol (str): The character used to fill the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        # Build the rectangle line by line.
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram that grows diagonally to the right.

        Each row is shifted right by its row index starting from the top-left corner.

        Args:
            width (int): The number of symbols in each row.
            height (int): The number of rows.
            symbol (str): The character used to fill the parallelogram.

        Returns:
            str: A multi-line string representing the parallelogram.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Shift each row by 'i' spaces.
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally to the right.

        The triangle is drawn with 'height' rows. The number of symbols in each row
        scales linearly from 1 to 'width' so that the bottom row contains exactly 'width' symbols.

        Args:
            width (int): The number of symbols in the base (last row) of the triangle.
            height (int): The number of rows.
            symbol (str): The character used to fill the triangle.

        Returns:
            str: A multi-line string representing the triangle.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Compute the number of symbols for the current row. Use math.ceil to ensure
            # that the final row has exactly 'width' symbols.
            num_symbols = math.ceil((i + 1) * width / height)
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of given height.

        Each row i (0-indexed) contains (2*i + 1) 'symbol' characters,
        centered relative to the pyramid's base which has width (2*height - 1).

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character used to fill the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.
        """
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        lines = []
        base_width = 2 * height - 1  # The width of the pyramid's base.
        for i in range(height):
            num_symbols = 2 * i + 1
            # Calculate left padding to center the row.
            padding = (base_width - num_symbols) // 2
            line = " " * padding + symbol * num_symbols
            lines.append(line)
        return "\n".join(lines)

# Example usage: (This block can be used for testing the functions)
if __name__ == "__main__":
    art = AsciiArt()

    print("Square (width = 5, symbol = '#'):")
    print(art.draw_square(5, "#"))
    print("\nRectangle (width = 8, height = 3, symbol = '*'):")
    print(art.draw_rectangle(8, 3, "*"))
    print("\nParallelogram (width = 8, height = 4, symbol = '@'):")
    print(art.draw_parallelogram(8, 4, "@"))
    print("\nTriangle (width = 10, height = 5, symbol = '+'):")
    print(art.draw_triangle(10, 5, "+"))
    print("\nPyramid (height = 5, symbol = '$'):")
    print(art.draw_pyramid(5, "$"))
