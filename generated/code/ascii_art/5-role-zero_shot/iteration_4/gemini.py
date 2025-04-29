class AsciiArt:
    """
    A class for generating ASCII art shapes.

    This class provides methods to draw various shapes like squares, rectangles,
    parallelograms, right-angled triangles, and pyramids using a specified symbol.
    It focuses on efficiency, input validation, and producing clean, readable output.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None):
        """
        Validates the input parameters for the drawing functions.

        Args:
            symbol (str): The symbol to use for drawing the shape.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If the symbol is invalid (not a single character or whitespace)
                        or if width/height are negative or zero.
        """
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
        if width is not None and width <= 0:
            raise ValueError("Width must be a positive integer.")
        if height is not None and height <= 0:
            raise ValueError("Height must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width using the given symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the square.
        """
        self._validate_input(symbol, width=width)
        return self.draw_rectangle(width, width, symbol)


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height using the given symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.
        """
        self._validate_input(symbol, width=width, height=height)
        return '\n'.join([symbol * width] * height)


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified dimensions and symbol.  The parallelogram
        slants to the right.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use.

        Returns:
            str: A multi-line string representing the parallelogram.
        """
        self._validate_input(symbol, width=width, height=height)
        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)
        return "\n".join(lines)


    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with the specified dimensions and symbol, growing diagonally to the right from the top-left.

        Args:
            width: The maximum width of the triangle at the base, could be less if limited by height.
            height: The height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            str: A multi-line string representing the triangle.
        """
        self._validate_input(symbol, width=width, height=height)
        lines = []
        actual_width = min(width, height)  # Triangle can't be wider than height
        for i in range(actual_width):
             lines.append(symbol * (i + 1))
        return '\n'.join(lines)
        

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the specified height and symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use.

        Returns:
            str: A multi-line string representing the pyramid.
        """
        self._validate_input(symbol, height=height)
        lines = []
        for i in range(height):
            padding = " " * (height - 1 - i)
            symbols = symbol * (2 * i + 1)
            lines.append(padding + symbols)
        return "\n".join(lines)



def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    art = AsciiArt()

    # Example Usage with Error Handling
    try:
        print("Square:")
        print(art.draw_square(5, "*"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "#"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(6, 4, "@"))

        print("\nTriangle:")
        print(art.draw_triangle(5, 7, "+"))  # Height will limit the effective width

        print("\nPyramid:")
        print(art.draw_pyramid(5, "$"))

        # Example of invalid input (uncomment to test)
        #print("\nInvalid Input Test:")
        #print(art.draw_square(4, "  "))  # Should raise ValueError


    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

