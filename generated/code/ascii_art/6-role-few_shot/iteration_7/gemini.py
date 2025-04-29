class AsciiArt:
    """
    A class for generating ASCII art shapes.

    This class provides methods to draw various geometric shapes filled with a specified symbol,
    ensuring that inputs are validated and the output is a multi-line string representing the shape.
    """

    def _validate_input(self, symbol: str, width: int, height: int = None) -> None:
        """
        Validates the input parameters for drawing shapes.

        Args:
            symbol (str): The symbol to use for drawing the shape.
            width (int): The width of the shape.
            height (int, optional): The height of the shape.  Defaults to None for shapes like squares.

        Raises:
            ValueError: If the symbol is invalid (not a single printable character),
                        or if width/height are negative or zero.
            TypeError: If width or height are not integers.
        """

        if not isinstance(symbol, str) or len(symbol) != 1 or not symbol.isprintable() or symbol.isspace():
            raise ValueError("Symbol must be a single, printable, non-whitespace character.")

        if not isinstance(width, int) or (height is not None and not isinstance(height, int)):
            raise TypeError("Width and height must be integers.")

        if width <= 0 or (height is not None and height <= 0):
            raise ValueError("Width and height must be positive integers.")


    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width filled with the given symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The symbol to fill the square with.

        Returns:
            str: A multi-line string representing the ASCII art square.
        """
        self._validate_input(symbol, width)
        return "\n".join([symbol * width for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height filled with the given symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to fill the rectangle with.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.
        """
        self._validate_input(symbol, width, height)
        return "\n".join([symbol * width for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the given width, height, and symbol.

        The parallelogram is drawn with each row shifted one space to the right, 
        starting from top-left corner.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character used to draw the parallelogram.

        Returns:
            str: A string representing the parallelogram.
        """
        self._validate_input(symbol, width, height)
        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with the given width, height, and symbol (grows diagonally).

        Args:
            width (int): The width of the base(bottom) of the triangle.
            height (int): The height of the triangle.
            symbol (str): The character used to draw the triangle.

        Returns:
            str: A string representing the triangle.

        Raises:
            ValueError: If height is more than width.
        """
        self._validate_input(symbol, width, height)
        if height > width:
            raise ValueError("Height cannot be greater than width for a right-angled triangle.")

        lines = []
        for i in range(height):
            lines.append(symbol * (i + 1))
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the specified height, filled with a given symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: Multi-line string representing the ASCII art.
        """
        self._validate_input(symbol, height, height)  # Reusing validation, height serves as both
        lines = []
        for i in range(height):
            spaces = " " * (height - 1 - i)
            symbols = symbol * (2 * i + 1)
            lines.append(spaces + symbols)
        return "\n".join(lines)



def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    art = AsciiArt()

    # Examples
    try:
        print("Square:")
        print(art.draw_square(5, "*"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "#"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(6, 4, "@"))

        print("\nTriangle:")
        print(art.draw_triangle(5, 5, "+"))

        print("\nPyramid:")
        print(art.draw_pyramid(4, "$"))

        # Example triggering input validation error:
        print("\nInvalid Input (Multi-character symbol):")
        print(art.draw_square(4, "**")) # Raises error

    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

