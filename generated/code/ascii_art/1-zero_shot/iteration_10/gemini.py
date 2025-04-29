class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods to draw squares, rectangles, parallelograms,
    right-angled triangles, and pyramids using a specified symbol.  It adheres
    to principles of OOP, includes input validation, and focuses on code quality.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width, filled with the given symbol.

        Args:
            width: The width of the square (must be a positive integer).
            symbol: The character to use for drawing the square (must be a single, 
                    printable character).

        Returns:
            A multiline string representing the ASCII art square.

        Raises:
            ValueError: If width is not a positive integer or if the symbol is
                        invalid (not a single character or whitespace).
        """
        self._validate_input(width, symbol)  # Call the shared validation method

        square = ""
        for _ in range(width):
            square += symbol * width + "\n"
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height, filled with the symbol.

        Args:
            width: The width of the rectangle (positive integer).
            height: The height of the rectangle (positive integer).
            symbol: The drawing symbol (single, printable character).

        Returns:
            A multiline string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height are invalid, or if the symbol is invalid.
        """
        self._validate_input(width, symbol, height)

        rectangle = ""
        for _ in range(height):
            rectangle += symbol * width + "\n"
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.

        Args:
            width: The width of the parallelogram (positive integer).
            height: The height of the parallelogram (positive integer).
            symbol: The drawing symbol (single, printable character).

        Returns:
            A multiline string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height are invalid, or if the symbol is invalid.
        """
        self._validate_input(width, symbol, height)

        parallelogram = ""
        for i in range(height):
            parallelogram += " " * i + symbol * width + "\n"
        return parallelogram

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width: The width of the triangle at its base (positive integer).
            height: The height of the triangle (positive integer).
            symbol:  The drawing symbol (single, printable character).

        Returns:
            A multiline string representing the ASCII art triangle.

        Raises:
             ValueError: If width or height are invalid, or if the symbol is
                         invalid, or if width is greater than height.
        """
        self._validate_input(width, symbol, height)
        if width > height:
            raise ValueError("For a right-angled triangle, width cannot be greater than height.")


        triangle = ""
        for i in range(height):
                triangle += symbol * min(i + 1, width) + "\n" # i + 1 because range starts at 0

        return triangle


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height: The height of the pyramid (positive integer).
            symbol: The drawing symbol (single, printable character).

        Returns:
            A multiline string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is invalid, or if the symbol is invalid.
        """
        self._validate_input(height, symbol)  # width is not used, height is validated

        pyramid = ""
        for i in range(height):
            spaces = " " * (height - 1 - i)
            symbols = symbol * (2 * i + 1)
            pyramid += spaces + symbols + spaces + "\n"
        return pyramid
    
    def _validate_input(self, *args):
        """
        Validates the input for drawing functions.

        Args:
            *args:  A variable number of arguments.  Expected to be either:
                    (width, symbol) or (width, symbol, height).

        Raises:
            ValueError:  If any of the dimensions are negative or the symbol is
                        invalid (not a single character, or is whitespace).
        """

        if len(args) < 2 or len(args) > 3:
            raise ValueError("Invalid number of arguments for input validation.")

        dimensions = [arg for arg in args[:-1]]  # All except the last (symbol)
        symbol = args[-1]  # The last argument is presumed to be the symbol

        for dim in dimensions:
            if not isinstance(dim, int) or dim <= 0:
                raise ValueError("Dimensions (width/height) must be positive integers.")

        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single, non-whitespace character.")



def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    art = AsciiArt()

    # Example usage with error handling
    try:
        print("Square:")
        print(art.draw_square(5, "*"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "#"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(6, 4, "@"))

        print("\nTriangle:")
        print(art.draw_triangle(4, 4, "+"))
        
        print("\nTriangle (width < height):")
        print(art.draw_triangle(2, 4, "+"))

        print("\nPyramid:")
        print(art.draw_pyramid(5, "$"))

        # Demonstrating error handling
        print("\nInvalid Input Examples (will raise ValueErrors):")
        #print(art.draw_square(-5, "*"))       # Negative width
        #print(art.draw_rectangle(4, 0, "&"))  # Zero height
        #print(art.draw_pyramid(6, "  "))     # Whitespace symbol
        print(art.draw_triangle(height=6, width=7, symbol = "o")) # triangle with width > height

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
