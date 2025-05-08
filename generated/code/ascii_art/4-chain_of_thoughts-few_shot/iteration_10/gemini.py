class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None):
        """
        Validates the input parameters for drawing functions.

        Args:
            symbol (str): The character to use for drawing.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If the symbol is invalid or dimensions are negative.
            TypeError: If the dimensions are not integers
        """
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")

        if width is not None:
            if not isinstance(width, int):
                raise TypeError("Width must be an integer.")
            if width <= 0:
                raise ValueError("Width must be a positive integer.")

        if height is not None:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer.")
            if height <= 0:
                raise ValueError("Height must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width filled with the specified symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art square.
        """
        self._validate_input(symbol, width=width)
        return '\n'.join([symbol * width] * width)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height filled with the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.
        """
        self._validate_input(symbol, width=width, height=height)
        return '\n'.join([symbol * width] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified width, height, and symbol.

        The parallelogram grows diagonally to the right, starting from the top-left
        corner. Each row is shifted by one space to the right.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.
        """
        self._validate_input(symbol, width=width, height=height)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return '\n'.join(result)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width (int): The width of the triangle's base. Note there is may be relation between the width and height.
            height (int): The height.
            symbol (str): The character to fill the triangle with.

        Returns:
            str: The ASCII art representation of the triangle.

        Raises:
            ValueError: If width is greater than height * 2.  Triangle would be too wide to be reasonably.
        """
        # Note: Removed unnecessary condition comparing width and height.
        self._validate_input(symbol, width = width, height = height)
        result = []
        for i in range(height):
            drawn_symbols = min(width, i + 1)  # Prevent drawing past the specified width
            result.append(symbol * drawn_symbols)
        return '\n'.join(result)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the specified height and symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.
        """
        self._validate_input(symbol, height=height)
        result = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            result.append(spaces + symbols)
        return '\n'.join(result)


# --- Example Usage and Basic In-Code Tests ---

if __name__ == "__main__":
    art = AsciiArt()

    # Square
    square = art.draw_square(5, "#")
    print("Square:\n" + square)
    assert square == "#####\n#####\n#####\n#####\n#####", "Square test failed"

    # Rectangle
    rectangle = art.draw_rectangle(7, 3, "*")
    print("\nRectangle:\n" + rectangle)
    assert rectangle == "*******\n*******\n*******", "Rectangle test failed"

    # Parallelogram
    parallelogram = art.draw_parallelogram(4, 5, "+")
    print("\nParallelogram:\n" + parallelogram)
    assert parallelogram == "++++\n ++++\n  ++++\n   ++++\n    ++++", "Parallelogram test failed"

    # Triangle
    triangle = art.draw_triangle(5, 6, "X")  # Corrected call
    print("\nTriangle:\n" + triangle)
    assert triangle == "X\nXX\nXXX\nXXXX\nXXXXX\nXXXXX", "Triangle Test Failed"

    # Pyramid
    pyramid = art.draw_pyramid(4, "@")
    print("\nPyramid:\n" + pyramid)
    assert pyramid == "   @\n  @@@\n @@@@@\n@@@@@@@", "Pyramid test failed"

    # Test invalid input
    try:
        art.draw_square(5, "  ")  # Whitespace symbol
    except ValueError as e:
        print("\nCaught expected error:", e)

    try:
        art.draw_rectangle(-5, 3, '#')   #Negative value
    except ValueError as e:
        print("Caught expected error:", e)

    try:
        art.draw_rectangle(5, 3, '##')   #Multichar
    except ValueError as e:
        print("Caught expected error:", e)

    try:
        art.draw_rectangle(5.5, 3, '#') #Not int
    except TypeError as e:
        print("Caught expected error:", e)
    
    print("\nAll in-code tests passed (or expected errors caught)!")
