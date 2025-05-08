class AsciiArt:
    """
    A class for generating various ASCII art shapes.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width filled with the given symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to fill the square with.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is negative, symbol is not a single character, or symbol is whitespace.
        """
        self._validate_input(width, symbol)

        square = ""
        for _ in range(width):
            square += symbol * width + "\n"
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height, filled with the given symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to fill the rectangle with.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is negative, symbol is not a single character, or symbol is whitespace.
        """
        self._validate_input(width, symbol)
        if height < 0:
            raise ValueError("Height cannot be negative.")

        rectangle = ""
        for _ in range(height):
            rectangle += symbol * width + "\n"
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified width and height, filled with the given symbol.
        The parallelogram is slanted to the right.

        Args:
            width (int): The width of each row.
            height (int): The number of rows.
            symbol (str): The character to use for drawing.

        Returns:
            str: The ASCII art representation of the parallelogram.

        Raises:
            ValueError: If width or height is negative, symbol is not a single character, or is whitespace.
        """
        self._validate_input(width, symbol)
        if height < 0:
            raise ValueError("Height cannot be negative.")

        parallelogram = ""
        for i in range(height):
            parallelogram += " " * i + symbol * width + "\n"
        return parallelogram

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with the specified width and height, filled with the given symbol.

        Args:
            width (int): The maximum width of the triangle (at the base).
            height (int): The height of the triangle.
            symbol (str): The character to use.

        Returns:
            str: The ASCII art representation of the triangle.

        Raises:
            ValueError: If width or height is negative, or symbol is not a single character, or is whitespace.
        """
        self._validate_input(width, symbol)  # Basic validation (width, symbol)
        if height < 0:
            raise ValueError("Height cannot be negative.")

        triangle = ""
        # Ensure that triangle doesn't exceed given width.  Important for consistency.
        for i in range(min(height, width)):  # Iterate up to the min of height or width
            triangle += symbol * (i + 1) + "\n"
        return triangle
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a pyramid with the specified height, filled with the given symbol.

        Args:
            height (int): The height of the pyramid (number of rows).
            symbol (str): The character to use.

        Returns:
            str: The ASCII art representation of the pyramid.

        Raises:
            ValueError: If height is negative, or symbol is not a single character, or is whitespace.
        """
        if height < 0:  # Height-specific check, _validate_input handles symbol check
            raise ValueError("Height cannot be negative.")

        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")

        pyramid = ""
        for i in range(height):
            pyramid += " " * (height - i - 1) + symbol * (2 * i + 1) + "\n"
        return pyramid

    def _validate_input(self, width: int, symbol: str):
        """
        Validates the input parameters for the drawing functions.

        Args:
            width (int): The width of the shape.
            symbol (str): The character to fill the shape with.

        Raises:
            ValueError: If width is negative, symbol is not a single character, or symbol is whitespace.
        """
        if width < 0:
            raise ValueError("Width cannot be negative.")
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
def main():
  # Example Usage with a loop and interactive input.
  ascii_art = AsciiArt()
  functions = {
    "square": ascii_art.draw_square,
    "rectangle": ascii_art.draw_rectangle,
    "parallelogram": ascii_art.draw_parallelogram,
    "triangle": ascii_art.draw_triangle,
    "pyramid": ascii_art.draw_pyramid,
  }

  while True:
    print("\nAvailable shapes:", ", ".join(functions.keys()))
    shape_choice = input("Enter the shape you want to draw (or 'exit' to quit): ").lower()
    if shape_choice == 'exit':
      break

    if shape_choice not in functions:
      print("Invalid shape choice.")
      continue

    symbol = input("Enter the symbol you want to use: ")

    try:
      if shape_choice == "square":
        width = int(input("Enter the width: "))
        print(functions[shape_choice](width, symbol))
      elif shape_choice == "rectangle":
        width = int(input("Enter the width: "))
        height = int(input("Enter the height: "))
        print(functions[shape_choice](width, height, symbol))
      elif shape_choice == "parallelogram":
        width = int(input("Enter the width: "))
        height = int(input("Enter the height: "))
        print(functions[shape_choice](width, height, symbol))
      elif shape_choice == "triangle":
        width = int(input("Enter the width: "))
        height = int(input("Enter the height: "))
        print(functions[shape_choice](width, height, symbol))

      elif shape_choice == "pyramid":
        height = int(input("Enter the height: "))
        print(functions[shape_choice](height, symbol))

    except ValueError as e:
      print(f"Error: {e}")

if __name__ == "__main__":
    main()
