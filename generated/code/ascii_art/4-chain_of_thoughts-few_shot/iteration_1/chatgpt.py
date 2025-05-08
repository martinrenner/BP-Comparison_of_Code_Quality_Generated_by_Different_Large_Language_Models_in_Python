class AsciiArt:
    """
    A console-based 2D ASCII art generator that draws various filled shapes.
    
    Methods:
        draw_square(width: int, symbol: str) -> str
        draw_rectangle(width: int, height: int, symbol: str) -> str
        draw_parallelogram(width: int, height: int, symbol: str) -> str
        draw_triangle(width: int, height: int, symbol: str) -> str
        draw_pyramid(height: int, symbol: str) -> str
    """

    def _validate_positive_int(self, name: str, value: int) -> None:
        """
        Validates that a numerical dimension is a positive integer.
        
        Args:
            name (str): The name of the parameter (e.g., "width", "height").
            value (int): The value to validate.
            
        Raises:
            ValueError: If the value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that a symbol is a single non-whitespace character.
        
        Args:
            symbol (str): The symbol to validate.
            
        Raises:
            ValueError: If the symbol is not exactly one character or is whitespace.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square using the given width and symbol.
        
        Each side of the square will have the specified width.
        
        Args:
            width (int): The number of characters for each side.
            symbol (str): The printable symbol to fill the square.
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If the width is not a positive integer or the symbol is invalid.
        """
        self._validate_positive_int("width", width)
        self._validate_symbol(symbol)
        
        # Build square: Create 'width' rows, each with 'width' symbols.
        rows = [symbol * width for _ in range(width)]
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle using the given width, height, and symbol.
        
        Args:
            width (int): The number of characters in each row.
            height (int): The number of rows.
            symbol (str): The printable symbol to fill the rectangle.
            
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If width or height is not a positive integer or the symbol is invalid.
        """
        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)
        
        rows = [symbol * width for _ in range(height)]
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram using the given width, height, and symbol.
        
        Each row of the shape is shifted to the right by one additional space,
        starting from the top-left corner.
        
        Args:
            width (int): The number of symbols per row (not including the shift).
            height (int): The number of rows.
            symbol (str): The printable symbol to fill the parallelogram.
            
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If width or height is not a positive integer or the symbol is invalid.
        """
        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)
        
        rows = []
        for i in range(height):
            # Each row is shifted by 'i' spaces then filled with 'width' symbols.
            row = " " * i + symbol * width
            rows.append(row)
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle using the given width (base length),
        height (number of rows), and symbol.
        
        The triangle is drawn such that:
          - If height == 1, it produces a single line containing 'width' symbols.
          - If height > 1, the top row starts with one symbol and the bottom row has
            exactly 'width' symbols. The number of symbols increases in a linear manner.
        
        Args:
            width (int): The number of symbols in the triangle's base (bottom row).
            height (int): The number of rows in the triangle.
            symbol (str): The printable symbol to fill the triangle.
            
        Returns:
            str: A multi-line string representing the triangle.
            
        Raises:
            ValueError: If width or height is not a positive integer or the symbol is invalid.
        """
        self._validate_positive_int("width", width)
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)
        
        rows = []
        if height == 1:
            rows.append(symbol * width)
        else:
            for i in range(height):
                # Calculate the number of symbols so that row 0 has 1 symbol and the last row has 'width' symbols.
                # Formula: n_symbols = round(1 + (width - 1) * (i / (height - 1)))
                n_symbols = round(1 + (width - 1) * i / (height - 1))
                # Ensure at least one symbol is printed.
                n_symbols = max(1, n_symbols)
                rows.append(symbol * n_symbols)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical filled pyramid using the given height and symbol.
        
        The pyramid has a base width of 2*height - 1 and is centered horizontally.
        
        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): The printable symbol to fill the pyramid.
            
        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If height is not a positive integer or the symbol is invalid.
        """
        self._validate_positive_int("height", height)
        self._validate_symbol(symbol)
        
        rows = []
        for i in range(height):
            # Calculate left padding: (height - i - 1) spaces.
            spaces = " " * (height - i - 1)
            # Number of symbols in the current row: 2*i + 1.
            symbols_count = 2 * i + 1
            row = spaces + (symbol * symbols_count) + spaces
            rows.append(row)
        return "\n".join(rows)


if __name__ == "__main__":
    # Example usage and basic testing of the AsciiArt class.
    art = AsciiArt()

    try:
        print("Square (width=5):")
        print(art.draw_square(5, "*"))
        print("\nRectangle (width=10, height=4):")
        print(art.draw_rectangle(10, 4, "#"))
        print("\nParallelogram (width=10, height=4):")
        print(art.draw_parallelogram(10, 4, "$"))
        print("\nTriangle (width=10, height=5):")
        print(art.draw_triangle(10, 5, "@"))
        print("\nPyramid (height=5):")
        print(art.draw_pyramid(5, "+"))
    except ValueError as ve:
        print(f"Input Error: {ve}")
