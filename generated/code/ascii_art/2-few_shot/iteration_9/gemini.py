class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods to draw squares, rectangles, parallelograms,
    right-angled triangles, and pyramids using a specified symbol.  It adheres
    to principles of object-oriented programming, input validation, and
    efficient string manipulation.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width filled with the given symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to use for drawing the square.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is negative, symbol is empty, or symbol is multi-character.
        """
        self._validate_input(width, symbol)  # Reuse validation
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height, filled with the given symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing the rectangle.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is negative, symbol is empty, or symbol is multi-character.
        """
        self._validate_input(width, symbol, height)  # Reuse validation

        # Efficient string multiplication and joining
        return '\n'.join([symbol * width] * height)


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified width and height, filled with the given symbol.

        The parallelogram is drawn diagonally to the right, starting from the top-left corner.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height is negative, symbol is empty, or symbol is multi-character.
        """
        self._validate_input(width, symbol, height)

        lines = []
        for i in range(height):
            line = " " * i + symbol * width  # Efficiently create each line
            lines.append(line)
        return '\n'.join(lines)


    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle. The longest side has the given width.
        Triangle grows diagonally to the right

        Args:
            width (int): The width of the triangle.
            height (int): The height of the triangle
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art triangle.

        Raises:
            ValueError: If width or height is negative, symbol is empty, symbol is multi-character,
                        or width and height do not define a right-angled triangle.
        """

        self._validate_input(width, symbol, height)
        if width != height:
             raise ValueError("Width and height must be equal for a right-angled triangle.")

        lines = []
        for i in range(1, height + 1):
            lines.append(symbol * i)
        return '\n'.join(lines)


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the specified height, filled with the given symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing the pyramid.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is negative, symbol is empty, or symbol is multi-character.
        """
        self._validate_input(1, symbol, height) # Width can be arbitrary > 0

        lines = []
        for i in range(1, height + 1):
            spaces = " " * (height - i)
            symbols = symbol * (2 * i - 1) # Calculate symbols for symmetry
            lines.append(spaces + symbols)
        return '\n'.join(lines)


    def _validate_input(self, width: int, symbol: str, height: int = None) -> None:
        """
        Validates the input parameters for the drawing functions.

        Args:
            width (int): The width of the shape.
            symbol (str): The character to use for drawing.
            height (int, optional): The height of the shape. Defaults to None.

        Raises:
            ValueError: If width or height is negative, symbol is empty,
                        symbol is multi-character, or symbol consists of whitespace only.
        """
        if width < 0 or (height is not None and height < 0):
            raise ValueError("Width and height cannot be negative.")
        if not symbol:
            raise ValueError("Symbol cannot be empty.")
        if len(symbol) > 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace only.")



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
        print(art.draw_pyramid(5, "X"))

        # Example demonstrating error handling:
        print("\nInvalid Input (multi-character symbol):")
        print(art.draw_square(4, "AB")) # Raises ValueError

    except ValueError as e:
        print(f"Error: {e}")

    try:
        # Example demonstrating error handling:
        print("\nInvalid Input (negative width):")
        print(art.draw_square(-4, "A"))  # Raises ValueError
    except ValueError as e:
        print(f"Error: {e}")

    try:
        # Example demonstrating error handling:
        print("\nInvalid Input (width and height not equals for right-angled triangle):")
        print(art.draw_triangle(width=5, height=4, symbol="A"))  # Raises ValueError
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
