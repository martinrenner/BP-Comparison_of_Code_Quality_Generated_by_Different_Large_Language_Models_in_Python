class AsciiArt:
    """
    A class for generating console-based 2D ASCII art shapes.
    
    This class implements functions to draw a square, rectangle, parallelogram,
    right-angled triangle, and symmetrical pyramid using a single printable symbol.
    All shapes are completely filled with the chosen symbol.
    """

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validates that the given dimension is a positive integer.

        Args:
            value (int): The value of the dimension to validate.
            name (str): The name of the dimension for the error message.

        Raises:
            ValueError: If the value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer, got {value}.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the given symbol is a single non-whitespace character.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            ValueError: If the symbol is not a single non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square (width x width) fully filled with the specified symbol.

        Args:
            width (int): The side length of the square.
            symbol (str): The symbol used to construct the square.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If width is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_symbol(symbol)

        # Generate each row of the square and join with newline characters.
        rows = [symbol * width for _ in range(width)]
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle fully filled with the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol used to construct the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If width or height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        rows = [symbol * width for _ in range(height)]
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram that grows diagonally to the right.
        Each subsequent row is shifted by one space.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol used to construct the parallelogram.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If width or height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Shift each row to the right by i spaces.
            line = " " * i + (symbol * width)
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally to the right,
        starting from the top-left corner. The triangle starts with 1 symbol in
        the first row and grows linearly so that the last row has 'width' symbols.

        Args:
            width (int): The number of symbols in the base (last row) of the triangle.
            height (int): The number of rows in the triangle.
            symbol (str): The symbol used to construct the triangle.

        Returns:
            str: A multi-line string representing the right-angled triangle.

        Raises:
            ValueError: If width or height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        lines = []
        if height == 1:
            # Special case: only one row.
            return symbol * width

        # Use linear interpolation to determine number of symbols for each row.
        # Ensures that the first row starts with one symbol and the last row has 'width' symbols.
        for i in range(height):
            # Formula: count = floor(i * (width - 1) / (height - 1)) + 1
            count = (i * (width - 1)) // (height - 1) + 1
            lines.append(symbol * count)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid. The pyramid consists of 'height' rows,
        and the base width equals (2 * height - 1).

        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): The symbol used to construct the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # The number of symbols increases by 2 on each subsequent row.
            num_symbols = 2 * i + 1
            # Calculate the left-side padding for centering.
            padding = height - i - 1
            lines.append(" " * padding + symbol * num_symbols)
        return "\n".join(lines)


if __name__ == "__main__":
    # Example usage and simple tests of the AsciiArt class.
    art = AsciiArt()

    print("Square (width=5):")
    print(art.draw_square(5, "#"))
    print("\nRectangle (width=10, height=3):")
    print(art.draw_rectangle(10, 3, "*"))
    print("\nParallelogram (width=6, height=4):")
    print(art.draw_parallelogram(6, 4, "@"))
    print("\nRight-Angled Triangle (base width=10, height=5):")
    print(art.draw_triangle(10, 5, "$"))
    print("\nPyramid (height=5):")
    print(art.draw_pyramid(5, "%"))
