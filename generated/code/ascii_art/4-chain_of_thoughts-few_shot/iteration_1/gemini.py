class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width filled with the specified symbol.

        Args:
            width: The width (and height) of the square.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art square.

        Raises:
            ValueError: If width is not positive, or symbol is invalid.
        """
        self._validate_input(width, symbol)  # Call the validation method
        square = ""
        for _ in range(width):
            square += symbol * width + "\n"
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height filled with the specified symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is not positive, or symbol is invalid.
        """
        self._validate_input(width, symbol, height) # Added height validation
        rectangle = ""
        for _ in range(height):
            rectangle += symbol * width + "\n"
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The symbol to use.

        Returns:
            str: The generated parallelogram.

        Raises:
            ValueError: If width or height is not positive, or if the symbol is invalid.
        """
        self._validate_input(width, symbol, height)
        parallelogram = ""
        for i in range(height):
            parallelogram += " " * i + symbol * width + "\n"
        return parallelogram

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width:  The width of the triangle's base.
            height: The height of the triangle.
            symbol:  The symbol to use.

        Returns:
            str: The generated triangle.

        Raises:
           ValueError:  If width or height is not positive, or if symbol is invalid.
        """
        self._validate_input(width, symbol, height)

        if width != height:
            raise ValueError("For a right-angled triangle, width and height must be equal.")

        triangle = ""
        for i in range(height):
            triangle += symbol * (i + 1) + "\n"
        return triangle
        

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The symbol to use.

        Returns:
           str: The generated pyramid.

        Raises:
            ValueError: If height are not positive, or if symbol is invalid.
        """
        self._validate_input(height, symbol)  # height acts as width for validation

        pyramid = ""
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            pyramid += spaces + symbols + spaces + "\n" # Added spaces on *both* sides
        return pyramid
    

    def _validate_input(self, width: int, symbol: str, height: int = None) -> None:
        """
        Validates the input parameters.  This is a private helper method.

        Args:
            width:  The width of the shape.
            symbol: The symbol to use.
            height: The height of the shape (optional, for shapes like rectangles).

        Raises:
            ValueError: If inputs are invalid.
        """
        if not isinstance(width, int) or (height is not None and not isinstance(height, int)):
            raise TypeError("Width and height must be integers.")
        if width <= 0 or (height is not None and height <= 0):
            raise ValueError("Width and height must be positive integers.")
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")



# Example Usage
if __name__ == "__main__":
    art = AsciiArt()

    try:
        print(art.draw_square(5, "*"))
        print(art.draw_rectangle(7, 3, "#"))
        print(art.draw_parallelogram(4, 6, "@"))
        print(art.draw_triangle(5, 5, "+"))  # Corrected
        print(art.draw_pyramid(4, "X"))

        # Example of invalid input
        # print(art.draw_square(-5, "*"))  # This will raise a ValueError
        # print(art.draw_rectangle(4, 6, "  ")) # This will raise ValueError
    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Error: {e}")



class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width filled with the specified symbol.

        Args:
            width: The width (and height) of the square.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art square.

        Raises:
            ValueError: If width is not positive, or symbol is invalid.
        """
        self._validate_input(width, symbol)  # Call the validation method
        square = ""
        for _ in range(width):
            square += symbol * width + "\n"
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height filled with the specified symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is not positive, or symbol is invalid.
        """
        self._validate_input(width, symbol, height) # Added height validation
        rectangle = ""
        for _ in range(height):
            rectangle += symbol * width + "\n"
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The symbol to use.

        Returns:
            str: The generated parallelogram.

        Raises:
            ValueError: If width or height is not positive, or if the symbol is invalid.
        """
        self._validate_input(width, symbol, height)
        parallelogram = ""
        for i in range(height):
            parallelogram += " " * i + symbol * width + "\n"
        return parallelogram

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width:  The width of the triangle's base.
            height: The height of the triangle.
            symbol:  The symbol to use.

        Returns:
            str: The generated triangle.

        Raises:
           ValueError:  If width or height is not positive, or if symbol is invalid.
           Or width and height are different.
        """
        self._validate_input(width, symbol, height)

        if width != height:
            raise ValueError("For a right-angled triangle, width and height must be equal.")

        triangle = ""
        for i in range(height):
            triangle += symbol * (i + 1) + "\n"
        return triangle
        

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The symbol to use.

        Returns:
           str: The generated pyramid.

        Raises:
            ValueError: If height are not positive, or if symbol is invalid.
        """
        self._validate_input(height, symbol)  # height acts as width for validation

        pyramid = ""
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            pyramid += spaces + symbols + spaces + "\n" # Added spaces on *both* sides
        return pyramid
    

    def _validate_input(self, width: int, symbol: str, height: int = None) -> None:
        """
        Validates the input parameters.  This is a private helper method.

        Args:
            width:  The width of the shape.
            symbol: The symbol to use.
            height: The height of the shape (optional, for shapes like rectangles).

        Raises:
            ValueError: If inputs are invalid.
        """
        if not isinstance(width, int) or (height is not None and not isinstance(height, int)):
            raise TypeError("Width and height must be integers.")
        if width <= 0 or (height is not None and height <= 0):
            raise ValueError("Width and height must be positive integers.")
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")


# Example Usage
if __name__ == "__main__":
    art = AsciiArt()

    try:
        print(art.draw_square(5, "*"))
        print(art.draw_rectangle(7, 3, "#"))
        print(art.draw_parallelogram(4, 6, "@"))
        print(art.draw_triangle(5, 5, "+"))  # Corrected
        print(art.draw_pyramid(4, "X"))

        # Example of invalid input
        # print(art.draw_square(-5, "*"))  # This will raise a ValueError
        # print(art.draw_rectangle(4, 6, "  ")) # This will raise ValueError
    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Error: {e}")
