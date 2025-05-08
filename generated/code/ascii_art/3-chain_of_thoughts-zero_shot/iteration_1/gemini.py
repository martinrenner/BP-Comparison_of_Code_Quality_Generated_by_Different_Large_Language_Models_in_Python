class AsciiArt:
    """
    A class for generating various ASCII art shapes.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None):
        """
        Validates the input parameters for the drawing functions.

        Args:
            symbol (str): The symbol to use for drawing.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If the symbol is invalid or dimensions are negative.
            TypeError: If width or height are not integers.
        """
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
        if width is not None and not isinstance(width, int):
            raise TypeError("Width must be an integer.")
        if height is not None and not isinstance(height, int):
            raise TypeError("Height must be an integer.")
        if (width is not None and width <= 0) or (height is not None and height <= 0):
            raise ValueError("Width and height must be positive integers.")


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
        return '\n'.join([symbol * width] * width)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height filled with the specified symbol.

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
        Draws a parallelogram with the given width and height, filled with the specified symbol.
        The parallelogram grows diagonally to the right.

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
        Draws a right-angled triangle.

        Args:
            width (int): The width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol to use for drawing the triangle.

        Returns:
            str: The ASCII art representation of the triangle.

        Raises:
            ValueError: If the width and height don't match, and height will be assign to width.
        """
        self._validate_input(symbol, width=width, height=height)

        if width != height:
            print("Warning: For a right-angled triangle, height should ideally match width. Adjusting height to match width.")
            height = width
        
        result = []
        for i in range(1, height + 1):
            result.append(symbol * i)
        return '\n'.join(result)


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the specified height, filled with the given symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the pyramid.
        """
        self._validate_input(symbol, height=height)
        result = []
        for i in range(1, height + 1):
            spaces = " " * (height - i)
            symbols = symbol * (2 * i - 1)
            result.append(spaces + symbols)
        return '\n'.join(result)


if __name__ == '__main__':
    art = AsciiArt()

    # Get user input for symbol
    while True:
        try:
            user_symbol = input("Enter a single character to use for drawing: ")
            art._validate_input(user_symbol)  # Reuse validation
            break  # Exit loop if input is valid
        except ValueError as e:
            print(e)

    # Examples and testing
    print("\nSquare:")
    print(art.draw_square(5, user_symbol))

    print("\nRectangle:")
    print(art.draw_rectangle(7, 3, user_symbol))

    print("\nParallelogram:")
    print(art.draw_parallelogram(4, 6, user_symbol))

    print("\nTriangle:")
    print(art.draw_triangle(5, 5, user_symbol))
    
    print("\nPyramid:")
    print(art.draw_pyramid(5, user_symbol))


    # Example of invalid input (handled gracefully)
    try:
        print("\nAttempting to draw a square with an invalid symbol:")
        print(art.draw_square(4, "  "))  # Multi-character symbol
    except ValueError as e:
        print(e)

    try:
        print("\nAttempting to draw a rectangle with negative dimensions:")
        print(art.draw_rectangle(-4, 5, user_symbol))  # Negative width
    except ValueError as e:
        print(e)
