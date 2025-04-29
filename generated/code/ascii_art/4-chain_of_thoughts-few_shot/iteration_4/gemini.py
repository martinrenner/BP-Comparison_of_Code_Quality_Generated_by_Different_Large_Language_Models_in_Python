class AsciiArt:
    """
    A class for generating various ASCII art shapes.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width filled with the given symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to use for drawing the square.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is negative or symbol is invalid.
        """
        self._validate_input(width, symbol)

        if width == 0:  # Handle edge case of zero width
            return ""

        square = ""
        for _ in range(width):
            square += symbol * width + "\n"
        return square.rstrip()  # Remove the trailing newline

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height filled with the given symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing the rectangle.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is negative, or symbol is invalid.
        """
        self._validate_input(width, symbol, height)

        if width == 0 or height == 0:  # Handle edge cases of zero dimensions
            return ""

        rectangle = ""
        for _ in range(height):
            rectangle += symbol * width + "\n"
        return rectangle.rstrip()

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use.

        Returns:
            str: ASCII art of the parallelogram.

        Raises:
            ValueError: If invalid input.
        """
        self._validate_input(width, symbol, height)

        if width == 0 or height == 0:
            return ""

        parallelogram = ""
        for i in range(height):
            parallelogram += " " * i + symbol * width + "\n"
        return parallelogram.rstrip()

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width (int): The base width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The character to use.

        Returns:
             str: ASCII art of the triangle.

        Raises:
            ValueError: If invalid input.
        """
        self._validate_input(width, symbol, height)

        if width == 0 or height == 0:
            return ""

        if width < height:  # Ensure that the triangle grows diagonally
            raise ValueError("Width must be greater or equal than height for the right-angled triangle.")
        triangle = ""

        for i in range(1, height + 1):
          triangle += symbol * i + "\n"

        return triangle.rstrip()

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use.

        Returns:
            str: ASCII art of the pyramid.

        Raises:
            ValueError: If invalid input.
        """
        self._validate_input(height, symbol) # width is not used, but must at least validate height

        if height == 0:
            return ""

        pyramid = ""
        for i in range(1, height + 1):
            spaces = " " * (height - i)
            symbols = symbol * (2 * i - 1)
            pyramid += spaces + symbols + spaces + "\n"  # Added spaces for symmetry
        return pyramid.rstrip()

    def _validate_input(self, *args):
        """
        Validates the input parameters.

        Args:
            *args:  Variable length argument list.  Expected: width, symbol, [height]

        Raises:
            ValueError: If input is invalid.
        """
        if len(args) < 2:
            raise ValueError("At least width/height and symbol must be provided.")

        dimension_args = [arg for arg in args[:-1] if isinstance(arg, int)]
        symbol = args[-1]

        if not all(dim >= 0 for dim in dimension_args):
            raise ValueError("Dimensions (width, height) cannot be negative.")

        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")

        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")


# Example Usage and Driver Code
if __name__ == "__main__":
    art = AsciiArt()

    try:
        print("Square:\n", art.draw_square(5, "#"))
        print("\nRectangle:\n", art.draw_rectangle(7, 3, "*"))
        print("\nParallelogram:\n", art.draw_parallelogram(6, 4, "+"))
        print("\nTriangle:\n", art.draw_triangle(5,5, "X"))  # Corrected example
        print("\nPyramid:\n", art.draw_pyramid(4, "@"))

        # Example of invalid input
        # print("\nInvalid Square:\n", art.draw_square(-5, "#"))  # Raises ValueError
        # print("\nInvalid Symbol:\n", art.draw_square(5, "##"))  # Raises ValueError
        print("\nZero width square:\n", art.draw_square(0, '$'))
        print("\nTriangle (h>w):\n", art.draw_triangle(4, 5, "T"))

    except ValueError as e:
        print(f"Error: {e}")
