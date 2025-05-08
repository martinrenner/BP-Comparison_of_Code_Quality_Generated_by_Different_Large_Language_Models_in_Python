class AsciiArt:
    """
    A class for generating ASCII art shapes.

    This class provides methods to draw various geometric shapes using ASCII characters,
    ensuring input validation and efficient rendering.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None):
        """
        Validates the input parameters for drawing shapes.

        Args:
            symbol (str): The character to use for drawing the shape.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If the symbol is not a single printable character,
                        or if width/height are negative or zero.
            TypeError: If width or height are not integers (when provided).
        """

        if not isinstance(symbol, str) or len(symbol) != 1 or not symbol.isprintable() or symbol.isspace():
            raise ValueError("Symbol must be a single printable character.")

        if width is not None:
            if not isinstance(width, int):
                raise TypeError("Width must be an integer.")
            if width <= 0:
                raise ValueError("Width must be a positive integer.")

        if height is not None:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer.")
            if height <= 0:
                raise ValueError("Height must be a positive integer.")


    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width using the given symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the square.
        """

        self._validate_input(symbol, width=width)
        return '\n'.join([symbol * width for _ in range(width)])


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height using the given symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.
        """

        self._validate_input(symbol, width=width, height=height)
        return '\n'.join([symbol * width for _ in range(height)])


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.  It grows diagonally to the right, starting from the top-left corner.

        Args:
            width (int): The width of the parallelogram's base.
            height (int): The height of the parallelogram.
            symbol (str): The character to use.

        Returns:
            str: A multi-line string representing the parallelogram.
        """

        self._validate_input(symbol, width=width, height=height)
        lines = []
        for i in range(height):
            lines.append(' ' * i + symbol * width)
        return '\n'.join(lines)


    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle. It grows diagonally to the right, starting from the top-left corner.

        Args:
           width (int):  Maximum width of the triangle (at the bottom or top, depending on orientation)
           height (int): The height of the triangle.
            symbol (str): The character to use.

        Returns:
            str: A multi-line string representing the triangle.
        """
        self._validate_input(symbol, width=width, height=height)

        if width > height:
          raise ValueError("For the triangle, the width must be less or equal height")

        lines = []
        for i in range(height):
            lines.append(symbol * (i+1) )
        return '\n'.join(lines)
        


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the specified height using the given symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the pyramid.
        """

        self._validate_input(symbol, height=height)
        lines = []
        for i in range(height):
            spaces = ' ' * (height - 1 - i)
            symbols = symbol * (2 * i + 1)
            lines.append(spaces + symbols)
        return '\n'.join(lines)


# Example Usage
if __name__ == "__main__":
    art = AsciiArt()

    try:
        print("Square:")
        print(art.draw_square(5, '*'))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, '#'))

        print("\nParallelogram:")
        print(art.draw_parallelogram(6, 4, '+'))

        print("\nTriangle:")
        print(art.draw_triangle(4, 4, 'X')) # width and height should be the same

        print("\nPyramid:")
        print(art.draw_pyramid(5, '@'))

        # Example of invalid input
        # print(art.draw_square(4, '  ')) # This will raise a ValueError
        # print(art.draw_rectangle(-2, 5, '$')) # This will raise a ValueError

    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Error: {e}")

