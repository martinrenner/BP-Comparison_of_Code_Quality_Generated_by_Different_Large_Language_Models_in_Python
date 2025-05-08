class AsciiArt:
    """
    A class for generating ASCII art shapes in the console.
    """

    def _validate_symbol(self, symbol: str):
        """Validates the symbol to ensure it's a single, printable character."""
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")

    def draw_square(self, width: int, symbol: str) -> str:
        """Draws a square of the given width filled with the specified symbol.

        Args:
            width: The width (and height) of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is not positive or symbol is invalid.
        """
        self._validate_symbol(symbol)
        if width <= 0:
            raise ValueError("Width must be a positive integer.")

        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a rectangle of the given width and height filled with the symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height are not positive or symbol is invalid.
        """
        self._validate_symbol(symbol)
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive integers.")

        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """Draws a parallelogram.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height are not positive or symbol is invalid.
        """
        self._validate_symbol(symbol)
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive integers.")

        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a right-angled triangle. Note: width parameter not used

        Args:
            width: The width of the triangle.
            height: The height of the triangle.
            symbol: The character to use.

        Returns:
            A multi-line string of the triangle.

        Raises:
            ValueError: If the base or height are not positive or symbol is invalid.
        """

        self._validate_symbol(symbol)
        if  height <= 0:
            raise ValueError("Height must be a positive integer.")

        lines = []
        for i in range(1, height + 1):
            lines.append(symbol * i)
        return "\n".join(lines)
        

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """Draws a symmetrical pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The character to use.

        Returns:
            A multi-line string representing the pyramid.

        Raises:
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_symbol(symbol)
        if height <= 0:
            raise ValueError("Height must be a positive integer.")

        lines = []
        for i in range(1, height + 1):
            padding = " " * (height - i)
            line = padding + symbol * (2 * i - 1) + padding
            lines.append(line)
        return "\n".join(lines)


# Example Usage
if __name__ == "__main__":
    art_generator = AsciiArt()

    try:
        print("Square:\n" + art_generator.draw_square(5, "*"))
        print("\nRectangle:\n" + art_generator.draw_rectangle(7, 3, "#"))
        print("\nParallelogram:\n" + art_generator.draw_parallelogram(4, 6, "X"))
        print("\nTriangle:\n" + art_generator.draw_triangle(5, 5, "@"))
        print("\nPyramid:\n" + art_generator.draw_pyramid(4, "+"))

        # Example of invalid input (uncomment to test exception handling):
        # print("\nInvalid Square:\n" + art_generator.draw_square(-5, "*"))
        #print("\nInvalid Symbol:\n" + art_generator.draw_square(5, "  "))
        print("\nInvalid Symbol:\n" + art_generator.draw_square(5, "**")) #Multichar test.
    except ValueError as e:
        print(f"Error: {e}")
