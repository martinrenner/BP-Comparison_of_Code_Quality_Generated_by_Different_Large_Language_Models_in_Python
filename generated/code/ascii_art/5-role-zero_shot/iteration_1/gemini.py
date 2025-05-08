class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods to draw different geometric shapes using a specified symbol,
    ensuring that the input is validated and the output is a multi-line string
    representing the ASCII art.
    """

    def _validate_input(self, width: int, height: int, symbol: str):
        """
        Validates the input parameters for drawing shapes.

        Args:
            width (int): The width of the shape.
            height (int): The height of the shape.  May be optional for some shapes (e.g., square, pyramid).
            symbol (str): The character to use for drawing the shape.

        Raises:
            ValueError: If input parameters are invalid.
        """
        if not isinstance(width, int) or (height is not None and not isinstance(height, int)):
            raise ValueError("Width and height must be integers.")

        if width < 0 or (height is not None and height < 0):
            raise ValueError("Width and height cannot be negative.")

        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")

        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width using the specified symbol.

        Args:
            width (int): The width (and height) of the square.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(width, width, symbol)  # Height is same as width
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height using the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(width, height, symbol)
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified width, height, and symbol.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(width, height, symbol)
        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.  The 'width' and 'height' represent the two
        sides of the right angle.

        Args:
            width (int): The width of the base of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol to use to draw.

        Returns:
            str: Multi-line string - ascii art.

        Raises:
            ValueError: If input is invalid
        """
        self._validate_input(width, height, symbol)

        if width != height:
            raise ValueError("Width and height must be equal for a right-angled triangle.")

        lines = []
        for i in range(height):
            lines.append(symbol * (i + 1))
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the given height.

        Args:
            height: The height of the pyramid.
            symbol: The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art.
        Raises:
            ValueError: If input is invalid.
        """

        self._validate_input(height, height, symbol) # Use height as a dummy width for validation

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
        print(art.draw_pyramid(5, "$"))

        # Example of invalid input (uncomment to test)
        # print(art.draw_square(-5, "*"))  # Raises ValueError
        # print(art.draw_rectangle(5,4,"XX"))

        print("\nTriangle, different width and height")
        print(art.draw_triangle(width=4, height=5, symbol="X"))

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

