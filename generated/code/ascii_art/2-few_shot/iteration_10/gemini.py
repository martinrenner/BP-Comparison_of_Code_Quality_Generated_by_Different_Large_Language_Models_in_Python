class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods to draw squares, rectangles, parallelograms,
    right-angled triangles, and pyramids using a specified symbol.  It includes
    input validation to ensure the correctness and security of the generated art.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width filled with the given symbol.

        Args:
            width: The width of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is negative or symbol is invalid.
        """
        self._validate_input(width, symbol)
        return self._draw_rectangle(width, width, symbol)  # Reuse rectangle logic


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle with the specified width, height and fill symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is negative, or symbol is invalid.
        """
        self._validate_input(width, symbol, height)  # Validate both dimensions
        return self._draw_rectangle(width, height, symbol)


    def _draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Helper function to draw rectangle"""
        return '\n'.join([symbol * width for _ in range(height)])


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height is negative, or symbol is invalid.
        """
        self._validate_input(width, symbol, height)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return "\n".join(result)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width: The width of the base of the triangle.
            height: The height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII art triangle.

        Raises:
            ValueError: If width or height is negative, or if the symbol is invalid.
        """
        self._validate_input(width, symbol, height)

        if width > height:
            raise ValueError("For a right-angled triangle, height must be greater or equal to width.")

        result = []
        for i in range(height):
            # Only draw up to the width, maintaining right-angled property
            draw_width = min(i + 1, width)
            result.append(symbol * draw_width)
        return "\n".join(result)


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is negative, or if symbol is invalid.
        """
        self._validate_input(height, symbol) # Width is derived, not input
        result = []
        for i in range(height):
            spaces = " " * (height - 1 - i)
            symbols = symbol * (2 * i + 1)  # Correct number of symbols
            result.append(spaces + symbols)
        return "\n".join(result)

    def _validate_input(self, dimension1: int, symbol: str, dimension2: int = None):
        """
        Validates the input parameters for drawing functions.

        Args:
             dimension1: The first dimension (width or height).
             symbol: The character to use for drawing.
             dimension2: Second dimension of the shape (optional, if the shape have only one dimension).

        Raises:
            ValueError: If dimensions are negative, or the symbol is invalid
        """
        if dimension1 < 0 or (dimension2 is not None and dimension2 < 0):
            raise ValueError("Dimensions cannot be negative.")

        if not symbol or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")

        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")


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
        print(art.draw_triangle(4, 4, "+"))


        print("\nPyramid:")
        print(art.draw_pyramid(5, "$"))

        # Example demonstrating exception handling
        print("\nInvalid Input (Negative width):")
        print(art.draw_square(-5, "*"))
        

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

