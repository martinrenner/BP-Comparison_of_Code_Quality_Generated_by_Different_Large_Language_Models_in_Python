class AsciiArt:
    """
    A class for generating ASCII art shapes.

    This class provides methods to draw various shapes like squares, rectangles,
    parallelograms, triangles, and pyramids using a specified symbol.
    It includes input validation to ensure the correctness and security of the
    generated art.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None):
        """
        Validates the input parameters for drawing shapes.

        Args:
            symbol (str): The symbol to use for drawing the shape.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If the symbol is not a single character,
                        or if it is a whitespace,
                        or if width/height are negative or zero.
        """
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if width is not None and width <= 0:
            raise ValueError("Width must be a positive integer.")
        if height is not None and height <= 0:
            raise ValueError("Height must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width using the specified symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art square.
        """
        self._validate_input(symbol, width=width)
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
        self._validate_input(symbol, width=width, height=height)
        return '\n'.join([symbol * width for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram of the given width and height using the specified symbol.

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
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle using the specified symbol.  The triangle
        grows diagonally, so width and height co-define the size, though isn't strictly
        bound by those in every location.

        Args:
            width (int): Affects the width of the triangle.
            height (int): Affects the height (number of rows) of the triangle.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art triangle.
        """
        self._validate_input(symbol, width=width, height=height)

        # The 'height' determines the number of rows, consistent with other shapes
        lines = []
        for i in range(height):
          # The number of symbols in each increases, up to a maximum defined by 'width'
          num_symbols = min(i + 1, width)  # Constrain symbol count by width
          lines.append(symbol * num_symbols)
        return '\n'.join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the given height using the specified symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.
        """
        self._validate_input(symbol, height=height)
        lines = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            lines.append(spaces + symbols)
        return '\n'.join(lines)
