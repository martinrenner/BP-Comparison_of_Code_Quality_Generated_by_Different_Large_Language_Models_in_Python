
class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    This class provides methods to draw various shapes filled with a specified symbol,
    adhering to the principles of OOP and ISO/IEC 25010 standards for software quality.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None):
        """
        Validates the input parameters for drawing shapes.

        Args:
            symbol (str): The symbol to use for drawing.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If the symbol is not a single character, is whitespace,
                        or if width/height are negative or zero.
        TypeError: If width/height are not integers.
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
        Draws a square filled with the specified symbol.

        Args:
            width (int): The width (and height) of the square.
            symbol (str): The character to fill the square with.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(symbol, width=width)  # Validate inputs
        return '\n'.join([symbol * width for _ in range(width)])


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to fill the rectangle with.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(symbol, width=width, height=height)
        return '\n'.join([symbol * width for _ in range(height)])


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.  The parallelogram
        is slanted to the right.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to fill the parallelogram with.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(symbol, width=width, height=height)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return '\n'.join(result)


    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.

        Args:
          width (int): The width of the triangle.
          height (int): The height of the triangle
          symbol (str): The character to fill the triangle with

        Returns:
            str: A multi-line string representing the ASCII art triangle.

        Raises:
            ValueError: If input are invalid.
        """

        self._validate_input(symbol, width=width, height=height)

        if width > height:
          raise ValueError("Width cannot exceed height.")

        result = []
        for i in range(1, width + 1):
          result.append(symbol * i)

        return '\n'.join(result)




    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a pyramid filled with the specified symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to fill the pyramid with.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.

        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(symbol, height=height)
        result = []
        for i in range(1, height + 1):
            result.append(" " * (height - i) + symbol * (2 * i - 1))
        return '\n'.join(result)


# Example Usage
art = AsciiArt()

try:
    print(art.draw_square(5, "*"))
    print(art.draw_rectangle(7, 3, "#"))
    print(art.draw_parallelogram(4, 6, "+"))
    print(art.draw_triangle(5, 5, "X"))
    print(art.draw_pyramid(4, "@"))

    # Test cases with invalid input
    # print(art.draw_square(-5, "*"))  # Raises ValueError: Width and height must be positive integers.
    # print(art.draw_rectangle(4, 2, "@@"))  # Raises ValueError: Symbol must be a single character.
    # print(art.draw_parallelogram(6, 3, " ")) # Raises ValueError: Symbol cannot be whitespace.
     print(art.draw_triangle(6, 3, "T")) # Raises ValueError: Width cannot exceed height.
    # print(art.draw_pyramid(5, 5.5)) # Raises TypeError: Height must be an integer.
except ValueError as e:
    print(f"ValueError: {e}")
except TypeError as e:
    print(f"TypeError: {e}")

