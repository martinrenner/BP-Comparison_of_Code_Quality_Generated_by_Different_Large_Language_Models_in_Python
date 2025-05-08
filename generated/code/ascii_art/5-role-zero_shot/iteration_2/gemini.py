class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None):
        """
        Validates the input parameters for drawing shapes.

        Args:
            symbol (str): The symbol to use for drawing the shape.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If the symbol is invalid (not a single printable character, or whitespace),
                        or if width/height are negative or zero.
        """
        if not symbol or len(symbol) != 1 or not symbol.isprintable() or symbol.isspace():
            raise ValueError("Symbol must be a single printable character and not whitespace.")

        if width is not None and width <= 0:
            raise ValueError("Width must be a positive integer.")

        if height is not None and height <= 0:
            raise ValueError("Height must be a positive integer.")


    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width using the specified symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The symbol to use for drawing the square.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If input parameters are invalid.
        """
        self._validate_input(symbol, width=width)
        return '\n'.join([symbol * width for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height using the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing the rectangle.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If input parameters are invalid.
        """
        self._validate_input(symbol, width=width, height=height)
        return '\n'.join([symbol * width for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram of the given width and height using the specified symbol.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing the parallelogram.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If input parameters are invalid.
        """
        self._validate_input(symbol, width=width, height=height)
        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)
        return '\n'.join(lines)
        

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with given dimensions using the specified symbol.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: The ASCII art representation of the triangle.

        Raises:
            ValueError: If input parameters are invalid.
        """
        self._validate_input(symbol, width=width, height=height)
            
        if width > height:
            raise ValueError("For a right-angled triangle, height must to be not less than width.")
        
        lines = []
        for i in range(height):
          lines.append(symbol * min(width, i+1))  # Limit the line length up to 'width'
        return '\n'.join(lines)
            

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a pyramid of the given height using the specified symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing the pyramid.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.

        Raises:
            ValueError: If input parameters are invalid.
        """
        self._validate_input(symbol, height=height)
        lines = []
        for i in range(height):
            num_symbols = 2 * i + 1
            line = ' ' * (height - i - 1) + symbol * num_symbols
            lines.append(line)
        return '\n'.join(lines)



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
        print(art.draw_triangle(4, 4, "+"))
        
        print("\nPyramid:")
        print(art.draw_pyramid(5, "$"))

        # Example of invalid input
        #print("\nInvalid Square (multichar symbol):")
        #print(art.draw_square(4, "**"))  # This will raise a ValueError

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

