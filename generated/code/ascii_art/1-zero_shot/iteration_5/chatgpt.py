import math

class AsciiArt:
    """
    A class for drawing 2D ASCII art shapes in the console.
    
    Methods provided:
      - draw_square(width: int, symbol: str) -> str
      - draw_rectangle(width: int, height: int, symbol: str) -> str
      - draw_parallelogram(width: int, height: int, symbol: str) -> str
      - draw_triangle(width: int, height: int, symbol: str) -> str
      - draw_pyramid(height: int, symbol: str) -> str
    """

    def __init__(self):
        # No instance attributes needed
        pass

    @staticmethod
    def _validate_positive_int(value: int, name: str) -> None:
        """
        Validates that the given value is a positive integer.

        Args:
            value: The value to check.
            name: The name of the parameter for error messages.

        Raises:
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer. Got {value}.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that symbol is a single non-whitespace character.

        Args:
            symbol: The symbol to check.

        Raises:
            ValueError: If symbol is not a single printable non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be exactly one non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width using the specified symbol.

        Args:
            width: The side length of the square.
            symbol: A single non-whitespace character used to fill the square.

        Returns:
            A multi-line string representing the square in ASCII art.
        """
        self._validate_positive_int(width, "width")
        self._validate_symbol(symbol)

        # Each row is a repetition of the symbol, and there are 'width' rows.
        row = symbol * width
        square = "\n".join(row for _ in range(width))
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height using the specified symbol.

        Args:
            width: The horizontal length of the rectangle.
            height: The vertical length (number of rows) of the rectangle.
            symbol: A single non-whitespace character used to fill the rectangle.

        Returns:
            A multi-line string representing the rectangle in ASCII art.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        row = symbol * width
        rectangle = "\n".join(row for _ in range(height))
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram that grows diagonally to the right using the specified symbol.
        Each subsequent row is shifted by one additional space.

        Args:
            width: The number of symbols in each row.
            height: The number of rows.
            symbol: A single non-whitespace character used to fill the parallelogram.

        Returns:
            A multi-line string representing the parallelogram in ASCII art.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Each row is preceded by i spaces to achieve the diagonal effect.
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally to the right.
        The triangle is drawn with 'height' rows and the bottom row will have exactly 'width' symbols.
        The number of symbols in each row increases linearly from 1 in the first row to width in the last row.

        Args:
            width: The number of symbols in the final (bottom) row.
            height: The total number of rows.
            symbol: A single non-whitespace character used to fill the triangle.

        Returns:
            A multi-line string representing the right-angled triangle in ASCII art.
        """
        self._validate_positive_int(width, "width")
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Calculate the number of symbols for the current row.
            # math.ceil ensures that the final row gets exactly 'width' symbols.
            num_symbols = math.ceil((i + 1) * width / height)
            # Ensure that at least one symbol is printed.
            num_symbols = max(1, num_symbols)
            line = symbol * num_symbols
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid using the specified symbol.
        The pyramid has 'height' rows and a base width of (2 * height - 1) symbols.

        Args:
            height: The number of rows in the pyramid.
            symbol: A single non-whitespace character used to build the pyramid.

        Returns:
            A multi-line string representing the pyramid in ASCII art.
        """
        self._validate_positive_int(height, "height")
        self._validate_symbol(symbol)

        lines = []
        base_width = 2 * height - 1
        for i in range(height):
            # For the i-th row, the number of symbols is 2*i + 1.
            num_symbols = 2 * i + 1
            # Calculate the required left-padding so the pyramid is centered.
            num_spaces = (base_width - num_symbols) // 2
            line = " " * num_spaces + symbol * num_symbols
            lines.append(line)
        return "\n".join(lines)


# Example usage:
if __name__ == "__main__":
    art = AsciiArt()

    print("Square (width=5):")
    print(art.draw_square(5, "#"))
    
    print("\nRectangle (width=10, height=3):")
    print(art.draw_rectangle(10, 3, "*"))
    
    print("\nParallelogram (width=10, height=4):")
    print(art.draw_parallelogram(10, 4, "@"))
    
    print("\nRight-angled Triangle (width=10, height=5):")
    print(art.draw_triangle(10, 5, "+"))
    
    print("\nPyramid (height=5):")
    print(art.draw_pyramid(5, "$"))
