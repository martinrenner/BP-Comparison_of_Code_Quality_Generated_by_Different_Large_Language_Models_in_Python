import math


class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.
    
    Supported shapes:
      - Square
      - Rectangle
      - Parallelogram
      - Right-angled Triangle
      - Pyramid
    """

    def _validate_dimension(self, dimension: int, name: str) -> None:
        """
        Validates that a given dimension is a positive integer.

        Args:
            dimension (int): The dimension value (width or height).
            name (str): The name of the dimension (for error messages).

        Raises:
            ValueError: If the dimension is not a positive integer.
        """
        if not isinstance(dimension, int) or dimension <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the symbol is a single, non-whitespace character.

        Args:
            symbol (str): The character to use for drawing.

        Raises:
            ValueError: If symbol is not exactly one non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of a given width using the specified symbol.

        Args:
            width (int): The number of symbols on each side.
            symbol (str): A single character used to fill the square.

        Returns:
            str: A multi-line string representation of the square.

        Raises:
            ValueError: If width is not positive or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_symbol(symbol)
        # Each of the 'width' rows contains 'width' symbols.
        return "\n".join([symbol * width for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle using the specified dimensions and symbol.

        Args:
            width (int): Number of symbols per row.
            height (int): Number of rows.
            symbol (str): A single character used to fill the rectangle.

        Returns:
            str: A multi-line string representation of the rectangle.

        Raises:
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        return "\n".join([symbol * width for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that grows diagonally to the right.

        Each subsequent row is shifted one space to the right.

        Args:
            width (int): Number of symbols per row.
            height (int): Total number of rows.
            symbol (str): A single character used to fill the shape.

        Returns:
            str: A multi-line string representation of the parallelogram.

        Raises:
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        # Each row i is indented with i spaces.
        return "\n".join([(" " * i) + (symbol * width) for i in range(height)])

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally to the right,
        starting from the top-left corner. The triangle is filled using the given symbol.
        The parameter 'width' represents the base length (maximum number of symbols
        in the last row) and 'height' the number of rows. The number of symbols in each
        row is calculated proportionally so that the triangle scales horizontally.

        Args:
            width (int): The base width (number of symbols in the last row).
            height (int): The total number of rows.
            symbol (str): A single character used for drawing.

        Returns:
            str: A multi-line string representing the right-angled triangle.

        Raises:
            ValueError: If width/height are not positive or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        lines = []
        # Calculate the number of symbols per row using linear scaling.
        for i in range(height):
            # The proportion is (i+1)/height scaled by the base width.
            num_symbols = math.ceil((i + 1) * width / height)
            # Ensure at least 1 symbol is drawn.
            num_symbols = max(1, num_symbols)
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the given height using the specified symbol.
        The pyramid's base has a width of (2 * height - 1).

        Args:
            height (int): The number of rows (height) of the pyramid.
            symbol (str): A single character used for drawing.

        Returns:
            str: A multi-line string representation of the pyramid.

        Raises:
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        # Each row i has (2*i+1) symbols and (height-1-i) leading spaces.
        for i in range(height):
            spaces = " " * (height - 1 - i)
            symbols = symbol * (2 * i + 1)
            lines.append(spaces + symbols)
        return "\n".join(lines)


def main():
    """
    Entry point for the console-based ASCII Art application.

    Presents a menu to the user to select a shape and prompts for the dimensions
    and drawing symbol. Draws the selected ASCII art shape on the console.
    """
    ascii_art = AsciiArt()
    while True:
        print("\nASCII Art Shapes:")
        print("1. Square")
        print("2. Rectangle")
        print("3. Parallelogram")
        print("4. Right-Angled Triangle")
        print("5. Pyramid")
        print("6. Exit")
        choice = input("Select the shape to draw (1-6): ").strip()

        if choice == "6":
            print("Exiting the application.")
            break

        try:
            if choice == "1":
                width = int(input("Enter the width of the square: ").strip())
                symbol = input("Enter a single non-whitespace character for drawing: ").strip()
                result = ascii_art.draw_square(width, symbol)
            elif choice == "2":
                width = int(input("Enter the width of the rectangle: ").strip())
                height = int(input("Enter the height of the rectangle: ").strip())
                symbol = input("Enter a single non-whitespace character for drawing: ").strip()
                result = ascii_art.draw_rectangle(width, height, symbol)
            elif choice == "3":
                width = int(input("Enter the width of the parallelogram: ").strip())
                height = int(input("Enter the height of the parallelogram: ").strip())
                symbol = input("Enter a single non-whitespace character for drawing: ").strip()
                result = ascii_art.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                width = int(input("Enter the base width of the triangle: ").strip())
                height = int(input("Enter the height of the triangle: ").strip())
                symbol = input("Enter a single non-whitespace character for drawing: ").strip()
                result = ascii_art.draw_triangle(width, height, symbol)
            elif choice == "5":
                height = int(input("Enter the height of the pyramid: ").strip())
                symbol = input("Enter a single non-whitespace character for drawing: ").strip()
                result = ascii_art.draw_pyramid(height, symbol)
            else:
                print("Invalid option. Please choose a valid number (1-6).")
                continue

            print("\n" + result)
        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
