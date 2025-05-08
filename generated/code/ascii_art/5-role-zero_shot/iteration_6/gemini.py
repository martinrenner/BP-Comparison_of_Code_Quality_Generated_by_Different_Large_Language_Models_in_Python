class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None):
        """
        Validates the input parameters for the drawing functions.

        Args:
            symbol (str): The symbol to use for drawing the shape.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If the symbol is not a single printable character,
                        or if width/height are negative or zero.
        TypeError: If width/height is not provided when required by caller function
        """

        if not symbol or len(symbol) != 1 or not symbol.isprintable() or symbol.isspace():
            raise ValueError("Symbol must be a single printable character.")

        if width is not None:
            if not isinstance(width, int) or width <= 0:
                raise ValueError("Width must be a positive integer.")

        if height is not None:
            if not isinstance(height, int) or height <= 0:
                raise ValueError("Height must be a positive integer.")
        
        if width is None and (height is not None and height>0):
            raise TypeError("Width must be provided.")

        if height is None and (width is not None and width>0):
            raise TypeError("Height must be provided")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width using the specified symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art square.
        """

        self._validate_input(symbol, width, width)
        return '\n'.join([symbol * width for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height using the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.
        """
        self._validate_input(symbol, width, height)
        return '\n'.join([symbol * width for _ in range(height)])


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with given width, height and symbol.

        Args:
            width (int): Width of the parallelogram.
            height (int): Height of the parallelogram.
            symbol (str): Symbol to use for drawing.

        Returns:
            str: Multi-line string: parallelogram.
        """
        self._validate_input(symbol, width, height)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return "\n".join(result)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle
        Args:
            width (int): Width of the triangle.
            height (int): Height of the triangle.
            symbol (str): Symbol to use.
        Returns:
            str: A multi-line string representation of the triangle
        """
        self._validate_input(symbol, width, height)
        if width != height: # right-angled isosceles
            raise ValueError("Width and height must be equal for a right-angled triangle.")

        result = []
        for i in range(height):
            result.append(symbol * (i+1))
        return '\n'.join(result)


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the given height using the specified symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.
        """
        self._validate_input(symbol, height=height)  # Only height is needed for a pyramid

        result = []
        for i in range(height):
            spaces = " " * (height - 1 - i)
            symbols = symbol * (2 * i + 1)
            result.append(spaces + symbols)
        return '\n'.join(result)



# Example usage:
if __name__ == "__main__":
    art = AsciiArt()

    # Valid Inputs
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

    except ValueError as e:
        print(f"Error: {e}")

    # Invalid input examples (uncomment to test)
    try:
        print("\nInvalid Square (negative width):")
        print(art.draw_square(-5, "*"))  # Raises ValueError
    except ValueError as e:
        print(f"Error: {e}")

    try:
        print("\nInvalid Rectangle (multi-char symbol):")
        print(art.draw_rectangle(4, 2, "ab"))  # Raises ValueError
    except ValueError as e:
        print(f"Error: {e}")

    try:
      print("\nInvalid Triangle (width != height):")
      print(art.draw_triangle(width=2, height=3, symbol='+')) # Raises ValueError
    except ValueError as e:
        print(f"Error: {e}")
