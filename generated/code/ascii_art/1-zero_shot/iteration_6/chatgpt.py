class AsciiArt:
    """
    A class to generate 2D ASCII art for various shapes.
    
    This implementation meets the requirements of ISO/IEC 25010:
      - Functionality: Provides methods to draw a square, rectangle, parallelogram,
        right-angled triangle, and symmetrical pyramid using a chosen symbol.
      - Implementation: Uses object-oriented programming and built-in error types
        to validate inputs.
      - Code Quality: The code is modular, efficient, well-documented, and easily testable.
    """

    def __init__(self):
        # No instance-specific state is needed.
        pass

    @staticmethod
    def _validate_dimensions(*dimensions):
        """
        Validate that provided dimensions (width, height) are positive integers.
        
        :param dimensions: One or more integer dimensions.
        :raises ValueError: If any dimension is not a positive integer.
        """
        for d in dimensions:
            if not isinstance(d, int) or d <= 0:
                raise ValueError("Dimensions must be positive integers.")

    @staticmethod
    def _validate_symbol(symbol: str):
        """
        Validate that the symbol is a single non-whitespace character.
        
        :param symbol: The symbol from which the shape is drawn.
        :raises ValueError: If the symbol is not a single, visible character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a completely filled square.
        
        :param width: The side length of the square.
        :param symbol: The character used to build the square.
        :return: A multi-line string representing the square.
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)

        # Each row of the square is the symbol repeated 'width' times.
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled rectangle.
        
        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        :param symbol: The character used to build the rectangle.
        :return: A multi-line string representing the rectangle.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        # Build each row with the symbol repeated 'width' times.
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled parallelogram.
        
        The shape grows diagonally to the right: each subsequent row is shifted one space.
        
        :param width: The width of the parallelogram (number of symbols per row).
        :param height: The number of rows.
        :param symbol: The character used to draw the parallelogram.
        :return: A multi-line string representing the parallelogram.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Each row is shifted by 'i' spaces.
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally to the right.
        
        When height > 1, the first row has 1 symbol and the last row has 'width' symbols;
        intermediate rows are linearly interpolated.
        
        :param width: The target width (base) of the triangle (number of symbols in the final row).
        :param height: The number of rows in the triangle.
        :param symbol: The character used to draw the triangle.
        :return: A multi-line string representing the right-angled triangle.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        lines = []
        if height == 1:
            # For a single-row triangle, simply draw a line with 'width' symbols.
            lines.append(symbol * width)
        else:
            for i in range(height):
                # Interpolate the number of symbols: first row = 1 symbol, last row = width symbols.
                # Formula: count = round((width - 1) * (i / (height - 1))) + 1
                count = round((width - 1) * (i / (height - 1))) + 1
                lines.append(symbol * count)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.
        
        Each row is centered with the number of symbols increasing by 2 per level.
        
        :param height: The number of levels in the pyramid.
        :param symbol: The character used to draw the pyramid.
        :return: A multi-line string representing the pyramid.
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Calculate the number of symbols (odd numbers: 1, 3, 5, …).
            num_symbols = 2 * i + 1
            # Calculate the leading spaces to center the pyramid.
            spaces = height - i - 1
            line = " " * spaces + symbol * num_symbols
            lines.append(line)
        return "\n".join(lines)


if __name__ == "__main__":
    # Example usage and simple tests for each shape.
    art = AsciiArt()
    
    print("Square (width = 5):")
    print(art.draw_square(5, "#"))
    print("\nRectangle (width = 7, height = 3):")
    print(art.draw_rectangle(7, 3, "*"))
    print("\nParallelogram (width = 6, height = 4):")
    print(art.draw_parallelogram(6, 4, "@"))
    print("\nRight-angled Triangle (width = 5, height = 4):")
    print(art.draw_triangle(5, 4, "$"))
    print("\nPyramid (height = 4):")
    print(art.draw_pyramid(4, "%"))
