class AsciiArt:
    """
    A class for generating ASCII art shapes in the console.
    """

    def _validate_input(self, width=None, height=None, symbol=None):
        """
        Validates the input parameters for the drawing functions.

        Args:
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.
            symbol (str, optional): The symbol to use for drawing.

        Raises:
            ValueError: If width/height is not positive, or if the symbol is invalid.
            TypeError: If width/height are not integers
        """

        if width is not None:
            if not isinstance(width, int):
                raise TypeError("Width must be an integer.")
            if width <= 0:
                raise ValueError("Width must be a positive integer.")

        if height is not None:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer.")
            if height <= 0:
                raise ValueError("Height must be a positive integer.")

        if symbol is not None:
            if not isinstance(symbol, str):
                raise TypeError("Symbol must be a string.")
            if len(symbol) != 1:
                raise ValueError("Symbol must be a single character.")
            if symbol.isspace():
                raise ValueError("Symbol cannot be whitespace.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width, filled with the specified symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The symbol to use for drawing the square.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is not positive or if the symbol is invalid.
        """
        self._validate_input(width=width, symbol=symbol)

        square = ""
        for _ in range(width):
            square += symbol * width + "\n"
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height, filled with the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If width/height are not positive or if symbol is invalid.
        """
        self._validate_input(width=width, height=height, symbol=symbol)

        rectangle = ""
        for _ in range(height):
            rectangle += symbol * width + "\n"
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.  Each row is shifted one space to the right.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width/height are not positive, or if symbol is invalid.
        """
        self._validate_input(width=width, height=height, symbol=symbol)

        parallelogram = ""
        for i in range(height):
            parallelogram += " " * i + symbol * width + "\n"
        return parallelogram

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.  It grows diagonally to the right.

        Args:
            width: the base
            height: the height
            symbol (str): The symbol to use for drawing.

        Returns:
            str: Multi-line string: ASCII art triangle.

        Raises:
            ValueError: If width/height are not positive, or if symbol is invalid.
        """
        
        self._validate_input(width=width, height=height, symbol=symbol)
        
        if width != height:
            raise ValueError("Width and height of right triangle must be same for this implementation.")

        triangle = ""
        for i in range(1, height + 1):
            triangle += symbol * i + "\n"
        return triangle
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.

        Raises:
             ValueError: If height is not positive, or if symbol is invalid.
        """
        self._validate_input(height=height, symbol=symbol)

        pyramid = ""
        for i in range(1, height + 1):
            pyramid += " " * (height - i) + symbol * (2 * i - 1) + "\n"
        return pyramid


if __name__ == "__main__":
    art_generator = AsciiArt()

    # Draw a square
    try:
        square_art = art_generator.draw_square(5, '#')
        print(square_art)
    except ValueError as e:
        print(f"Error: {e}")

    # Draw a rectangle
    try:
        rectangle_art = art_generator.draw_rectangle(7, 3, '*')
        print(rectangle_art)
    except ValueError as e:
        print(f"Error: {e}")

    # Draw a parallelogram
    try:
        parallelogram_art = art_generator.draw_parallelogram(6, 4, '@')
        print(parallelogram_art)
    except ValueError as e:
        print(f"Error: {e}")

    # Draw a triangle
    try:
        triangle_art = art_generator.draw_triangle(5, 5, '!')
        print(triangle_art)
    except ValueError as e:
        print(f"Error: {e}")

    # Draw a pyramid
    try:
        pyramid_art = art_generator.draw_pyramid(4, '$')
        print(pyramid_art)
    except ValueError as e:
        print(f"Error: {e}")

    # Example of invalid input
    try:
        invalid_art = art_generator.draw_square(-5, '#')  # Negative width
        print(invalid_art)
    except ValueError as e:
        print(f"Error: {e}")  # Expected: Error: Width must be a positive integer.

    try:
        invalid_art = art_generator.draw_square(5, '##')  # Invalid symbol
        print(invalid_art)
    except ValueError as e:
        print(f"Error: {e}")  # Expected: Error: Symbol must be a single character.
