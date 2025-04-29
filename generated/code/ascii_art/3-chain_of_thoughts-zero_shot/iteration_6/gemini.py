class AsciiArt:
    """
    A class for generating various ASCII art shapes.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width filled with the given symbol.

        Args:
            width: The width of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A string representing the ASCII art square.

        Raises:
            ValueError: If width is not positive, or symbol is not a single
                        printable character.
        """
        self._validate_input(width, symbol)  # Call the validation method
        return '\n'.join([symbol * width for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height, filled with the given symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height are not positive, or symbol is invalid.
        """
        self._validate_input(width, symbol, height) # Validate both dimensions
        return '\n'.join([symbol * width for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The symbol to use for drawing.

        Returns:
            A string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height are not positive, or if the symbol is not valid.
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
            width: The base width of the triangle.
            height: The height of the triangle.
            symbol: The symbol to use for drawing.

        Returns:
            A string representing the ASCII art triangle.

        Raises:
            ValueError:  If width or height are not positive, if width is greater than height
                        or if the symbol is invalid.
        """
        self._validate_input(width, symbol, height)
        if width > height:
            raise ValueError("Width cannot be greater than height for a right-angled triangle.")

        result = []
        for i in range(1, width + 1):
            result.append(symbol * i)
        return "\n".join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The symbol to use.

        Returns:
            A string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_input(height, symbol) # We use a single-argument validation here.
        result = []
        for i in range(1, height + 1):
            spaces = " " * (height - i)
            symbols = symbol * (2 * i - 1)
            result.append(spaces + symbols)
        return "\n".join(result)

    def _validate_input(self, *args):
        """
        Validates the input parameters for the drawing functions.  Checks for
        positive dimensions and a single, printable symbol.

        Args:
            *args: A variable number of arguments.  The first n-1 arguments are
            treated as dimensions (width, height) and must be positive integers.
            The last argument is always the symbol and must be a single
            printable character.

        Raises:
            ValueError: If any dimension is not a positive integer, or if
                the symbol is not a single, printable character.
        """
        *dimensions, symbol = args

        for dim in dimensions:
            if not isinstance(dim, int) or dim <= 0:
                raise ValueError("Dimensions must be positive integers.")

        if not isinstance(symbol, str) or len(symbol) != 1 or not symbol.isprintable() or symbol.isspace():
            raise ValueError("Symbol must be a single printable character (and not whitespace).")

# --- End of Class Definition ---


# Example Usage (and basic testing)
if __name__ == "__main__":
    art_generator = AsciiArt()

    try:
        square = art_generator.draw_square(5, "#")
        print("Square:\n", square)

        rectangle = art_generator.draw_rectangle(7, 3, "*")
        print("\nRectangle:\n", rectangle)

        parallelogram = art_generator.draw_parallelogram(6, 4, "+")
        print("\nParallelogram:\n", parallelogram)
        
        triangle = art_generator.draw_triangle(4, 4, "X")
        print("\nTriangle:\n", triangle)

        pyramid = art_generator.draw_pyramid(5, "@")
        print("\nPyramid:\n", pyramid)

        # Demonstrating error handling:
        # invalid_square = art_generator.draw_square(-5, "#")  # Raises ValueError
        # invalid_symbol = art_generator.draw_rectangle(4, 2, "##")  # Raises ValueError
        # invalid_triangle = art_generator.draw_triangle(5, 3, "O") # Raises ValueError
        invalid_pyramid = art_generator.draw_pyramid(5, ' ') # Raises ValueError

    except ValueError as e:
        print(f"Error: {e}")
