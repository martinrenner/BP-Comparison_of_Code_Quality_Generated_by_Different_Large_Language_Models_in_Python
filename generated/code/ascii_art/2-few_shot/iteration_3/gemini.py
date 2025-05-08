class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods to draw squares, rectangles, parallelograms,
    right-angled triangles, and pyramids using a specified symbol.  It includes
    input validation to ensure correctness and security.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width filled with the specified symbol.

        Args:
            width: The width of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A string representing the ASCII art square.

        Raises:
            ValueError: If width is negative, symbol is empty, contains
            multiple characters, or is whitespace.
        """
        self._validate_input(width, symbol)  # Call the shared validation

        square = ""
        for _ in range(width):
            square += symbol * width + "\n"
        return square


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height, filled with the
        specified symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is negative, symbol is empty,
            contains multiple characters, or is whitespace.
        """
        self._validate_input(width, symbol, height)

        rectangle = ""
        for _ in range(height):
            rectangle += symbol * width + "\n"
        return rectangle


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram of the specified width and height, filled with
        the given symbol.  The parallelogram is slanted to the right.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height is negative, symbol is empty,
            contains multiple characters, or is whitespace.
        """
        self._validate_input(width, symbol, height)

        parallelogram = ""
        for i in range(height):
            parallelogram += " " * i + symbol * width + "\n"
        return parallelogram


    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with the specified width, height, and symbol.

        Args:
            width: Width of triangle's base.
            height: The height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art right-angled triangle.

        Raises:
            ValueError: If width or height is negative, symbol is empty, contains
                        multiple characters, or is whitespace.
        """

        self._validate_input(width, symbol, height)

        if width != height:
            # Ensure that input values are valid for this case
            raise ValueError("Width and height must be equal for a right-angled triangle.")

        triangle = ""
        for i in range(height):
            triangle += symbol * (i + 1) + "\n"
        return triangle
    

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a pyramid of the given height filled with the specified symbol.

        Args:
            height: The height of the pyramid.
            symbol: The character to use for drawing the pyramid.

        Returns:
            A string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is negative, symbol is empty, contains
            multiple characters, or is whitespace.
        """
        self._validate_input(height, symbol)  # height is validated as a dimension

        pyramid = ""
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            pyramid += spaces + symbols + "\n"
        return pyramid


    def _validate_input(self, *args):
        """
        Validates input parameters for drawing functions. This is a private helper method.

        Args:
            *args: Variable number of arguments:  The first n-1 arguments are
                   dimensions (width, height), and the last argument is always the symbol.

        Raises:
            ValueError: If any dimension is negative, or if the symbol is empty,
                        contains multiple characters, or consists of whitespace.
        """
        *dimensions, symbol = args

        for dim in dimensions:
            if not isinstance(dim, int) or dim < 0:
                raise ValueError("Dimensions must be non-negative integers.")

        if not isinstance(symbol, str) or not symbol:
            raise ValueError("Symbol must be a non-empty string.")
        if len(symbol) > 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")


def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    art = AsciiArt()

    # Example usage with error handling:
    try:
        print(art.draw_square(5, "*"))
        print(art.draw_rectangle(7, 3, "#"))
        print(art.draw_parallelogram(6, 4, "@"))
        print(art.draw_triangle(5, 5, "+"))
        print(art.draw_pyramid(5, "$"))

        # Example of invalid input:

        # print(art.draw_square(-5, "*"))       # Raises ValueError: Dimensions must be non-negative integers.
        # print(art.draw_rectangle(7, 3, "##"))  # Raises ValueError: Symbol must be a single character.
        # print(art.draw_parallelogram(6, 4, ""))  # Raises ValueError: Symbol must be a non-empty string.
        # print(art.draw_triangle(5, 2, "+")) # Raises ValueError: Width and height must be equal for a right-angled triangle.
        # print(art.draw_pyramid(5, " "))       # Raises ValueError: Symbol cannot be whitespace.
       

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

