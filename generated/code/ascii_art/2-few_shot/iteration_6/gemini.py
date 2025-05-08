class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods to draw squares, rectangles, parallelograms,
    right-angled triangles, and pyramids using a specified symbol.  It includes
    input validation to ensure the correctness and security of the generated art.
    """

    def _validate_input(self, width: int, height: int, symbol: str) -> None:
        """
        Validates the common input parameters for shape drawing.

        Args:
            width (int): The width of the shape.
            height (int): The height of the shape.
            symbol (str): The character used to draw the shape.

        Raises:
            ValueError: If any input is invalid.
        """
        if not isinstance(width, int) or (width is not None and width <= 0):  # Allow width to be None for pyramid
            raise ValueError("Width must be a positive integer.")
        if not isinstance(height, int) or height <= 0:
            raise ValueError("Height must be a positive integer.")
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")


    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width using the given symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character used to draw the square.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(width, 1, symbol)  # Height is not used but validated as 1 for consistency
        return '\n'.join([symbol * width] * width)


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height using the given symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character used to draw the rectangle.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(width, height, symbol)
        return '\n'.join([symbol * width] * height)


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the given dimensions and symbol.

        The parallelogram grows diagonally to the right, starting from the top-left.
        Each row is shifted by one space to the right compared to the previous row.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(width, height, symbol)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return '\n'.join(result)


    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle. The triangle grows diagonally. The longest side is
        determined by the height.

        Args:
            width (int): The 'width' doesn't directly control size, used for input validation only
            height (int): The height of the triangle (and of the longest side).
            symbol (str): The character to draw with.

        Returns:
            str: Multi-line ASCII art triangle.

        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(width, height, symbol) # Width is needed for interface consistency
        if width < height:
           raise ValueError("In a right-angled triangle, the height cannot exceed the width for diagonal representation.")

        result = []
        for i in range(1, height + 1):
            result.append(symbol * i)
        return '\n'.join(result)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the specified height using the given symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character used to draw the pyramid.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.

        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(None, height, symbol) # Width not applicable for pyramid.  Pass None.

        result = []
        for i in range(1, height + 1):
            spaces = " " * (height - i)
            symbols = symbol * (2 * i - 1)
            result.append(spaces + symbols)
        return '\n'.join(result)

def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    art = AsciiArt()

    try:
        print("Square:")
        print(art.draw_square(5, "#"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "*"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(4, 6, "@"))

        print("\nTriangle:")
        print(art.draw_triangle(5, 5, "+"))  # Corrected call

        print("\nPyramid:")
        print(art.draw_pyramid(4, "$"))

        # Example of invalid input
        print("\nInvalid Input (Whitespace):")
        print(art.draw_square(5, " "))

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
