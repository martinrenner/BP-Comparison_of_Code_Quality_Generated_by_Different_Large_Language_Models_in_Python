class AsciiArt:
    """
    A class for generating various ASCII art shapes.

    This class provides methods to draw squares, rectangles, parallelograms,
    right-angled triangles, and pyramids using a specified symbol.  It adheres
    to principles of OOP and includes input validation for robustness.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width filled with the given symbol.

        Args:
            width: The width of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is negative, or symbol is not a single
                        printable character or symbol is a whitespace.
        """
        self._validate_input(width, symbol)  # Call the shared validation
        if width ==0:
            return ""

        square = ""
        for _ in range(width):
            square += symbol * width + "\n"
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height with the given symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is negative, or symbol is not a
                        single printable character or symbol is a whitespace.
        """
        self._validate_input(width, symbol) #Call the size and symbol validation
        self._validate_size(height)   # Validate height separately

        if width == 0 or height == 0:
            return ""

        rectangle = ""
        for _ in range(height):
            rectangle += symbol * width + "\n"
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.  The parallelogram's top-left corner starts
        at the origin, and each subsequent row is shifted one space to the right.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to use.

        Returns:
            A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height is negative, or symbol is not a
                        single printable character, or symbol is a whitespace.
        """
        self._validate_input(width, symbol)  # Size and symbol validation
        self._validate_size(height)     # Validate height

        if width == 0 or height == 0:
            return ""

        parallelogram = ""
        for i in range(height):
            parallelogram += " " * i + symbol * width + "\n"
        return parallelogram

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width:  The width of the triangle's base.
            height: The height of the triangle.
            symbol:  The character to use.

        Returns:
            A multi-line string of the ASCII art triangle.

        Raises:
            ValueError: If width or height is negative, or symbol is not a
                        single printable character, or symbol is a whitespace.

        """
        self._validate_input(width, symbol) # Size and symbol validation
        self._validate_size(height)     # Validate height

        if width == 0 or height == 0:
            return ""

        if width < height:
          raise ValueError("For the triangle width must me larger than height.")

        triangle = ""
        for i in range(height):
          triangle += symbol * (i + 1) + "\n"
        return triangle

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height: The height of the pyramid (number of rows).
            symbol: The character to use.

        Returns:
            A multi-line string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is negative, symbol is not a single
                        printable character, or symbol is a whitespace.
        """
        # Validate height and symbol together
        self._validate_input(height, symbol)

        if height == 0:
            return ""

        pyramid = ""
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            pyramid += spaces + symbols + "\n"
        return pyramid
    

    def _validate_input(self, size: int, symbol: str) -> None:
      """
        Helper method for shared input validation.  Checks size and symbol.
      """
      self._validate_size(size)
      self._validate_symbol(symbol)  # Validate symbol separately

    def _validate_size(self, size: int) -> None:
        """
        Validates the size (width or height) of a shape.

        Args:
            size: The size to validate.

        Raises:
            ValueError: If size is negative.
        """
        if size < 0:
            raise ValueError("Size (width/height) cannot be negative.")

    def _validate_symbol(self, symbol: str) -> None:
      """
      Validates that the symbol is a single, printable character, and not whitespace.

      Args:
          symbol (str): The symbol to validate.

      Raises:
          ValueError: If the symbol is not valid.
      """

      if not isinstance(symbol, str):
          raise TypeError("Symbol must be a string.")
      if len(symbol) != 1:
          raise ValueError("Symbol must be a single character.")
      if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
      if not symbol.isprintable():
            raise ValueError("Symbol must be a printable character.")

def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    art = AsciiArt()

    # Examples with error handling
    try:
        print("Square:")
        print(art.draw_square(5, "*"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "#"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(4, 6, "@"))

        print("\nTriangle:")
        print(art.draw_triangle(5, 5, "+"))

        print("\nPyramid:")
        print(art.draw_pyramid(5, "$"))

        # Example of invalid input (negative width)
        print("\nInvalid Square (negative width):")
        print(art.draw_square(-5, "*"))  # This will raise a ValueError

    except ValueError as e:
        print(f"Error: {e}")

    try:
        # Example of invalid input (multi-character symbol)
        print("\nInvalid Rectangle (multi-character symbol):")
        print(art.draw_rectangle(4, 2, "##"))  # This will raise a ValueError
    except ValueError as e:
        print(f"Error: {e}")

    try:
        # Example of zero size
        print("\nEmpty Square (zero width/height):")
        print(art.draw_square(0, "*"))  # width == 0
    except ValueError as e:
        print(f"Error: {e}")

    try:
        # Example of incorrect Triangle
        print("\nIncorrect Triangle (width < height):")
        print(art.draw_triangle(2, 5, "T"))
    except ValueError as e:
        print(f"Error: {e}")

    try:
      # Example of invalid size (size is str, but not int)
      print("\nInvalid Square (size/width is not int):")
      print(art.draw_square("5","*"))
    except TypeError as e:
        print(f"Error: {e}")

    try:
      # Example of invalid size (symbol is int, but not str)
      print("\nInvalid Square (symbol is not str):")
      print(art.draw_square(5,5))
    except TypeError as e:
        print(f"Error: {e}")   

if __name__ == "__main__":
    main()
