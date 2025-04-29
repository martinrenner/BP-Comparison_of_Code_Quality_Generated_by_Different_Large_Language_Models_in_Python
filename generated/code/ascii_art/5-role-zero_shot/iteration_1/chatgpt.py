import math


class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods for drawing filled shapes:
      - Square
      - Rectangle
      - Parallelogram (with each row shifted one space to the right)
      - Right-angled triangle (with the right angle at the bottom-left)
      - Symmetrical pyramid

    Each method validates its inputs according to the following rules:
      • Numeric dimensions (width/height) must be positive integers.
      • Symbol must be a single, non-whitespace, printable character.
    """

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validate that a dimension is a positive integer.

        Args:
            value (int): The dimension to check.
            name (str): The name of the parameter (for the error message).

        Raises:
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the symbol is a single, printable, non-whitespace character.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            ValueError: If symbol is not exactly one character or is whitespace.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace() or not symbol.isprintable():
            raise ValueError("Symbol must be a non-whitespace, printable character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square with side length equal to 'width'.

        Args:
            width (int): The number of symbols in each side of the square.
            symbol (str): The single-character symbol used to fill the square.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If the width is not a positive integer or if the symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)

        # Generate each row of the square.
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle with specified width and height.

        Args:
            width (int): The number of symbols in each row.
            height (int): The number of rows.
            symbol (str): The single-character symbol used to fill the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If the dimensions are not positive integers or if the symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram that shifts each row one space to the right.

        Args:
            width (int): The number of symbols in the non-shifted row.
            height (int): The number of rows.
            symbol (str): The single-character symbol used to fill the parallelogram.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If the dimensions are not positive integers or if the symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Each row is shifted by i spaces.
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle with the right angle at the bottom-left corner.

        The triangle is constructed over 'height' rows. Its horizontal length scales
        so that the bottom row has exactly 'width' symbols. The number of symbols in 
        each row is computed using a simple scaling formula.

        Args:
            width (int): The number of symbols in the base (last row) of the triangle.
            height (int): The number of rows.
            symbol (str): The single-character symbol used to fill the triangle.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            ValueError: If the dimensions are not positive integers or if the symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Scale the number of symbols so that the last row has exactly 'width' symbols.
            count = max(1, math.ceil((i + 1) * width / height))
            lines.append(symbol * count)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid.

        The pyramid has 'height' rows and a base width of (2 * height - 1) symbols.
        Each row is centered horizontally.

        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): The single-character symbol used to fill the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If the height is not a positive integer or if the symbol is invalid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Determine leading spaces to center the pyramid.
            spaces = " " * (height - i - 1)
            # Each row has an odd number of symbols.
            symbols_count = 2 * i + 1
            line = spaces + symbol * symbols_count
            lines.append(line)
        return "\n".join(lines)


if __name__ == "__main__":
    # Create an instance of the AsciiArt class.
    art = AsciiArt()

    # Demonstration of the different shapes.
    try:
        print("Square (width=4, symbol='#'):")
        print(art.draw_square(4, "#"))
        print("\nRectangle (width=6, height=3, symbol='*'):")
        print(art.draw_rectangle(6, 3, "*"))
        print("\nParallelogram (width=6, height=4, symbol='@'):")
        print(art.draw_parallelogram(6, 4, "@"))
        print("\nTriangle (width=5, height=5, symbol='+'):")
        print(art.draw_triangle(5, 5, "+"))
        print("\nPyramid (height=5, symbol='^'):")
        print(art.draw_pyramid(5, "^"))
    except ValueError as e:
        # Output errors for invalid input.
        print(f"Input Error: {e}")
