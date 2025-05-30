class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods to draw squares, rectangles, parallelograms,
    right-angled triangles, and pyramids using a specified symbol. It includes
    input validation to ensure correctness and security.
    """

    def _validate_input(self, symbol: str, width: int = 0, height: int = 0) -> None:
        """
        Validates the input parameters for drawing shapes.

        Args:
            symbol (str): The symbol to use for drawing.
            width (int, optional): The width of the shape. Defaults to 0.
            height (int, optional): The height of the shape. Defaults to 0.

        Raises:
            ValueError: If the symbol is not a single character,
                        is whitespace, or if width/height are negative.
            TypeError: If width or height are not integers.
        """
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
        if not isinstance(width, int) or (height != 0 and not isinstance(height, int)):
            raise TypeError("Width and height must be integers.")
        if width < 0 or height < 0:
            raise ValueError("Width and height cannot be negative.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width using the given symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art square.
        """
        self._validate_input(symbol, width=width)
        return "\n".join([symbol * width for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height using the given symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.
        """
        self._validate_input(symbol, width=width, height=height)
        return "\n".join([symbol * width for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram of the specified width and height.

        The parallelogram's rows are shifted by one space to the right
        starting from the top-left corner.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.
        """
        self._validate_input(symbol, width=width, height=height)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return "\n".join(result)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.  Grows diagonally to the right.

        Args:
            width (int): The base width of the triangle.
            height (int): The height of the triangle (should generally equal base).
            symbol (str): The symbol to use for drawing the triangle.

        Returns:
            str: The string representation of the triangle.
        """
        self._validate_input(symbol, width=width, height=height)

        if width != height:
            raise ValueError("For a right triangle, height and width must be equal in this implementation.")

        result = []
        for i in range(height):
            result.append(symbol * (i + 1))
        return "\n".join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the specified height.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.
        """
        self._validate_input(symbol, height=height)
        result = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            result.append(spaces + symbols)
        return "\n".join(result)


# Example Usage and Testing
if __name__ == "__main__":
    art_generator = AsciiArt()

    # Square
    print("Square:")
    print(art_generator.draw_square(5, "*"))

    # Rectangle
    print("\nRectangle:")
    print(art_generator.draw_rectangle(7, 3, "#"))

    # Parallelogram
    print("\nParallelogram:")
    print(art_generator.draw_parallelogram(6, 4, "@"))

    # Right-Angled Triangle
    print("\nRight-Angled Triangle:")
    print(art_generator.draw_triangle(5, 5, "+"))

    # Pyramid
    print("\nPyramid:")
    print(art_generator.draw_pyramid(5, "$"))


    # Example of invalid input (multichar symbol)
    try:
        print(art_generator.draw_square(4, "ab"))
    except ValueError as e:
        print(f"\nError (multichar): {e}")

    # Example of invalid input (whitespace)
    try:
        print(art_generator.draw_square(4, " "))
    except ValueError as e:
        print(f"\nError (whitespace): {e}")

    # Example of invalid input (negative width)
    try:
        print(art_generator.draw_rectangle(4,-3,'%'))
    except ValueError as e:
        print(f"\nError (negative): {e}")

    # Example of invalid input (incorrect type)
    try:
        print(art_generator.draw_rectangle(4.3, 3, '%'))  # type: ignore
    except TypeError as e:
        print(f"\nError (incorrect type): {e}")
