class AsciiArt:
    """
    A class for generating 2D ASCII art shapes in the console.
    This class supports drawing squares, rectangles, parallelograms,
    right-angled triangles (with the right angle at the top-left), and
    symmetrical pyramids.
    """

    def __init__(self):
        # No instance attributes are necessary at this time.
        pass

    def _validate_dimensions(self, *dims: int) -> None:
        """
        Validates that all provided dimensions are positive integers.

        Args:
            *dims (int): One or more dimension values to validate.

        Raises:
            ValueError: If any dimension is not an integer or is <= 0.
        """
        for dim in dims:
            if not isinstance(dim, int):
                raise ValueError("Dimensions must be integers.")
            if dim <= 0:
                raise ValueError("Dimensions must be positive integers.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the symbol is a single, non-whitespace character.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            ValueError: If symbol is not a string of exactly one non-whitespace character.
        """
        if not isinstance(symbol, str):
            raise ValueError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a completely filled square using the specified symbol.

        Args:
            width (int): The width (and height) of the square.
            symbol (str): The printable symbol to fill the square with.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If width is not a positive integer or the symbol is invalid.
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)
        # Build each row by repeating the symbol 'width' times,
        # and then join the rows with a newline.
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled rectangle using the specified symbol.

        Args:
            width (int): The number of symbols per row.
            height (int): The number of rows.
            symbol (str): The printable symbol to fill the rectangle with.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If width or height is not a positive integer or the symbol is invalid.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        # Create the rectangle row by row.
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled parallelogram. Each row is shifted
        one space to the right relative to the previous row.

        Args:
            width (int): The number of symbols in the base of the parallelogram.
            height (int): The number of rows.
            symbol (str): The printable symbol used to draw the parallelogram.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If width or height is not a positive integer or the symbol is invalid.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # Each subsequent row starts with one more space.
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled right-angled triangle using the specified symbol.
        In this implementation the right angle is positioned at the top-left corner.
        Each subsequent row is indented by one additional space and the number of
        symbols decreases by one per row.

        For example, draw_triangle(width=5, height=3, symbol='*') produces:
            *****
             ****
              ***

        Note:
            To ensure a proper filled triangle, width must be greater than or equal to height.

        Args:
            width (int): The length of the triangle's horizontal leg (top edge).
            height (int): The number of rows (vertical leg length).
            symbol (str): The printable symbol used to draw the triangle.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            ValueError: If dimensions are invalid, symbol is invalid,
                        or if width < height.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        if width < height:
            raise ValueError(
                "For a right-angled triangle with the right angle at the top-left, "
                "width must be greater than or equal to height."
            )

        lines = []
        # Each row i has an indent of i spaces and (width - i) symbols.
        for i in range(height):
            count = width - i
            line = " " * i + symbol * count
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a completely filled symmetric pyramid using the specified symbol.
        Each row contains an odd number of symbols (2 * row_index + 1), centered
        within a field of width (2 * height - 1).

        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): The printable symbol used to draw the pyramid.

        Returns:
            str: A multi-line string representing the symmetric pyramid.

        Raises:
            ValueError: If height is not a positive integer or the symbol is invalid.
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)
        lines = []
        total_width = 2 * height - 1  # The width of the pyramid's base.
        for i in range(height):
            num_symbols = 2 * i + 1
            num_spaces = (total_width - num_symbols) // 2
            line = " " * num_spaces + symbol * num_symbols + " " * num_spaces
            lines.append(line)
        return "\n".join(lines)


# Example usage in a console-based application
if __name__ == "__main__":
    art = AsciiArt()
    try:
        print("Square (width = 5):")
        print(art.draw_square(5, "#"))
        print("\nRectangle (width = 8, height = 3):")
        print(art.draw_rectangle(8, 3, "*"))
        print("\nParallelogram (width = 6, height = 4):")
        print(art.draw_parallelogram(6, 4, "@"))
        print("\nTriangle (width = 7, height = 4):")
        print(art.draw_triangle(7, 4, "$"))
        print("\nPyramid (height = 5):")
        print(art.draw_pyramid(5, "%"))
    except ValueError as error:
        print("Error:", error)
