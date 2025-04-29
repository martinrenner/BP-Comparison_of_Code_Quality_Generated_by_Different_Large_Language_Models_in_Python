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
            TypeError: If width or height are not integers (when provided).
            ValueError: If symbol is not a single character, is whitespace,
                        or if width/height are not positive.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
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
        Draws a square of the specified width and symbol.

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
        Draws a rectangle of the specified width, height, and symbol.

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
        Draws a parallelogram of the specified width, height, and symbol.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing.

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
        Draws a right-angled triangle.  Note:  The relationship
        between width and height affects the triangle's appearance.
        Ideally, height should be proportional to width for a visually
        pleasing triangle.  This implementation prioritizes using both
        width and height as specified.

        Args:
            width (int): Maximum width of the triangle.
            height (int):  The height of the triangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art triangle.
        """
        self._validate_input(symbol, width=width, height=height)
        lines = []
        for i in range(height):
            # Calculate the number of symbols for this row.  This ensures
            # that the width constraint is honored, even if it results in
            # a "truncated" triangle if height > width.
            num_symbols = min(i + 1, width)
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the specified height and symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.
        """
        self._validate_input(symbol, height=height)
        lines = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            lines.append(spaces + symbols)
        return "\n".join(lines)
