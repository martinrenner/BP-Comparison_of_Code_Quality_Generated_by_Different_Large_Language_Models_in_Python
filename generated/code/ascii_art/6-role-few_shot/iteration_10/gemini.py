class AsciiArt:
    """
    A class for generating ASCII art shapes.

    This class provides methods to draw various geometric shapes using ASCII characters,
    ensuring input validation and efficient generation of the shapes.
    """

    def _validate_input(self, symbol: str, width: int = 0, height: int = 0) -> None:
        """
        Validates the input parameters for drawing shapes.

        Args:
            symbol (str): The symbol to use for drawing.
            width (int, optional): The width of the shape. Defaults to 0.
            height (int, optional): The height of the shape. Defaults to 0.

        Raises:
            ValueError: If the symbol is invalid or dimensions are negative.
            TypeError: If dimensions are not integers
        """

        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if not isinstance(width, int) or (height != 0 and not isinstance(height, int)):
            raise TypeError("Width and height must be integers.")
        if width < 0 or height < 0:
            raise ValueError("Width and height cannot be negative.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width using the specified symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A string representing the ASCII art square.
        """

        self._validate_input(symbol, width=width)
        if width == 0:
            return ""
        return "\n".join([symbol * width] * width)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given dimensions using the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A string representing the ASCII art rectangle.
        """

        self._validate_input(symbol, width=width, height=height)
        if width == 0 or height == 0:
             return ""
        return "\n".join([symbol * width] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram of the given dimensions using the specified symbol.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A string representing the ASCII art parallelogram.
        """

        self._validate_input(symbol, width=width, height=height)
        if width == 0 or height == 0:
             return ""
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return "\n".join(result)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
      """
      Draws a right-angled triangle.  It grows diagonally, starting top-left.

      Args:
          width (int): The maximum width of the triangle (at its base).
          height (int): The height of the triangle.
          symbol (str): The character to use to draw the triangle.

      Returns:
          str: The ASCII art representation of the triangle.

      Raises:
          ValueError: If input is invalid.
      """
      self._validate_input(symbol, width, height)
      if width == 0 or height == 0:
             return ""
      result = []
      for i in range(height):
        row_width = min(width, i + 1)  # Ensure width is not exceeded
        result.append(symbol * row_width)
      return "\n".join(result)
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a pyramid of the given height using the specified symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A string representing the ASCII art pyramid.
        """

        self._validate_input(symbol, height=height)  # width not needed
        if height == 0:
            return ""
        result = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            result.append(spaces + symbols)
        return "\n".join(result)
