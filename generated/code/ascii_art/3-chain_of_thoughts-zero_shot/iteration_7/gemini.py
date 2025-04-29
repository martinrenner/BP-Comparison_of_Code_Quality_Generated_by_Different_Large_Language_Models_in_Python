class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width, filled with the given symbol.

        Args:
            width: The width of the square.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art square.

        Raises:
            ValueError: If width is not positive, or symbol is invalid.
            TypeError: If width is not an integer, or symbol is not a string.
        """
        self._validate_input(width, symbol, "width")
        return (symbol * width + "\n") * width

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height, filled with the given symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art rectangle.

        Raises:
             ValueError: If width/height is not positive, or symbol is invalid.
            TypeError: If width/height is not an integer, or symbol is not a string.
        """
        self._validate_input(width, symbol, "width")
        self._validate_input(height, symbol, "height")  # Validate height as well
        return (symbol * width + "\n") * height

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.  Each row is shifted one space to the right.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The drawing symbol.

        Returns:
            A multiline string representing the parallelogram.
            
        Raises:
            ValueError: If width/height is not positive, or symbol is invalid.
            TypeError: If width/height is not an integer, or symbol is not a string.
        """

        self._validate_input(width, symbol, "width")
        self._validate_input(height, symbol, "height")  # Validate height
        result = ""
        for i in range(height):
            result += " " * i + symbol * width + "\n"
        return result

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width: width of triangle's base.
            height: The height of the triangle.
            symbol: The drawing symbol.

        Returns:
            A multiline string representing the triangle.

        Raises:
            ValueError: If width/height is not positive, or symbol is invalid.
            TypeError: If width/height is not an integer, or symbol is not a string.
        """
        self._validate_input(width, symbol, "width")
        self._validate_input(height, symbol, "height") # Validate height

        if width != height:
            raise ValueError("For a right-angled triangle, width and height must be equal for proper diagonal growth.")

        result = ""
        for i in range(1, height + 1):
            result += symbol * i + "\n"
        return result

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The drawing symbol.

        Returns:
            A multiline string representing the pyramid.

        Raises:
            ValueError: If height is not positive, or symbol is invalid.
            TypeError: If height is not an integer, or symbol is not a string.
        """
        self._validate_input(height, symbol, "height") #height is checked

        result = ""
        for i in range(1, height + 1):
            spaces = " " * (height - i)
            result += spaces + symbol * (2 * i - 1) + spaces + "\n"
        return result

    def _validate_input(self, dimension: int, symbol: str, dimension_name: str):
        """
        Validates the input parameters.  A private helper method.

        Args:
            dimension: The dimension (width or height) to validate.
            symbol: The symbol to validate.
            dimension_name: string name of dimension for raise context

        Raises:
            ValueError: If dimension is not positive, or symbol is invalid.
            TypeError: If dimension is not an integer, or symbol is not a string.
        """

        if not isinstance(dimension, int):
            raise TypeError(f"{dimension_name} must be an integer.")
        if dimension <= 0:
            raise ValueError(f"{dimension_name} must be positive.")
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")



# Example Usage
if __name__ == "__main__":
    art = AsciiArt()

    try:
        print("Square:")
        print(art.draw_square(5, "#"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "*"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(6, 4, "@"))

        print("\nTriangle:")
        print(art.draw_triangle(5, 5, "+"))  #width = height

        print("\nPyramid:")
        print(art.draw_pyramid(5, "X"))

        # Example of invalid input
        # print(art.draw_square(-5, "#"))   # Raises ValueError
        # print(art.draw_rectangle(4, 2, "  "))  # Raises ValueError
        print("\nTriangle (invalid):")
        print(art.draw_triangle(4, 5, "+"))  # Raises ValueError

    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Error: {e}")
