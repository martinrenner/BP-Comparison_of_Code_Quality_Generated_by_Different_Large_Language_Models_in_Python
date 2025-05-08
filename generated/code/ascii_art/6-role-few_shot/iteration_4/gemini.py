class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    This class provides methods to draw various shapes like squares, rectangles,
    parallelograms, triangles, and pyramids using a specified symbol.
    It emphasizes input validation and ensures the generated shapes are
    completely filled with the chosen symbol.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width, filled with the specified symbol.

        Args:
            width (int): The width (and height) of the square.
            symbol (str): The single character to fill the square with.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is negative or symbol is invalid.
        """
        self._validate_input(width, symbol)
        return self._draw_rectangle(width, width, symbol)


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height, filled with the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The single character to fill the rectangle with.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is negative, or symbol is invalid.
        """
        self._validate_input(width, symbol, height)  # Validate both width and height
        return self._draw_rectangle(width, height, symbol)

    def _draw_rectangle(self, width: int, height: int, symbol: str) -> str:
      """
      Internal method to draw the rectangle.
      Keeps draw_rectangle and draw_square clean.
      """
      rows = []
      for _ in range(height):
          rows.append(symbol * width)
      return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified width, height, and symbol.

        The parallelogram grows diagonally to the right, starting from the
        top-left corner.  Each row is shifted by one space to the right
        compared to the previous row.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The single character to fill the parallelogram with.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height is negative, or symbol is invalid.
        """
        self._validate_input(width, symbol, height)
        rows = []
        for i in range(height):
            rows.append(" " * i + symbol * width)
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle. The triangle grows diagonally.

        Args:
            width (int): The maximum width of the triangle (at its base).
            height (int): The height of the triangle.
            symbol (str): The single character to fill the triangle with.

        Returns:
            str: A multi-line string representing the ASCII art triangle.

        Raises:
            ValueError: If width or height is negative, or symbol is invalid.
        """
        self._validate_input(width, symbol, height)

        # For a right-angled triangle, the height essentially dictates the
        # number of rows, and on each row the width should not exceed height
        if width > height:
            width = height

        rows = []
        for i in range(min(width, height)):  # Iterate up to the height
            rows.append(symbol * (i + 1))
        return "\n".join(rows)


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the given height, filled with the
        specified symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The single character to fill the pyramid with.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is negative, or symbol is invalid.
        """
        self._validate_input(height, symbol)  # Height is validated like width
        rows = []
        for i in range(height):
            padding = " " * (height - i - 1)
            row_symbols = symbol * (2 * i + 1)
            rows.append(padding + row_symbols)
        return "\n".join(rows)


    def _validate_input(self, width: int, symbol: str, height: int = None):
        """
        Validates the input parameters for the drawing methods.

        Common validation logic is grouped into the 'validate_input' method.

        Args:
            width (int): The width of the shape.
            symbol (str): The symbol to use for drawing.
            height (int, optional): The height of the shape (if applicable).

        Raises:
            ValueError: If any input is invalid.
        """
        if width < 0:
            raise ValueError("Width cannot be negative.")
        if height is not None and height < 0:
            raise ValueError("Height cannot be negative.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")


# Example usage and testing.
if __name__ == "__main__":
    art = AsciiArt()

    try:
        square = art.draw_square(5, "*")
        print("Square:\n" + square)

        rectangle = art.draw_rectangle(6, 3, "#")
        print("\nRectangle:\n" + rectangle)

        parallelogram = art.draw_parallelogram(4, 5, "+")
        print("\nParallelogram:\n" + parallelogram)

        triangle = art.draw_triangle(4, 6, "X")
        print("\nTriangle:\n" + triangle)
        triangle2 = art.draw_triangle(6, 4, "Y")
        print("\nTriangle2:\n" + triangle2)


        pyramid = art.draw_pyramid(5, "O")
        print("\nPyramid:\n" + pyramid)

        # Example of invalid input (negative width)
        # art.draw_square(-5, "*")  # This will raise a ValueError

        # Example of invalid input (multi-character symbol)
        # art.draw_rectangle(4, 4, "XX")  # This will raise a ValueError

        # Example of invalid input (whitespace symbol)
        # art.draw_pyramid(5, " ") # This will raise a ValueError

    except ValueError as e:
        print(f"Error: {e}")
