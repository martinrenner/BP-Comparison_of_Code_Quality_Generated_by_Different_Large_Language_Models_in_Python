class AsciiArt:
    """
    A class for generating 2D ASCII art shapes on the console.
    
    Provides methods to draw filled square, rectangle, parallelogram,
    right-angled triangle, and symmetrical pyramid.
    """

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validates that a dimension (width/height) is a positive integer.
        
        :param value: The dimension value to validate.
        :param name: The name of the dimension (for error messages).
        :raises ValueError: If the dimension is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer, got {value}.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the symbol is a single non-whitespace character.
        
        :param symbol: The symbol to validate.
        :raises ValueError: If symbol is not a single non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square with the given width and symbol.
        
        :param width: The side length of the square.
        :param symbol: The character used to draw the square.
        :return: A multiline string representing the square.
        :raises ValueError: If width is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)
        
        # Construct each row as the symbol repeated 'width' times.
        rows = [symbol * width for _ in range(width)]
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle with the given width, height, and symbol.
        
        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        :param symbol: The character used to draw the rectangle.
        :return: A multiline string representing the rectangle.
        :raises ValueError: If width/height are not positive integers or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        rows = [symbol * width for _ in range(height)]
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram with the given width, height, and symbol.
        Each row is shifted one space to the right from the row above.
        
        :param width: The width of each row of the parallelogram.
        :param height: The number of rows.
        :param symbol: The character used to draw the parallelogram.
        :return: A multiline string representing the parallelogram.
        :raises ValueError: If width/height are not positive integers or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        rows = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle.
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        The triangle is scaled so that:
          - It has 'height' rows.
          - The first row has 1 symbol.
          - The last row has 'width' symbols.
          - Intermediate rows interpolate linearly.
        
        :param width: The total number of symbols in the base (last row) of the triangle.
        :param height: The number of rows in the triangle.
        :param symbol: The character used to draw the triangle.
        :return: A multiline string representing the triangle.
        :raises ValueError: If width/height are not positive integers or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        rows = []
        if height == 1:
            # Single row triangle simply has width symbols.
            rows.append(symbol * width)
        else:
            for i in range(1, height + 1):
                # Ensure the first row has 1 symbol and the last row has 'width' symbols.
                # The formula below linearly increments the count.
                count = 1 + (width - 1) * (i - 1) // (height - 1)
                rows.append(symbol * count)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid with the given height and symbol.
        The pyramid has a centered appearance with an odd number of symbols on each row.
        
        :param height: The number of rows in the pyramid.
        :param symbol: The character used to draw the pyramid.
        :return: A multiline string representing the pyramid.
        :raises ValueError: If height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        
        rows = []
        # The width of the pyramid's base will be (2 * height - 1).
        for i in range(1, height + 1):
            symbols_count = 2 * i - 1
            spaces = " " * (height - i)
            rows.append(spaces + (symbol * symbols_count))
        return "\n".join(rows)


# Demo and simple test cases when running as a script
if __name__ == "__main__":
    art = AsciiArt()

    try:
        print("Square (width=4, symbol='#'):")
        print(art.draw_square(4, "#"))
        print("\nRectangle (width=6, height=3, symbol='*'):")
        print(art.draw_rectangle(6, 3, "*"))
        print("\nParallelogram (width=5, height=4, symbol='@'):")
        print(art.draw_parallelogram(5, 4, "@"))
        print("\nTriangle (width=7, height=5, symbol='^'):")
        print(art.draw_triangle(7, 5, "^"))
        print("\nPyramid (height=4, symbol='+'):")
        print(art.draw_pyramid(4, "+"))
    except ValueError as ve:
        print("Input error:", ve)
