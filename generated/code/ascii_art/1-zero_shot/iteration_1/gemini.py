class AsciiArt:
    """
    A class for generating ASCII art shapes.

    This class provides methods to draw various filled shapes (square, rectangle,
    parallelogram, right-angled triangle, and pyramid) using a specified symbol.
    It adheres to OOP principles and includes input validation.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of the specified width using the given symbol.

        Args:
            width: The width of the square (must be a positive integer).
            symbol: The character to use for drawing (must be a single printable character).

        Returns:
            A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is not positive, or if the symbol is invalid.
        """
        self._validate_input(width, symbol)
        return self._draw_rectangle_base(width, width, symbol)


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of the specified width and height using the given symbol.

        Args:
            width: The width of the rectangle (must be a positive integer).
            height: The height of the rectangle (must be a positive integer).
            symbol: The character to use for drawing (must be a single printable character).

        Returns:
            A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is not positive, or if the symbol is invalid.
        """
        self._validate_input(width, symbol, height)  # Height validation
        return self._draw_rectangle_base(width, height, symbol)

    def _draw_rectangle_base(self, width: int, height: int, symbol: str) -> str:
        """Helper function to draw a rectangle."""
        return "\n".join([symbol * width] * height)


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram.

        The parallelogram grows diagonally to the right, starting from the top-left corner.
        Each row is shifted by one space to the right compared to the previous row.

        Args:
            width: The width of the parallelogram (must be a positive integer).
            height: The height of the parallelogram (must be a positive integer).
            symbol: The character to use (must be a single printable character).

        Returns:
            A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height is not positive, or if symbol is invalid
        """
        self._validate_input(width, symbol, height)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return "\n".join(result)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle.

        The triangle grows diagonally to the right, starting from the top-left
        corner. The number of symbols in each row corresponds to the row number (1-based indexing).

        Args:
            width:  The base of the triangle. Must be a positive integer
            height: The height of the triangle (must be a positive integer).
            symbol: The character to use (must be a single printable character).

        Returns:
            A multi-line string representing the ASCII art right-angled triangle.

        Raises:
            ValueError: If base or height is not positive, or if the symbol is invalid.
        """

        self._validate_input(width, symbol, height)

        if width < height:
            raise ValueError("Width must be greater than or equals to height for the triangle.")

        result = []
        for i in range(1, height + 1):
            result.append(symbol * i)
        return "\n".join(result)


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid of the specified height using the given symbol.

        Args:
            height: The height of the pyramid (must be a positive integer).
            symbol: The character to use for drawing (must be a single printable character).

        Returns:
            A multi-line string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is not positive, or if the symbol is invalid.
        """
        self._validate_input(height, symbol)  # Only height needed for validation
        result = []
        for i in range(1, height + 1):
            spaces = " " * (height - i)
            symbols = symbol * (2 * i - 1)
            result.append(spaces + symbols)
        return "\n".join(result)

    def _validate_input(self, width, symbol, height=None):
      """Validates input for width, height, and symbol."""
      if not isinstance(width, int) or width <= 0 :
        raise ValueError("Width must be a positive integer.")
      if height is not None:
          if not isinstance(height, int) or height <= 0:
            raise ValueError("Height must be a positive integer.")
      if not isinstance(symbol, str) or len(symbol) != 1:
        raise ValueError("Symbol must be a single character.")
      if symbol.isspace():
          raise ValueError("Symbol cannot be a whitespace character.")


def main():
    """
    Main function to demonstrate the AsciiArt class functionality.
    """
    art_generator = AsciiArt()

    try:
        # Square
        square = art_generator.draw_square(5, "*")
        print("Square:\n" + square)

        # Rectangle
        rectangle = art_generator.draw_rectangle(7, 3, "#")
        print("\nRectangle:\n" + rectangle)

        # Parallelogram
        parallelogram = art_generator.draw_parallelogram(4, 6, "@")
        print("\nParallelogram:\n" + parallelogram)

        # Triangle
        triangle = art_generator.draw_triangle(5, 5, "+")
        print("\nTriangle:\n" + triangle)

        # Pyramid
        pyramid = art_generator.draw_pyramid(4, "$")
        print("\nPyramid:\n" + pyramid)

        # Example of input validation:
        # art_generator.draw_square(-5, "*") # Raises ValueError
        # art_generator.draw_rectangle(4, 2, "  ")  # Raises ValueError
        # art_generator.draw_pyramid(3, "")  # Raises ValueError
        # art_generator.draw_triangle(3, 5, "Q")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
