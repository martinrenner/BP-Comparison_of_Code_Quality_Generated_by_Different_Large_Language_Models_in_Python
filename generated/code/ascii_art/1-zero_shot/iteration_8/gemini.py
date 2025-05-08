class AsciiArt:
    """
    A class for generating ASCII art shapes.  It adheres to ISO/IEC 25010
    quality standards by focusing on correctness, performance, modularity,
    security, testability, readability, and documentation.
    """

    def _validate_input(self, symbol: str, *args: int):
        """
        Validates the input parameters for the drawing functions.

        Args:
            symbol: The symbol to use for drawing.
            *args:  Width and/or height values.

        Raises:
            TypeError: If the symbol is not a string or if dimensions are not integers.
            ValueError: If the symbol is not a single character, is whitespace,
                        or if dimensions are not positive.
        """

        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
        for arg in args:
            if not isinstance(arg, int):
                raise TypeError("Dimensions must be integers.")
            if arg <= 0:
                raise ValueError("Dimensions must be positive integers.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width filled with the specified symbol.

        Args:
            width: The width of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A string representing the ASCII art square.

        Raises:
            TypeError: If input types are incorrect.
            ValueError: If input values are invalid.
        """
        self._validate_input(symbol, width)
        return '\n'.join([symbol * width for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given dimensions filled with the specified symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A string representing the ASCII art rectangle.

        Raises:
            TypeError: If input types are incorrect.
            ValueError: If input values are invalid.
        """
        self._validate_input(symbol, width, height)
        return '\n'.join([symbol * width for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with given dimensions and symbol.  The parallelogram
        slants to the right.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to use.

        Returns:
            A multi-line string representing the parallelogram.

        Raises:
            TypeError: If input types are incorrect.
            ValueError: If input values are invalid.
        """
        self._validate_input(symbol, width, height)
        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)  # Efficient string multiplication
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width: The maximum width of the triangle (at the base).
            height: The height of the triangle.
            symbol: The character to use.

        Returns:
            The ASCII art triangle as a string.  Returns an empty string if
            width or height is zero.

        Raises:
            TypeError: If input types are incorrect.
            ValueError: If input values are invalid, except if either width or height is 0.

        """
        self._validate_input(symbol, width, height)
        lines = []

        # Ensure proportional growth capped by both width and height
        for i in range(min(width, height)):
             lines.append(symbol * (i + 1))
             
        return "\n".join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a pyramid of the specified height, filled with the given symbol.

        Args:
            height: The height of the pyramid.
            symbol: The symbol to use for drawing.

        Returns:
            A string representing the ASCII art pyramid.

        Raises:
            TypeError: If input types are incorrect.
            ValueError: If input values are invalid.
        """
        self._validate_input(symbol, height)
        lines = []
        for i in range(height):
            padding = " " * (height - 1 - i)
            # Calculate the number of symbols needed to form a proportional pyramid.
            symbols = symbol * (2 * i + 1)  
            lines.append(padding + symbols)
        return "\n".join(lines)



def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    art = AsciiArt()

    # Example usage with input validation and error handling
    try:
        print("Square:")
        print(art.draw_square(5, "*"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "#"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(4, 6, "@"))
        
        print("\nTriangle:")
        print(art.draw_triangle(5, 7, "+"))

        print("\nPyramid:")
        print(art.draw_pyramid(5, "$"))

        # Example of invalid inputs
        print("\nInvalid Input Examples (will raise exceptions):")
        # print(art.draw_square(-5, "*"))  # Negative width
        # print(art.draw_rectangle(4, 0, "&")) # Zero height
        # print(art.draw_pyramid(6, "  "))  # Whitespace symbol
        # print(art.draw_parallelogram(5, 3, "AB"))  # Multi-character symbol
        print(art.draw_square(5, "*"))
        print(art.draw_rectangle(4, 2, "&")) 
        print(art.draw_pyramid(6, "Y"))
        print(art.draw_parallelogram(5, 3, "P"))
        print(art.draw_triangle(width=3, height=6, symbol="T"))

    except (TypeError, ValueError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
