class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods to draw squares, rectangles, parallelograms,
    right-angled triangles, and pyramids using a specified symbol.  It adheres
    to principles of OOP and includes input validation to ensure robustness.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width, filled with the given symbol.

        Args:
            width: The width (and height) of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multiline string representing the ASCII art square.

        Raises:
            ValueError: If the width is negative or zero, or if the symbol
                is not a single character or is whitespace.
        """
        self._validate_input(width, symbol)

        square = ""
        for _ in range(width):
            square += symbol * width + "\n"
        return square


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height, filled with the symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A multiline string representing the ASCII art rectangle.

        Raises:
            ValueError: If width/height is negative/zero, or the symbol
                is invalid.
        """
        self._validate_input(width, symbol, height)

        rectangle = ""
        for _ in range(height):
            rectangle += symbol * width + "\n"
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.  The parallelogram grows diagonally to the
		right, with top-left corner as start point. Each row is shifted
		by one space to the right relative to the previous row.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to use.

        Returns:
            A multiline string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width/height is negative/zero, or the symbol is invalid.
        """
        self._validate_input(width, symbol, height)

        parallelogram = ""
        for i in range(height):
            parallelogram += " " * i + symbol * width + "\n"
        return parallelogram


    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle. The triangle grows diagonally
		to the right, starting from the top-left corner.

        Args:
            width: The max width of the triangle (at the bottom).
            height: The height of the triangle.
            symbol: The character to use.

        Returns:
            A multiline string representing the ASCII art triangle.

        Raises:
            ValueError: If width/height is negative/zero, or the symbol is invalid.
            NotImplementedError: If width > height
        """
        self._validate_input(width, symbol, height)

        if (width > height):
            raise NotImplementedError("Current implementation of right angled triangle cannot have width > height")

        triangle = ""
        for i in range(height):
          current_width = int(width * (i + 1) / height) # scale width according to what row of our 'height' sided triangle we're in
          triangle += symbol * current_width + "\n"

        return triangle


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the specified height, filled with symbol.

        Args:
            height: The height of the pyramid.
            symbol: The character to use.

        Returns:
            A multiline string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is negative/zero, or the symbol is invalid.
        """
        self._validate_input(height, symbol)  # Height is used as width here

        pyramid = ""
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            pyramid += spaces + symbols + "\n"
        return pyramid


    def _validate_input(self, width: int, symbol: str, height: int = None) -> None:
        """
        Validates the input parameters.

        Args:
            width: The width of the shape.
            symbol: The character to use for drawing.
            height: The height of the shape (optional, defaults to None).

        Raises:
            ValueError: If input parameters are invalid.
        """
        if not isinstance(width, int) or (height is not None and not isinstance(height, int)):
            raise TypeError("Width and height must be integers.")

        if width <= 0 or (height is not None and height <= 0):
            raise ValueError("Width and height must be positive integers.")

        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")

        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")


# Example usage (and rudimentary testing):
if __name__ == "__main__":
    art = AsciiArt()

    try:
        print("Square:")
        print(art.draw_square(5, "*"))

        print("Rectangle:")
        print(art.draw_rectangle(7, 3, "#"))

        print("Parallelogram:")
        print(art.draw_parallelogram(4, 6, "@"))

        print("Triangle:")
        print(art.draw_triangle(5, 5, "+"))
        print("Triangle (2x2):")
        print(art.draw_triangle(2, 2, "+"))

        print("Pyramid:")
        print(art.draw_pyramid(4, "$"))

        # Example of invalid input:
        print("Invalid Input Test (negative width):")
        print(art.draw_square(-5, "*"))  # Raises ValueError

    except ValueError as e:
        print(f"Caught ValueError: {e}")
    except TypeError as e:
        print(f"Caught TypeError: {e}")
    except NotImplementedError as e:
        print(f"Caught NotImplementedError: {e}")
