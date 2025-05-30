class AsciiArt:
    """
    A class for generating console-based 2D ASCII art shapes.

    This class implements methods to generate filled ASCII shapes, including:
      - Square
      - Rectangle
      - Parallelogram (with each subsequent row indented by one space)
      - Right-angled triangle (with dimensions defined by a base and height)
      - Symmetrical pyramid

    Each drawing method validates its inputs and returns a multi-line string that,
    when printed, displays the desired ASCII art.
    """

    def _validate_dimension(self, value: int, name: str) -> None:
        """
        Validates that a given dimension (width or height) is a positive integer.

        Args:
            value (int): The dimension value to be validated.
            name (str): The name of the dimension (e.g., "width" or "height").

        Raises:
            TypeError: If the dimension value is not an integer.
            ValueError: If the dimension value is not positive (<= 0).
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive, non-zero integer.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the symbol is a single, non-whitespace character.

        Args:
            symbol (str): The symbol to be used for drawing.

        Raises:
            TypeError: If symbol is not a string.
            ValueError: If symbol length is not 1 or if it is a whitespace character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square completely filled with the chosen symbol.

        Args:
            width (int): The width (and height) of the square.
            symbol (str): The single character used to fill the square.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError or TypeError: If input validations fail.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)

        # A square is composed of 'width' rows, each containing 'width' copies of the symbol.
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle completely filled with the chosen symbol.

        Args:
            width (int): The width (number of symbols per row) of the rectangle.
            height (int): The height (number of rows) of the rectangle.
            symbol (str): The single character used to fill the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError or TypeError: If input validations fail.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram completely filled with the chosen symbol.
        The parallelogram grows diagonally to the right starting from the top-left,
        with each subsequent row shifted one space to the right.

        Args:
            width (int): The number of symbols per row (before indentation).
            height (int): The number of rows.
            symbol (str): The single character used to fill the shape.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError or TypeError: If input validations fail.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            # Each row is indented by 'row' spaces.
            line = " " * row + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle completely filled with the chosen symbol.
        This triangle has a base of 'width' symbols in its last row and 'height' rows in total.
        It "grows diagonally to the right" by increasing the number of symbols per row linearly
        from top to bottom.

        The number of symbols on each row is computed using linear interpolation:
          - For height == 1, the single row contains 'width' symbols.
          - For height > 1, the row at index i (0-indexed) gets:
                count = round((i + 1) * width / height)
            ensuring the top row has at least one symbol and the bottom row equals 'width'.

        Args:
            width (int): The total number of symbols in the last row (base) of the triangle.
            height (int): The number of rows in the triangle.
            symbol (str): The single character used to fill the triangle.

        Returns:
            str: A multi-line string representing the right-angled triangle.

        Raises:
            ValueError or TypeError: If input validations fail.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Calculate the number of symbols for this row.
            # Ensure at least one symbol is drawn.
            if height == 1:
                num_symbols = width
            else:
                num_symbols = round((i + 1) * width / height)
            num_symbols = max(1, num_symbols)
            line = symbol * num_symbols
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid completely filled with the chosen symbol.
        The pyramid is centered, and its base has a width of (2*height - 1) symbols.
        Each row i (0-indexed) contains:
          - (height - i - 1) leading spaces,
          - (2*i + 1) symbols,
          - (height - i - 1) trailing spaces (optional for centering).

        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): The single character used to fill the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError or TypeError: If input validations fail.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            num_symbols = 2 * i + 1
            num_spaces = height - i - 1
            # Center the symbols by adding equal spaces on both sides.
            line = " " * num_spaces + symbol * num_symbols + " " * num_spaces
            lines.append(line)
        return "\n".join(lines)


def main():
    """
    Main function to run the console-based ASCII art application.

    The user is prompted to select a shape and provide the required dimensions
    and symbol. The generated ASCII art is then displayed.
    """
    art_gen = AsciiArt()
    print("Welcome to the ASCII Art Generator!")
    print("Select a shape to draw:")
    print("  1. Square")
    print("  2. Rectangle")
    print("  3. Parallelogram")
    print("  4. Right-angled Triangle")
    print("  5. Pyramid")
    
    choice = input("Enter the number of your choice: ").strip()

    try:
        if choice == "1":
            width = int(input("Enter the width of the square: "))
            symbol = input("Enter a single character as the symbol: ")
            result = art_gen.draw_square(width, symbol)
        elif choice == "2":
            width = int(input("Enter the width of the rectangle: "))
            height = int(input("Enter the height of the rectangle: "))
            symbol = input("Enter a single character as the symbol: ")
            result = art_gen.draw_rectangle(width, height, symbol)
        elif choice == "3":
            width = int(input("Enter the width of the parallelogram: "))
            height = int(input("Enter the height of the parallelogram: "))
            symbol = input("Enter a single character as the symbol: ")
            result = art_gen.draw_parallelogram(width, height, symbol)
        elif choice == "4":
            width = int(input("Enter the base width of the triangle (symbols in the last row): "))
            height = int(input("Enter the height (number of rows) of the triangle: "))
            symbol = input("Enter a single character as the symbol: ")
            result = art_gen.draw_triangle(width, height, symbol)
        elif choice == "5":
            height = int(input("Enter the height of the pyramid: "))
            symbol = input("Enter a single character as the symbol: ")
            result = art_gen.draw_pyramid(height, symbol)
        else:
            print("Invalid choice. Please run the program again and select a valid option.")
            return

        print("\nHere is your ASCII art:\n")
        print(result)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
