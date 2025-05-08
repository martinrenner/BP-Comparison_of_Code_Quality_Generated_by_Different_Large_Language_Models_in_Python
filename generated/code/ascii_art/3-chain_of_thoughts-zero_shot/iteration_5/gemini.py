class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    This class provides methods to draw various shapes (square, rectangle,
    parallelogram, right-angled triangle, and pyramid) using a specified symbol.
    It adheres to the ISO/IEC 25010 quality standards.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None) -> None:
        """Validates the input parameters."""

        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
        if width is not None and width <= 0:
            raise ValueError("Width must be a positive integer.")
        if height is not None and height <= 0:
            raise ValueError("Height must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width filled with the specified symbol.

        Args:
            width: The width of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A string representing the ASCII art square.
        """
        self._validate_input(symbol, width=width)
        return "\n".join([symbol * width] * width)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height, filled with symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to fill the rectangle with.

        Returns:
            A string representing the ASCII art rectangle.
        """
        self._validate_input(symbol, width=width, height=height)
        return "\n".join([symbol * width] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art parallelogram.
        """
        self._validate_input(symbol, width=width, height=height)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return "\n".join(result)

    def draw_triangle(self, width: int, height:int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width: The width of the triangle.
            height: The height of the triangle
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art triangle.
        """

        self._validate_input(symbol, width = width, height=height)
        if width > height:
           raise ValueError("For the triangle, the width has to be not greater than the height")

        result = []
        for i in range(height):
            result.append(symbol * (i + 1))
        return "\n".join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art pyramid.
        """
        self._validate_input(symbol, height=height)
        result = []
        for i in range(height):
            result.append(" " * (height - 1 - i) + symbol * (2 * i + 1))
        return "\n".join(result)

# --- Example Usage ---
if __name__ == "__main__":
    art = AsciiArt()

    try:
        print("Square:")
        print(art.draw_square(5, "#"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "*"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(6, 4, "@"))

        print("\nTriangle:")
        print(art.draw_triangle(4, 4, "+"))

        print("\nPyramid:")
        print(art.draw_pyramid(5, "X"))

        # Example of invalid input (uncomment to test error handling)
        # print(art.draw_square(4, "  "))
        # print(art.draw_pyramid(-3,"W"))
        print("\nTriangle (Invalid: width > height")
        print(art.draw_triangle(5,3,"!")) #Expected ValueError

    except ValueError as e:
        print(f"Error: {e}")
