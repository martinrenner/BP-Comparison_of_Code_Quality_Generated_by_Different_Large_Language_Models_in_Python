class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    This class provides methods to draw various shapes filled with a specified symbol,
    adhering to the principles of object-oriented programming and ISO/IEC 25010
    quality characteristics.
    """

    def _validate_input(self, width=None, height=None, symbol=None):
        """Validates the input parameters for shape drawing methods.

        Args:
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.
            symbol (str, optional): The character used to draw the shape.

        Raises:
            TypeError: If width or height are not integers, or if symbol is not a string.
            ValueError: If width or height are negative, or if symbol is not
             a single, non-whitespace character.
        """

        if width is not None and not isinstance(width, int):
            raise TypeError("Width must be an integer.")
        if height is not None and not isinstance(height, int):
            raise TypeError("Height must be an integer.")
        if symbol is not None and not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")

        if width is not None and width <= 0:
            raise ValueError("Width must be a positive integer.")
        if height is not None and height <= 0:
            raise ValueError("Height must be a positive integer.")

        if symbol is not None:
            if len(symbol) != 1:
                raise ValueError("Symbol must be a single character.")
            if symbol.isspace():
                raise ValueError("Symbol cannot be whitespace.")

    def draw_square(self, width: int, symbol: str) -> str:
        """Draws a filled square.

        Args:
            width: The width (and height) of the square.
            symbol: The character to fill the square with.

        Returns:
            A multi-line string representing the square.
        """
        self._validate_input(width=width, symbol=symbol)
        return '\n'.join([symbol * width for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a filled rectangle.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to fill the rectangle with.

        Returns:
            A multi-line string representing the rectangle.
        """
        self._validate_input(width=width, height=height, symbol=symbol)
        return '\n'.join([symbol * width for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """Draws a filled parallelogram.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to fill the parallelogram with.

        Returns:
            A multi-line string representing the parallelogram.
        """
        self._validate_input(width=width, height=height, symbol=symbol)
        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)  # Efficient string concatenation
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a filled right-angled triangle.

        Args:
            width: The max width of the triangle.
            height: The height of the triangle.
            symbol: The character used.

        Returns:
            A multi-line string representing the triangle.
        """

        self._validate_input(width=width, height=height, symbol=symbol)
        # Adjust width dynamically based on height
        lines = []
        for i in range(1, height + 1):
            # Ensure the 'width' does not exceed the specified parameter, by calculating current_width
            current_width = min(i, width)
            lines.append(symbol * current_width)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """Draws a filled pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The character to fill the pyramid with.

        Returns:
            A multi-line string representing the pyramid.
        """
        self._validate_input(height=height, symbol=symbol)
        lines = []
        for i in range(1, height + 1):
            spaces = " " * (height - i)
            symbols = symbol * (2 * i - 1)
            lines.append(spaces + symbols)  # Efficient string concatenation
        return '\n'.join(lines)
def main():
    """Main function to demonstrate the AsciiArt class."""

    art = AsciiArt()

    # Example usage with error handling
    try:
        print("Square:")
        print(art.draw_square(5, "*"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "#"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(4, 6, "@"))

        print("\nTriangle:")
        print(art.draw_triangle(5, 6, "+"))  # Correct usage

        print("\nPyramid:")
        print(art.draw_pyramid(5, "$"))

        # Example of invalid input (uncomment to test)
        # print(art.draw_square(-5, "*"))      # Raises ValueError
        # print(art.draw_rectangle(4, 2, "  "))   # Raises ValueError
        # print(art.draw_pyramid(3, "AB"))    # Raises ValueError

    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
if __name__ == "__main__":
  main()
