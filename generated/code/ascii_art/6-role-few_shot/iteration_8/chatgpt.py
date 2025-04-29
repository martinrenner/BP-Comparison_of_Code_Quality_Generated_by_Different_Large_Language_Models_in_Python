import math


class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.
    Provides methods to draw square, rectangle, parallelogram, right-angled triangle, and pyramid.
    """

    def _validate_dimension(self, value: int, name: str) -> None:
        """
        Validates that a dimension (width or height) is a positive integer.

        Args:
            value (int): The dimension value to validate.
            name (str): The name of the dimension (for error messages).

        Raises:
            ValueError: If the value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the drawing symbol is a single, non-whitespace printable character.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            ValueError: If symbol is not a single non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a non-whitespace single character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a completely filled square.

        Args:
            width (int): The width of the square (and number of rows).
            symbol (str): The character used for drawing.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If width is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_symbol(symbol)

        rows = [symbol * width for _ in range(width)]
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled rectangle.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character used for drawing.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If width or height are not positive integers or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        rows = [symbol * width for _ in range(height)]
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled parallelogram.
        Each row is shifted by one space to the right relative to the previous row.

        Args:
            width (int): The width of each row of the parallelogram.
            height (int): The number of rows (height) of the parallelogram.
            symbol (str): The character used for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If width or height are not positive integers or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        rows = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.
        The triangle grows diagonally to the right, starting from the top-left corner.
        The base of the triangle has the given width and the triangle spans the given height,
        with the number of symbols in each row scaled linearly.

        Args:
            width (int): The number of symbols in the base (last row) of the triangle.
            height (int): The number of rows in the triangle.
            symbol (str): The character used for drawing.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            ValueError: If width or height are not positive integers or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            # Calculate the number of symbols for current row.
            # Ensures at least one symbol per row and exactly 'width' symbols in the last row.
            num_symbols = max(1, math.ceil((i + 1) * width / height))
            rows.append(symbol * num_symbols)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.
        The base of the pyramid will have width (2 * height - 1).

        Args:
            height (int): The number of rows of the pyramid.
            symbol (str): The character used for drawing.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        total_width = 2 * height - 1
        rows = []
        for i in range(height):
            num_symbols = 2 * i + 1
            spaces = (total_width - num_symbols) // 2
            rows.append(" " * spaces + symbol * num_symbols)
        return "\n".join(rows)


def main() -> None:
    """
    Main function to run the console-based ASCII Art application.
    Provides a menu for the user to select which shape to draw and
    prompts for required parameters.
    """
    art = AsciiArt()
    menu = (
        "\nASCII Art Generator Menu:\n"
        "1. Draw Square\n"
        "2. Draw Rectangle\n"
        "3. Draw Parallelogram\n"
        "4. Draw Right-Angled Triangle\n"
        "5. Draw Pyramid\n"
        "6. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "6":
            print("Exiting the ASCII Art Generator. Goodbye!")
            break

        try:
            if choice == "1":
                width = int(input("Enter square width: "))
                symbol = input("Enter a single non-whitespace symbol: ")
                result = art.draw_square(width, symbol)
                print("\n" + result)
            elif choice == "2":
                width = int(input("Enter rectangle width: "))
                height = int(input("Enter rectangle height: "))
                symbol = input("Enter a single non-whitespace symbol: ")
                result = art.draw_rectangle(width, height, symbol)
                print("\n" + result)
            elif choice == "3":
                width = int(input("Enter parallelogram width: "))
                height = int(input("Enter parallelogram height: "))
                symbol = input("Enter a single non-whitespace symbol: ")
                result = art.draw_parallelogram(width, height, symbol)
                print("\n" + result)
            elif choice == "4":
                width = int(input("Enter the base width for the triangle: "))
                height = int(input("Enter the triangle height (number of rows): "))
                symbol = input("Enter a single non-whitespace symbol: ")
                result = art.draw_triangle(width, height, symbol)
                print("\n" + result)
            elif choice == "5":
                height = int(input("Enter pyramid height (number of rows): "))
                symbol = input("Enter a single non-whitespace symbol: ")
                result = art.draw_pyramid(height, symbol)
                print("\n" + result)
            else:
                print("Invalid choice. Please select a number between 1 and 6.")
        except ValueError as ve:
            print(f"Error: {ve}")


if __name__ == "__main__":
    main()
