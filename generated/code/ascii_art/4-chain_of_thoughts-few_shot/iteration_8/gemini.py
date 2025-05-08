class AsciiArt:
    """
    A class for generating various ASCII art shapes.
    """

    def _validate_input(self, width: int, height: int, symbol: str, is_pyramid: bool = False) -> None:
        """Validates common input parameters for drawing functions."""
        if not isinstance(width, int):
            raise TypeError("Width must be an integer.")
        if not is_pyramid:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer.")
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
        if width <= 0:
            raise ValueError("Width must be a positive integer.")
        if not is_pyramid:
            if height <= 0:
                raise ValueError("Height must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width filled with the specified symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to use for drawing the square.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            TypeError: If width is not an integer or symbol is not a string
            ValueError: If symbol is not a single character, is whitespace,
                        or if width is not positive.
        """

        self._validate_input(width, 1, symbol)  # height is irrelevant for square, use dummy value.
        return (symbol * width + '\n') * width

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height, filled with the symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string
            ValueError: If symbol is invalid, or dimensions are not positive.
        """
        self._validate_input(width, height, symbol)
        return (symbol * width + '\n') * height

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string
            ValueError: If symbol is invalid, or dimensions are not positive.
        """
        self._validate_input(width, height, symbol)
        result = ""
        for i in range(height):
            result += " " * i + symbol * width + "\n"
        return result

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The character to use.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            TypeError: If width/height are not integers or symbol is not a string
            ValueError: If symbol is invalid, or dimensions are not positive.
        """
        self._validate_input(width, height, symbol)
        if width != height:
            raise ValueError("Width and height must be equal for a right-angled triangle.")
        result = ""
        for i in range(1, height + 1):
            result += symbol * i + "\n"
        return result
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            TypeError: If height is not an integer or symbol is not a string
            ValueError: If symbol is invalid, or height is not positive.
        """
        self._validate_input(width=1, height=height, symbol=symbol, is_pyramid=True)  # width is not required
        if not isinstance(height, int):
            raise TypeError("Height must be an integer.")
        if height <= 0:
            raise ValueError("Height must be positive")

        result = ""
        for i in range(1, height + 1):
            spaces = " " * (height - i)
            symbols = symbol * (2 * i - 1)
            result += spaces + symbols + "\n"
        return result

# Example Usage (and basic testing)
if __name__ == "__main__":
    art = AsciiArt()

    try:
        print("Square:")
        print(art.draw_square(5, "*"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "#"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(6, 4, "@"))

        print("\nTriangle:")
        print(art.draw_triangle(4, 4, "+"))

        print("\nPyramid:")
        print(art.draw_pyramid(5, "X"))

        # Example of invalid input (uncomment to test error handling)
        # print("\nInvalid Square (negative width):")
        # print(art.draw_square(-5, "*"))  # Raises ValueError

        # print("\nInvalid Rectangle (multi-char symbol):")
        # print(art.draw_rectangle(4, 2, "##"))   #Raises ValueError
        
        # print("\nInvalid Rectangle (width is not int):")
        # print(art.draw_rectangle("4", 2, "#"))   #Raises TypeError

    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Error: {e}")
