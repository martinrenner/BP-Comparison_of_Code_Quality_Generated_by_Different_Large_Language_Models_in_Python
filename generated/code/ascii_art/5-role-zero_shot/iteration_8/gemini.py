class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None):
        """Validates the input parameters for drawing shapes.

        Args:
            symbol (str): The symbol to use for drawing the shape.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If the symbol is invalid or dimensions are negative.
        """

        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
        if width is not None and width <= 0:
            raise ValueError("Width must be a positive integer.")
        if height is not None and height <= 0:
            raise ValueError("Height must be a positive integer.")


    def draw_square(self, width: int, symbol: str) -> str:
        """Draws a square using the specified symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(symbol, width=width)
        return '\n'.join([symbol * width for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a rectangle using the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If input is invalid.
        """

        self._validate_input(symbol, width=width, height=height)
        return '\n'.join([symbol * width for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """Draws a parallelogram using the specified symbol.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If input is invalid.
        """

        self._validate_input(symbol, width=width, height=height)
        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a right-angled triangle.

        Args:
            width (int):  The width of the triangle's base.
            height (int):  The height of the triangle.
            symbol (str): The symbol to use.

        Returns:
            str: A multiline string representing the triangle.

        Raises:
            ValueError: If input is invalid.
        """

        self._validate_input(symbol, width=width, height=height)

        # We need to ensure the triangle grows correctly, based on height and width
        # We'll ensure each row's length is proportional to its height position
        lines = []
        for i in range(1, height + 1):
            # Calculate symbol count based on proportion of height
            symbol_count = int(i * (width / height))
            if symbol_count <=0 :
                continue #skip lines that will anyway have no symbols
            lines.append(symbol * symbol_count)
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """Draws a symmetrical pyramid using the specified symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If input is invalid.
        """

        self._validate_input(symbol, height=height)
        lines = []
        for i in range(1, height + 1):
            spaces = " " * (height - i)
            symbols = symbol * (2 * i - 1)
            lines.append(spaces + symbols)
        return '\n'.join(lines)


# Example usage
if __name__ == "__main__":
    art = AsciiArt()

    try:
        # Test cases
        print("Square:")
        print(art.draw_square(5, "*"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "#"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(6, 4, "@"))

        print("\nTriangle:")
        print(art.draw_triangle(5,5, "+"))  # Test right-angled triangle

        print("\nPyramid:")
        print(art.draw_pyramid(5, "$"))


        #test invalid input - multi-character symbol
        print("\nInvalid Input (Multi-character Symbol):")
        print(art.draw_square(4, "ab"))

    except ValueError as e:
        print(f"Error: {e}")

    try:
        #test invalid input - negative width
        print("\nInvalid Input (Negative Width):")
        print(art.draw_square(-4, "a"))

    except ValueError as e:
        print(f"Error: {e}")

    try:
        #test invalid input - whitespace symbol
        print("\nInvalid Input (Whitespace):")
        print(art.draw_square(4, " "))

    except ValueError as e:
        print(f"Error: {e}")


    try:
        #test triangle with different width/height
        #width greater than height
        print("\nTriangle (width > height):")
        print(art.draw_triangle(10,3, "+"))
        #width smaller than height
        print("\nTriangle (width < height):")
        print(art.draw_triangle(3,5, "+"))
        #very samll height
        print("\nTriangle (very small height):")
        print(art.draw_triangle(5,1, "+"))
        #same height as width
        print("\nTriangle (same height):")
        print(art.draw_triangle(5,5, "+"))
    except ValueError as e:
        print(f"Error: {e}")
