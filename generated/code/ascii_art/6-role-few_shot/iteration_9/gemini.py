class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods to draw squares, rectangles, parallelograms,
    right-angled triangles, and pyramids using a specified symbol.  It includes
    input validation to ensure correct usage and prevent common errors.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width using the specified symbol.

        Args:
            width (int): The width (and height) of the square.
            symbol (str): The character to use for drawing the square.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is not positive, or symbol is invalid.
        """
        self._validate_input(width, symbol)  # input validation
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height using the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing the rectangle.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is not positive, or symbol is invalid.
        """
        self._validate_input(width, symbol)  # input validation
        self._validate_input(height, symbol)  # input validation
        
        lines = []
        for _ in range(height):
            lines.append(symbol * width)
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified dimensions and symbol.

        The parallelogram grows diagonally to the right, starting from the
        top-left corner. Each row is shifted by one space.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height is not positive, or symbol is invalid.
        """
        self._validate_input(width, symbol) # input validation
        self._validate_input(height, symbol)  # input validation

        lines = []
        for i in range(height):
            lines.append(" " * i + symbol * width)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.  It grows diagonally to the right,
        starting from the top-left corner, forming a sharp point at the top.

        Args:
            width (int): The width of the triangle.
            height (int): The height of the triangle
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art triangle.

        Raises:
            ValueError: If width or height is not positive, or symbol is invalid.
        """
        
        self._validate_input(width, symbol)
        self._validate_input(height, symbol)

        # Ensure that the triangle doesn't have "cut" sides by adjusting width to height
        
        lines = []
        if width > height:
           for i in range(1, height+1):
               lines.append(symbol * i)
        else:
             for i in range(1,width+1):
                lines.append(symbol * i)   
        return "\n".join(lines)
           

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the specified height using the specified symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing the pyramid.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is not positive, or symbol is invalid.
        """
        self._validate_input(height, symbol)  # input validation

        lines = []
        for i in range(1, height + 1):
            padding = " " * (height - i)
            line = padding + symbol * (2 * i - 1) + padding
            lines.append(line)
        return "\n".join(lines)

    def _validate_input(self, dimension: int, symbol: str):
        """
        Validates input parameters for shape drawing methods.

        Args:
            dimension (int):  The dimension (width or height) of the shape.
            symbol (str): The character to use.

        Raises:
            ValueError:  If the dimension is not positive, or the symbol is
              not a single printable character, or if the symbol is whitespace.
        """
        
        if not isinstance(dimension, int) or dimension <= 0:
            raise ValueError("Dimension must be a positive integer.")

        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")

        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
        


# Example Usage (and basic tests)
if __name__ == "__main__":
    art = AsciiArt()

    try:
        print("Square:")
        print(art.draw_square(5, "*"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "#"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(6, 4, "@"))

        print("\nTriangle:")
        print(art.draw_triangle(5, 5, "+"))
        
        print("\nTriangle (width > height):")
        print(art.draw_triangle(7, 4, "+"))

        print("\nPyramid:")
        print(art.draw_pyramid(5, "%"))

        # Example of invalid inputs that are to be handled correctly:
        # print("\nInvalid Square (negative width):")
        # print(art.draw_square(-5, "*"))  # Raises ValueError

        # print("\nInvalid Rectangle (zero height):")
        # print(art.draw_rectangle(5, 0, "#")) # Raises ValueError

        # print("\nInvalid symbol (multiple characters):")
        # art.draw_square(3, "**")  # Raises ValueError

         # print("\nInvalid symbol (whitespace):")
         # art.draw_square(3, " ")  # Raises ValueError

    except ValueError as e:
        print(f"Error: {e}")
