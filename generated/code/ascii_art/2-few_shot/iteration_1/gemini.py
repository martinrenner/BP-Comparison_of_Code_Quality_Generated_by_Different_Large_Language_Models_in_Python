class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods to draw squares, rectangles, parallelograms,
    right-angled triangles, and pyramids using a specified symbol.  It adheres
    to principles of OOP and includes input validation to ensure robustness
    and security.  The design emphasizes readability, maintainability, and
    testability.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width, filled with the given symbol.

        Args:
            width: The width (and height) of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is negative or zero, or if the symbol is
                        not a single printable character or contains whitespace.
        """
        self._validate_input(width, symbol)  # Reuse common validation

        square = ""
        for _ in range(width):
            square += symbol * width + "\n"
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height, filled with the
        given symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is negative or zero, or if the
                        symbol is not a single printable character or contains
                        whitespace..
        """
        self._validate_input(width, symbol)
        self._validate_input(height, symbol)

        rectangle = ""
        for _ in range(height):
            rectangle += symbol * width + "\n"
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified width and height, filled with
        the given symbol.  The parallelogram slants to the right.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height is negative or zero, or if the
                        symbol is invalid.
        """
        self._validate_input(width, symbol)
        self._validate_input(height, symbol)

        parallelogram = ""
        for i in range(height):
            parallelogram += " " * i + symbol * width + "\n"
        return parallelogram

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.  Note: height parameter is not used in this.

        Args:
            width: The width of the base of the triangle.
            height: The height of the triangle (Not used in this implementation, preserved).
            symbol: The character to use for drawing the triangle.

        Returns:
            A multi-line string representing the ASCII art triangle.

        Raises:
            ValueError: If width is negative/zero or if the symbol is invalid.
        """

        self._validate_input(width, symbol)  # Validate based on width
        if height > 0:
            pass  # Avoid Unused Variable warning
        triangle = ""
        for i in range(1, width + 1):
            triangle += symbol * i + "\n"
        return triangle

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a pyramid of the specified height, filled with the given symbol.

        Args:
            height: The height of the pyramid.
            symbol: The character to use for drawing the pyramid.

        Returns:
            A multi-line string representing the ASCII art pyramid.

        Raises:
             ValueError: If height is negative or zero, or if symbol is invalid.
        """
        self._validate_input(height, symbol)

        pyramid = ""
        for i in range(1, height + 1):
            padding = " " * (height - i)
            pyramid += padding + symbol * (2 * i - 1) + padding + "\n"
        return pyramid

    def _validate_input(self, dimension: int, symbol: str) -> None:
        """
        Validates the input parameters for dimension and symbol.  This is a
        private helper method to reduce code duplication.

        Args:
            dimension: The dimension (width or height) to validate.
            symbol: The drawing symbol to validate.

        Raises:
            ValueError: If the dimension is not positive, or if the symbol is
                        not a single character, or if the symbol contains
                        whitespace.
        """
        if not isinstance(dimension, int) or dimension <= 0:
            raise ValueError("Dimension must be a positive integer.")

        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")

        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")



if __name__ == '__main__':
    art_generator = AsciiArt()

    # Example Usage and Testing
    try:
        print("Square:")
        print(art_generator.draw_square(5, "*"))

        print("Rectangle:")
        print(art_generator.draw_rectangle(7, 3, "#"))

        print("Parallelogram:")
        print(art_generator.draw_parallelogram(6, 4, "@"))

        print("Triangle:")
        print(art_generator.draw_triangle(5, 5, "+"))  # Height param is unused

        print("Pyramid:")
        print(art_generator.draw_pyramid(5, "$"))

        # Example of handling invalid input
        print("Invalid Input Test (negative width):")
        print(art_generator.draw_square(-5, "*"))  # Expected ValueError

    except ValueError as e:
        print(f"Error: {e}")

    try:
        print("Invalid Input Test (multi-character symbol):")
        print(art_generator.draw_square(5, "**"))  # Expected ValueError

    except ValueError as e:
        print(f"Error: {e}")

    try:
        print("Invalid Input Test (Whitespace symbol):")
        print(art_generator.draw_square(5, " "))  # Expected ValueError
    except ValueError as e:
        print(f"Error: {e}")
