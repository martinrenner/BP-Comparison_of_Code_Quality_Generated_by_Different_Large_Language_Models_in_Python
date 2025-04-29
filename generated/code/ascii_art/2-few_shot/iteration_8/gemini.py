class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods to draw squares, rectangles, parallelograms,
    right-angled triangles, and pyramids using a specified symbol.  It includes
    input validation to ensure the correctness and security of the generated art.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None):
        """
        Validates the input parameters.

        Args:
            symbol (str): The symbol to use for drawing.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If the symbol is invalid, or if width/height are negative.
            TypeError: If width or height where required, but not provided.
        """
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

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
        
        if width is None and (height is not None and height <= 0):
            raise TypeError("Width must be an integer.") # Catches NoneType errors

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width using the given symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to use for drawing.

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
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.
        """
        self._validate_input(symbol, width=width, height=height)
        return "\n".join([symbol * width for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.
        """
        self._validate_input(symbol, width=width, height=height)
        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
          width (int):  The width of the base of the triangle
          height (int): The height of the triangle.
          symbol (str): The symbol to use.

        Returns:
            str: Multi-line string: the ASCII triangle.

        """
        self._validate_input(symbol, width=width, height=height)

        # Ensure triangle dimensions make sense.
        if width != height: # Forcing a 45-degree right angled triangle.
            raise ValueError("Width and Height should be equal to create proper triangle")                            

        lines = []
        for i in range(height):
            lines.append(symbol * (i + 1))
        return "\n".join(lines)


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the specified height.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use.

        Returns:
            str: A multi-line string representing the ASCII art.
        """
        self._validate_input(symbol, height=height)
        lines = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            lines.append(spaces + symbols)
        return "\n".join(lines)


# Example Usage
if __name__ == "__main__":
    art = AsciiArt()

    print("Square:")
    print(art.draw_square(5, "*"))

    print("\nRectangle:")
    print(art.draw_rectangle(4, 6, "#"))

    print("\nParallelogram:")
    print(art.draw_parallelogram(7, 3, "+"))

    print("\nTriangle:")
    print(art.draw_triangle(5, 5, "X"))  # Corrected: Now uses width and height

    print("\nPyramid:")
    print(art.draw_pyramid(4, "@"))

    # Example Test Cases (you would normally use a testing framework like unittest)

    try:
        art.draw_square(-2, "*")  # Test negative width
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        art.draw_rectangle(5, 3, "  ")  # Test multi-char symbol
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        art.draw_pyramid(3, " ")  # Test whitespace symbol
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    try:
        art.draw_rectangle(width=5, height='abc', symbol="@") # Test type for height
    except TypeError as e:
        print(f"Caught expected error: {e}")

    try:
        art.draw_triangle(width=6, height=3, symbol="&")  # Test for inproper triangle
    except ValueError as e:
        print(f"Caught expected error: {e}")   
