class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods to draw squares, rectangles, parallelograms,
    right-angled triangles, and pyramids using a specified symbol.  It adheres
    to principles of OOP and includes input validation to ensure robustness and
    security.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width, filled with the given symbol.

        Args:
            width: The width (and height) of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is negative, symbol is empty or not a single, printable, and non-whitespace character.
        """
        self._validate_input(width, symbol)  # Unified input validation

        square = ""
        for _ in range(width):
            square += symbol * width + "\n"
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height, filled with the given symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A multi-line string representing the ASCII art rectangle.

        Raises:
             ValueError: If width/height is negative, symbol is empty or not a single, printable, and non-whitespace character.
        """
        self._validate_input(width, symbol, height)

        rectangle = ""
        for _ in range(height):
            rectangle += symbol * width + "\n"
        return rectangle
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.  The parallelogram 'grows' diagonally to the
        right, starting from the top-left corner. Each row is shifted by one space.

        Args:
            width: The width of the parallelogram's base.
            height: The height of the parallelogram.
            symbol: The character to use.

        Returns:
            A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width/height is negative, symbol is empty or not a single, printable, and non-whitespace character.
        """
        self._validate_input(width, symbol, height)

        parallelogram = ""
        for i in range(height):
            parallelogram += " " * i + symbol * width + "\n"
        return parallelogram

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.  The triangle grows diagonally to the
        right, starting from the top-left corner.

        Args:
            width:  The width of the triangle's base. MUST be equal to height (right-angled).
            height: The height of the triangle. MUST be equal to width (right-angled).
            symbol: The character to use.

        Returns:
            A multi-line string representing the ASCII art triangle.

        Raises:
            ValueError:  If width != height, width/height is negative, symbol is empty or not a single, printable, and non-whitespace character.
        """
        self._validate_input(width, symbol, height)
        if width != height:
            raise ValueError("Width and height must be equal for a right-angled triangle.")
        
        triangle = ""
        for i in range(height):
            triangle += symbol * (i + 1) + "\n"
        return triangle


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The character to use.

        Returns:
            A multi-line string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is negative, symbol is empty or not a single, printable, and non-whitespace character.
        """
        self._validate_input(height, symbol)  # height acts as dimension

        pyramid = ""
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            pyramid += spaces + symbols + "\n"
        return pyramid
    

    def _validate_input(self, *args):
        """
        Private helper function for input validation. Centralized validation logic.

        Args:
            *args:  Variable number of arguments.  The last argument MUST be the
                    symbol.  All arguments before the symbol are treated as
                    integer dimensions (width, height).
        Raises:
            ValueError: If dimensions are negative,  symbol is empty, not a single character, or whitespace.
        """
        symbol = args[-1]
        dimensions = args[:-1]

        for dim in dimensions:
            if not isinstance(dim, int):
                raise TypeError("Dimensions must be integers.") #Added type checking
            if dim <= 0:
                raise ValueError("Dimensions must be positive integers.")

        if not isinstance(symbol, str): #Added type checking
            raise TypeError("Symbol must be a string.")
        if not symbol:
            raise ValueError("Symbol cannot be empty.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")


def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    art = AsciiArt()

    try:
        # Square
        print("Square:")
        print(art.draw_square(5, "*"))

        # Rectangle
        print("Rectangle:")
        print(art.draw_rectangle(7, 3, "#"))

        # Parallelogram
        print("Parallelogram:")
        print(art.draw_parallelogram(4, 6, "@"))

        # Triangle
        print("Triangle:")
        print(art.draw_triangle(4, 4, "+"))

        # Pyramid
        print("Pyramid:")
        print(art.draw_pyramid(5, "$"))

        # Example of invalid input (negative width)
        print("Invalid Input (Negative Width):")
        print(art.draw_square(-5, "*"))

    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
         print(f"Error: {e}")

if __name__ == "__main__":
    main()
