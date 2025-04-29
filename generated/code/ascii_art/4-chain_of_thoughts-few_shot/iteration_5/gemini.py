class AsciiArt:
    """
    A class for generating ASCII art shapes in the console.
    """

    def _validate_input(self, symbol: str, width: int = 0, height: int = 0):
        """
        Validates the input parameters for drawing functions.

        Args:
            symbol (str): The character to use for drawing.
            width (int, optional): The width of the shape. Defaults to 0.
            height (int, optional): The height of the shape. Defaults to 0.

        Raises:
            TypeError: If width or height are not integers.
            ValueError: If symbol is not a single character, is whitespace,
                        or if width/height are negative.
        """
        if not isinstance(width, int) or (height != 0 and not isinstance(height, int)):
            raise TypeError("Width and height must be integers.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
        if width < 0 or height < 0:
            raise ValueError("Width and height cannot be negative.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width and symbol.

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
        Draws a rectangle of the specified width, height, and symbol.

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
        Draws a parallelogram.  Each row is shifted one space to the right.

        Args:
            width (int): The width of each row.
            height (int): The number of rows.
            symbol (str): The character to use.

        Returns:
            str: The parallelogram as a multi-line string.
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
            width (int): The maximum width of the triangle.
            height (int): The height of the triangle (number of rows).
            symbol (str): The character to use.

        Returns:
            str: The triangle as a multi-line string.
        
        Raises:
            ValueError: If height is greater than width.
        """
        self._validate_input(symbol, width=width, height=height)

        if height > width:
            raise ValueError("Height cannot be greater than width for a right-angled triangle.")

        result = []
        for i in range(1, height + 1):
            result.append(symbol * i)
        return '\n'.join(result)
        

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height (int): The height of the pyramid (number of rows).
            symbol (str): The character to use.

        Returns:
            str: The pyramid as a multi-line string.
        """
        self._validate_input(symbol, height=height)
        result = []
        for i in range(1, height + 1):
            spaces = " " * (height - i)
            symbols = symbol * (2 * i - 1)
            result.append(spaces + symbols)
        return '\n'.join(result)


# Example Usage
if __name__ == "__main__":
    art = AsciiArt()

    try:
        print("Square:")
        print(art.draw_square(5, "*"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "#"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(4, 5, "+"))

        print("\nTriangle:")
        print(art.draw_triangle(5, 5, "X"))  # Corrected test case

        print("\nPyramid:")
        print(art.draw_pyramid(5, "O"))

        # Example of invalid input
        print("\nInvalid Input Test (Whitespace):")
        print(art.draw_square(4, " "))  # Should raise ValueError

    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Error: {e}")
