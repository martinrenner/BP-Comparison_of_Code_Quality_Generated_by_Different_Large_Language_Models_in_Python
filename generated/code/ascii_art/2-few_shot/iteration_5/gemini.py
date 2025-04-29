class AsciiArt:
    """
    A class for generating ASCII art shapes.

    This class provides methods to draw various shapes like squares, rectangles,
    parallelograms, triangles, and pyramids using a specified symbol.
    It adheres to OOP principles and includes input validation to ensure
    robustness and security.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width filled with the specified symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to fill the square with.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is negative, symbol is not a single character,
                        or symbol is whitespace.
        """
        self._validate_input(width, symbol)  # Reuse validation

        return '\n'.join([symbol * width for _ in range(width)])


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle with given width and height, filled with the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to fill the rectangle with.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is negative, symbol is not a single
                        character, or symbol is whitespace.
        """
        self._validate_input(width, symbol)   # Reuse validation
        if height < 0:
            raise ValueError("Height cannot be negative.")

        return '\n'.join([symbol * width for _ in range(height)])


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with given width and height.

        The parallelogram grows diagonally to the right, starting from the
        top-left corner. Each row is shifted by one space.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height is negative, the symbol is not a
                        single character, or the symbol is whitespace.
        """
        self._validate_input(width, symbol)
        if height < 0:
            raise ValueError("Height cannot be negative.")

        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)
        return '\n'.join(lines)


    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The symbol to use.

        Returns:
            str: The ASCII art triangle.

        Raises:
            ValueError: If width or height is negative, symbol is invalid.
        """
        self._validate_input(width, symbol)
        if height < 0:
            raise ValueError("Height cannot be negative.")

        if width < height :
           raise ValueError("For right-angled triangle width must be equal or greater to height.")
        
        lines = []
        for i in range(height):
            lines.append(symbol * (i + 1))
        return '\n'.join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the given height filled with symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to fill the pyramid with.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.

        Raises:
             ValueError: If height is negative, symbol is not a single character,
                        or symbol is whitespace.
        """

        if height < 0: # No need to validate a symbol, because we use it only once
            raise ValueError("Height cannot be negative.")
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")

        lines = []
        for i in range(height):
            padding = " " * (height - i - 1)
            row = symbol * (2 * i + 1)
            lines.append(padding + row)
        return '\n'.join(lines)
    

    def _validate_input(self, width: int, symbol: str) -> None:
        """
        Validates the input parameters for shape drawing methods.  This is an
        internal helper method (indicated by the leading underscore).

        Args:
            width (int): The width of the shape.
            symbol (str): The character to fill the shape with.

        Raises:
            ValueError: If width is negative, symbol is not a single character,
                        or symbol is whitespace.
        """
        if width < 0:
            raise ValueError("Width cannot be negative.")
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")


def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    art = AsciiArt()

    # Get user input with error handling
    while True:
        try:
            symbol = input("Enter the symbol you want to use: ")
            if len(symbol) != 1 or symbol.isspace():
                print("Invalid symbol. Please enter a single, non-whitespace character.")
                continue

            width = int(input("Enter the width of the shapes: "))
            height = int(input("Enter the height of the shapes (for rectangle, parallelogram, and triangle): "))
            pyramid_height = int(input("Enter the height of the pyramid: "))
            
            if width < 0 or height < 0 or pyramid_height <0:
                print("Width and height must be non-negative integers.")
                continue
            
            break # Exit loop if input is valid
        except ValueError:
            print("Invalid input. Please enter numeric values for width and height.")

    # Examples using valid inputs and demonstrating each function
    try:
        print("\nSquare:")
        print(art.draw_square(width, symbol))

        print("\nRectangle:")
        print(art.draw_rectangle(width, height, symbol))

        print("\nParallelogram:")
        print(art.draw_parallelogram(width, height, symbol))

        print("\nTriangle:")
        print(art.draw_triangle(width, height, symbol))

        print("\nPyramid:")
        print(art.draw_pyramid(pyramid_height, symbol))

    except ValueError as e:
        print(f"Error: {e}")  # Catch any validation errors that might occur

if __name__ == "__main__":
    main()
