class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods to draw different geometric shapes using ASCII
    characters, adhering to principles of clean architecture and maintainability.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None):
        """
        Validates the input parameters for drawing shapes.

        Args:
            symbol (str): The character to use for drawing the shape.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If the symbol is not a single printable character,
                        or if width/height are negative or zero.
            TypeError: If width or height are not integers.
        """

        if not isinstance(symbol, str) or len(symbol) != 1 or not symbol.isprintable() or symbol.isspace():
            raise ValueError("Symbol must be a single printable character.")

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
        Draws a square of the given width using the specified symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art square.
        """
        self._validate_input(symbol, width=width)  # Validate inputs
        return '\n'.join([symbol * width for _ in range(width)])


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height using the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.
        """
        self._validate_input(symbol, width=width, height=height) # Validate inputs
        return '\n'.join([symbol * width for _ in range(height)])


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified width, height, and symbol.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multiline string representing the ASCII art parallelogram.
        """
        self._validate_input(symbol, width=width, height=height)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return "\n".join(result)



    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows to width and height and the specified symbol.

        Args:
            width (int): The width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol to use.

        Returns:
            str: A multi-line string representing the ASCII art triangle.
        """
        self._validate_input(symbol, width=width, height=height) # Validate inputs

        # Determine the maximum number of characters needed in a row (for scaling)
        max_chars = max(width, height)
        result = []

        # Drawing logic considering both width and height
        for i in range(height):
            drawn_symbols = min(i + 1, width)  # Limit the number of symbols by width
            line = symbol * drawn_symbols
            result.append(line)

        return '\n'.join(result)


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the given height using the specified symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.
        """
        self._validate_input(symbol, height=height)  # Validate inputs

        result = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            result.append(spaces + symbols)
        return '\n'.join(result)


if __name__ == "__main__":
    art = AsciiArt()

    # Example usage with validation and error handling
    try:
        square = art.draw_square(5, "*")
        print("Square:\n", square)

        rectangle = art.draw_rectangle(7, 3, "#")
        print("\nRectangle:\n", rectangle)

        parallelogram = art.draw_parallelogram(6, 4, "@")
        print("\nParallelogram:\n", parallelogram)

        triangle = art.draw_triangle(5, 5, "+")  # width, height, symbol
        print("\nTriangle:\n", triangle)

        pyramid = art.draw_pyramid(5, "$")
        print("\nPyramid:\n", pyramid)

        # Example of invalid input
        invalid_square = art.draw_square(-5, "*")  # Raises ValueError
        print(invalid_square)
        
        invalid_square2 = art.draw_square(5, "**")  # Raises ValueError
        print(invalid_square)
        
    except ValueError as e:
        print(f"ValueError: {e}")
    except TypeError as e:
        print(f"TypeError: {e}")

