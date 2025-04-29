class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None) -> None:
        """
        Validates the input parameters.

        Args:
            symbol (str): The symbol to use for drawing.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If the symbol is invalid or width/height are negative.
            TypeError: If width/height are not integers.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")

        if width is not None:
            if not isinstance(width, int):
                raise TypeError("Width must be an integer.")
            if width < 0:
                raise ValueError("Width cannot be negative.")

        if height is not None:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer.")
            if height < 0:
                raise ValueError("Height cannot be negative.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width filled with the specified symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the square.
        """
        self._validate_input(symbol, width=width)
        return '\n'.join([symbol * width for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given dimensions filled with the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.
        """
        self._validate_input(symbol, width=width, height=height)
        return '\n'.join([symbol * width for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.  Each row is shifted one space to the right.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.
        """
        self._validate_input(symbol, width=width, height=height)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return '\n'.join(result)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
         Draws a right-angled triangle, that is expanded both vertically and horizontally.

         Args:
             width (int): The width of the triangle's base.
             height (int): The height of the triangle.
             symbol (str): The character to use.

         Returns:
             str: Multi-line string: the triangle.
         """

        self._validate_input(symbol, width = width, height = height)
        if width != height:
            raise ValueError("Width and height of the triangle must be equal.")

        result = []
        for i in range(1, height + 1):
            result.append(symbol * i)
        return '\n'.join(result)
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a pyramid of the given height filled with the specified symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the pyramid.
        """
        self._validate_input(symbol, height=height)
        result = []
        for i in range(height):
            result.append(" " * (height - i - 1) + symbol * (2 * i + 1))
        return '\n'.join(result)
