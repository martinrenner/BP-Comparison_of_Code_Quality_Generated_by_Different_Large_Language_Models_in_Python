class AsciiArt:
    """
    A class for generating ASCII art shapes.

    This class provides methods to draw various shapes like squares, rectangles,
    parallelograms, triangles, and pyramids using a specified symbol.
    It focuses on clean code, efficiency, and input validation.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width, filled with the given symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to fill the square with.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If width is negative, or symbol is invalid.
        """
        self._validate_input(width, symbol)
        return self._draw_rectangle(width, width, symbol)


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height, filled with the given symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to fill the rectangle with.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
             ValueError: If width or height is negative, or symbol is invalid.
        """
        self._validate_input(width, symbol)
        self._validate_input(height, symbol)
        return self._draw_rectangle(width, height, symbol)


    def _draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Helper function that generates ASCII art for rectangle (and square, as a special case).

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character used to draw the rectangle.

        Returns:
            str: The ASCII art representation of the rectangle.
        """
        lines = []
        for _ in range(height):
            lines.append(symbol * width)
        return "\n".join(lines)


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified width and height, using the provided symbol.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to fill the parallelogram with.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If width or height is negative, or symbol is invalid.
        """
        self._validate_input(width, symbol)
        self._validate_input(height, symbol)
        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle, filled with the specified symbol.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The character to fill the triangle with.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            ValueError: If width or height is negative, or symbol is invalid.
        """
        self._validate_input(width, symbol)
        self._validate_input(height, symbol)

        lines = []
        # Check and adjust based on which side is shorter.
        if width >= height:
            scale = width /height
            for i in range(height):
              lines.append(symbol * int(scale * (i+1)))
        else:
            scale = height/width
            for i in range(height):
                line_width = (i + scale) // scale # calculate amount of symbols in current row
                if line_width > width:
                    break
                lines.append(symbol * int(line_width))
        return "\n".join(lines)


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the specified height, using the given symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to fill the pyramid with.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If height is negative or symbol is invalid.
        """
        self._validate_input(height, symbol)
        lines = []
        for i in range(height):
            lines.append(" " * (height - i - 1) + symbol * (2 * i + 1))
        return "\n".join(lines)

    def _validate_input(self, dimension: int, symbol: str):
        """
        Validates the input dimensions and symbol.

        Args:
            dimension (int): The dimension (width or height) to validate.
            symbol (str): The symbol to validate.

        Raises:
            ValueError: If dimension is negative, symbol is empty,
                        contains whitespace, or is more than one character.
        """
        if dimension < 0:
            raise ValueError("Dimensions must be non-negative.")
        if not symbol:
            raise ValueError("Symbol cannot be empty.")
        if len(symbol) > 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")



def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    art = AsciiArt()

    try:
        print("Square:")
        print(art.draw_square(5, "*"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "#"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(6, 4, "@"))

        print("\nTriangle:")
        print(art.draw_triangle(5, 8, "+"))

        print("\nPyramid:")
        print(art.draw_pyramid(5, "$"))

        # Example with invalid input, demonstrating exception handling:
        print("\nInvalid Input Test:")
        print(art.draw_square(-5, "*"))  # Raises ValueError

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

