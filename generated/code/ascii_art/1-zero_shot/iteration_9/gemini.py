class AsciiArt:
    """
    A class for generating ASCII art shapes.

    This class provides methods to draw various geometric shapes using ASCII
    characters, adhering to ISO/IEC 25010 standards for quality.
    """

    def _validate_input(self, symbol: str, dimensions: tuple[int, ...]):
        """
        Validates the input parameters for drawing functions.

        Args:
            symbol (str): The character used to draw the shape.
            dimensions (tuple[int, ...]):  A tuple containing dimensions (width, height, etc.).

        Raises:
            ValueError: If the symbol is invalid (not a single printable
              character, whitespace),  or if any dimension is negative or zero.
            TypeError: If the dimensions are not integers.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if not all(isinstance(dim, int) for dim in dimensions):
            raise TypeError("Dimensions must be integers.")

        if any(dim <= 0 for dim in dimensions):
            raise ValueError("Dimensions must be positive integers.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of the given width using the specified symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to fill the square with.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If width is not positive, or the symbol is invalid.
            TypeError: If width is not integer.
        """
        self._validate_input(symbol, (width,))
        return '\n'.join([symbol * width] * width)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle with the specified dimensions and symbol.

        Args:
            width (int):  The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to fill the rectangle with.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If width or height is not positive, or the symbol is invalid.
             TypeError: If width or height is not integer.
        """
        self._validate_input(symbol, (width, height))
        return '\n'.join([symbol * width] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram.  The parallelogram slants to the right.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If width or height is not positive, or the symbol is invalid.
            TypeError: If width or height is not integer.
        """
        self._validate_input(symbol, (width, height))
        result = []
        for i in range(height):
            result.append(' ' * i + symbol * width)
        return '\n'.join(result)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width (int): The width of the triangle's base.
            height(int): The height of the triangle, must be <= width.
            symbol (str): The character to use.

        Returns:
            str: The ASCII art representation of the triangle.

        Raises:
            ValueError: If width or height is negative, or the symbol is invalid, or height > width.
            TypeError: If width or height is not integer.
        """
        self._validate_input(symbol, (width, height))
        if height > width:
            raise ValueError("Height of the triangle cannot be greater than its width.")

        result = []
        for i in range(height):
            result.append(symbol * (i + 1))
        return '\n'.join(result)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled pyramid with the specified height and symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to fill the pyramid with.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If height is not positive, or symbol is invalid.
            TypeError: If height is not integer.
        """
        self._validate_input(symbol, (height,))
        result = []
        for i in range(height):
            spaces = ' ' * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            result.append(spaces + symbols)
        return '\n'.join(result)



def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    art = AsciiArt()

    # Get user input for symbol
    while True:
        try:
            symbol = input("Enter the symbol you want to use for drawing: ")
            # Perform basic validation here to give immediate feedback
            art._validate_input(symbol, (1,))  # Use a dummy dimension for symbol-only check
            break
        except ValueError as e:
            print(f"Invalid symbol: {e}")

    # Draw shapes
    try:
        print("\nSquare:")
        print(art.draw_square(5, symbol))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, symbol))

        print("\nParallelogram:")
        print(art.draw_parallelogram(6, 4, symbol))

        print("\nTriangle:")
        print(art.draw_triangle(5, 5, symbol))

        print("\nPyramid:")
        print(art.draw_pyramid(5, symbol))

    except (ValueError, TypeError) as e:
        print(f"Error drawing shapes: {e}")

    # Example of invalid input
    try:
        print(art.draw_square(-5, symbol))
    except ValueError as e:
        print(f"\nExpected error (negative width): {e}")

    try:
        print(art.draw_triangle(5, 8, symbol))
    except ValueError as e:
        print(f"\nExpected error(height is greater than width): {e}")

if __name__ == "__main__":
    main()
