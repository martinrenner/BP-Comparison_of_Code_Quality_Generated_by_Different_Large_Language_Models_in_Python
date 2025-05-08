class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width filled with the given symbol.

        Args:
            width: The width of the square.
            symbol: The character to fill the square with.

        Returns:
            A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If the symbol is invalid or width is negative.
        """
        self._validate_input(width, symbol)
        if width == 0:
            return ""

        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height, filled with the symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to fill the rectangle with.

        Returns:
            A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If the symbol is invalid or width/height is negative.
        """
        self._validate_input(width, symbol, height)
        if width == 0 or height == 0:
            return ""

        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to fill the parallelogram with.

        Returns:
            A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If the symbol is invalid or width/height is negative.
        """
        self._validate_input(width, symbol, height)
        if width == 0 or height == 0:
            return ""

        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character for triangle.

        Returns:
            A multi-line string representing the ASCII art triangle.

        Raises:
            ValueError: If the symbol is invalid or width/height is negative.
       """
        self._validate_input(width, symbol, height)
        if width == 0 or height == 0:
            return ""

        lines = []
        # Ensure the drawing does not exceed the given height
        for i in range(min(width, height)):
            lines.append(symbol * (i + 1))
        return "\n".join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The character to fill the pyramid with.

        Returns:
            A multi-line string representing the ASCII art pyramid.

        Raises:
            ValueError: If the symbol is invalid or height is negative.
        """
        self._validate_input(None, symbol, height)  # No width for pyramid
        if height == 0:
            return ""

        lines = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            lines.append(spaces + symbols)
        return "\n".join(lines)

    def _validate_input(self, width: int | None, symbol: str, height: int | None = None):
        """
        Validates the input parameters for the drawing functions.

        Args:
            width: The width of the shape (can be None for shapes like pyramid).
            symbol: The character to fill the shape with.
            height: The height of the shape (optional, can be None).

        Raises:
            ValueError: If any of the input parameters are invalid.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")

        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        
        if width is not None:
            if not isinstance(width, int) or width < 0:
                raise ValueError("Width must be a non-negative integer.")
        if height is not None:
            if not isinstance(height, int) or height < 0:
                raise ValueError("Height must be a non-negative integer.")


# --- Example Usage and Testing ---

if __name__ == "__main__":
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
        
        print("\nZero width Square:")
        print(art.draw_square(0, "*"))  # Empty
        
        print("\nRectangle with zero height:")
        print(art.draw_rectangle(7, 0, "#")) # Empty
       
        print("\nInvalid Input (multi-character symbol):")
        print(art.draw_square(5, "**"))   #ValueError

    except ValueError as e:
        print(f"Error: {e}")
