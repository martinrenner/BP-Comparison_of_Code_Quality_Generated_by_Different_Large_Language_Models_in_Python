class AsciiArt:
    """
    A class for generating 2D ASCII art shapes in the console.

    Supported shapes:
      - Square
      - Rectangle
      - Parallelogram (each row shifted one space to the right)
      - Right-angled triangle (with the right angle at the bottom-left,
        growing diagonally to the right)
      - Symmetrical pyramid

    Each drawing method validates its inputs and returns a multi‐line string
    representing the ASCII art.
    """

    def __init__(self):
        # No instance state is needed yet.
        pass

    def _validate_dimension(self, value: int, name: str) -> None:
        """
        Validates that a dimension (width or height) is a positive integer.

        :param value: The dimension value to validate.
        :param name: The name of the dimension (used for error messages).
        :raises ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer, got {value}.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the symbol is a single, non-whitespace character.

        :param symbol: The symbol to validate.
        :raises ValueError: If symbol is not a single, non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single, non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a fully-filled square.

        :param width: The length of each side of the square.
        :param symbol: A single non-whitespace character to fill the shape.
        :return: A multi-line string representing the square.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)

        # Build each row and join with newline characters.
        row = symbol * width
        square_lines = [row for _ in range(width)]
        return "\n".join(square_lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a fully-filled rectangle.

        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        :param symbol: A single non-whitespace character to fill the shape.
        :return: A multi-line string representing the rectangle.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        # Build each row of the rectangle.
        row = symbol * width
        rectangle_lines = [row for _ in range(height)]
        return "\n".join(rectangle_lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a fully-filled parallelogram that grows diagonally to the right.

        Each subsequent row is shifted one space further to the right.

        :param width: The width (number of symbols in a row) of the parallelogram.
        :param height: The number of rows.
        :param symbol: A single non-whitespace character to fill the shape.
        :return: A multi-line string representing the parallelogram.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for r in range(height):
            # Each row is preceded by a number of spaces equal to the row index.
            line = " " * r + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally to the right.

        The triangle is defined such that:
          - Its base (last row) contains exactly "width" symbols.
          - There are "height" rows.
          - The number of symbols per row is linearly interpolated from 1 to width.
          - The right angle is located at the bottom-left.

        :param width: The number of symbols in the base of the triangle.
        :param height: The number of rows in the triangle.
        :param symbol: A single non-whitespace character to fill the shape.
        :return: A multi-line string representing the triangle.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        # Special-case when the triangle has only one row.
        if height == 1:
            return symbol * width

        lines = []
        # For a triangle with the right angle at the bottom-left,
        # the first row has 1 symbol and the last row has "width" symbols.
        # Use linear interpolation to compute symbols per row.
        for r in range(height):
            # Compute:
            #   num_symbols = 1 + round(r * (width - 1) / (height - 1))
            num_symbols = 1 + round(r * (width - 1) / (height - 1))
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        The pyramid has:
          - "height" rows.
          - A base width of (2 * height - 1) symbols.
          - Each row is centered with spaces padding the sides.

        :param height: The height of the pyramid (number of rows).
        :param symbol: A single non-whitespace character to fill the pyramid.
        :return: A multi-line string representing the pyramid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        base_width = 2 * height - 1
        lines = []
        for i in range(height):
            num_symbols = 2 * i + 1
            # Calculate left (and right) padding for centering the row.
            num_spaces = (base_width - num_symbols) // 2
            line = " " * num_spaces + symbol * num_symbols + " " * num_spaces
            lines.append(line)
        return "\n".join(lines)


# Example usage and basic test cases
if __name__ == "__main__":
    art = AsciiArt()

    # Draw a square
    print("Square (width=4):")
    print(art.draw_square(4, "#"))
    print()

    # Draw a rectangle
    print("Rectangle (width=6, height=3):")
    print(art.draw_rectangle(6, 3, "*"))
    print()

    # Draw a parallelogram
    print("Parallelogram (width=5, height=4):")
    print(art.draw_parallelogram(5, 4, "@"))
    print()

    # Draw a right-angled triangle
    print("Right-angled Triangle (base width=7, height=4):")
    print(art.draw_triangle(7, 4, "$"))
    print()

    # Draw a pyramid
    print("Pyramid (height=5):")
    print(art.draw_pyramid(5, "%"))
    print()
