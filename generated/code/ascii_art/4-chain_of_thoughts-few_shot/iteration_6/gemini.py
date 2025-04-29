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
            TypeError: If width/height are not integers or if the symbol is not a string.
            ValueError: If width/height are not positive, or if the symbol is not a single character or contains whitespace.
        """

        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")

        if width is not None:
            if not isinstance(width, int):
                raise TypeError("Width must be an integer.")
            if width <= 0:
                raise ValueError("Width must be positive.")

        if height is not None:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer.")
            if height <= 0:
                raise ValueError("Height must be positive.")


    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width filled with the given symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the square.
        """
        self._validate_input(symbol, width=width)
        return '\n'.join([symbol * width] * width)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height filled with the given symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.
        """
        self._validate_input(symbol, width=width, height=height)
        return '\n'.join([symbol * width] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified width and height, filled with the given symbol.
        The parallelogram is slanted to the right.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.
        """
        self._validate_input(symbol, width=width, height=height)
        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with the specified width, filled with the given symbol.

        Args:
            width (int): The width of the triangle's base.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the triangle.

        """
        # Note: We assume width equates to height for a clean right-angled triangle.

        self._validate_input(symbol, width=width)
        lines = []
        for i in range(1, width + 1):
            lines.append(symbol * i)
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a pyramid with the specified height, filled with the given symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the pyramid.
        """
        self._validate_input(symbol, height=height)
        lines = []
        for i in range(1, height + 1):
            padding = " " * (height - i)
            row = symbol * (2 * i - 1)
            lines.append(padding + row)
        return '\n'.join(lines)

# --- Example Usage ---
if __name__ == '__main__':
    art = AsciiArt()

    try:
        square = art.draw_square(5, "#")
        print("Square:\n", square)

        rectangle = art.draw_rectangle(7, 3, "*")
        print("\nRectangle:\n", rectangle)

        parallelogram = art.draw_parallelogram(6, 4, "+")
        print("\nParallelogram:\n", parallelogram)

        triangle = art.draw_triangle(5, "X")
        print("\nTriangle:\n", triangle)
        
        pyramid = art.draw_pyramid(5, "O")
        print("\nPyramid:\n", pyramid)

        # Example of invalid input:
        # invalid_square = art.draw_square(-5, "#")  # Raises ValueError
        # invalid_symbol = art.draw_square(5, "##") # Raises ValueError
        # invalid_symbol2 = art.draw_square(5, " ") # Raises ValueError


    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
