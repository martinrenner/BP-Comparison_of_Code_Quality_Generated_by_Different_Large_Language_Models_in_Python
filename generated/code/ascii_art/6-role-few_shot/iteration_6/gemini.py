class AsciiArt:
    """
    A class for generating ASCII art shapes.

    This class provides methods to draw various shapes like squares, rectangles,
    parallelograms, triangles, and pyramids using a specified symbol.
    """

    def _validate_input(self, symbol: str):
        """
        Validates the input symbol.

        Args:
            symbol (str): The symbol to use for drawing.

        Raises:
            ValueError: If the symbol is not a single character or is whitespace.
        """
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")

    def _validate_dimensions(self, width: int, height: int = None):
        """
        Validates the dimensions (width and height).

        Args:
            width (int):  The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If width or height is negative or zero.
        """
        if width <= 0:
            raise ValueError("Width must be positive.")
        if height is not None and height <= 0:
            raise ValueError("Height must be positive.")


    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width using the specified symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(symbol)
        self._validate_dimensions(width)

        lines = []
        for _ in range(width):
            lines.append(symbol * width)
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height using the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(symbol)
        self._validate_dimensions(width, height)

        lines = []
        for _ in range(height):
            lines.append(symbol * width)
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str):  The symbol to draw with.

        Returns:
            str: The parallelogram as a string.

        Raises:
             ValueError: If input validation fails.
        """
        self._validate_input(symbol)
        self._validate_dimensions(width, height)

        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)
        return "\n".join(lines)


    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
           width (int): The maximum width of the triangle
           height (int): The height of the triangle.
           symbol (str): The symbol to draw with.

        Returns:
            str: The triangle as a string

        Raises:
            ValueError: If input validation fails.
        """

        self._validate_input(symbol)
        self._validate_dimensions(width, height)

        lines = []
        for i in range(height):
            lines.append(symbol * min(i + 1, width)) # Ensure width constraint
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to draw with.

        Returns:
            str: The pyramid as a string.

        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(symbol)
        self._validate_dimensions(height, height)  # Use height for both to validate

        lines = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            lines.append(spaces + symbols)
        return "\n".join(lines)
