import math


class AsciiArt:
    """
    A class providing methods for drawing various ASCII shapes.
    All shapes are completely filled with a user-selected symbol.
    """

    @staticmethod
    def _validate_dimension(*dimensions: int) -> None:
        """
        Validates that all dimension values are positive integers.

        Args:
            *dimensions (int): One or more dimension values (width, height).

        Raises:
            ValueError: If any dimension is not a positive integer.
        """
        for dim in dimensions:
            if not isinstance(dim, int) or dim <= 0:
                raise ValueError("Dimensions must be positive integers.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the drawing symbol is a single, non-whitespace character.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            ValueError: If the symbol is not a single non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square.

        Args:
            width (int): The width (and height) of the square.
            symbol (str): A single printable character used for drawing.

        Returns:
            str: A string containing the ASCII art of a square.

        Raises:
            ValueError: If invalid width or symbol is provided.
        """
        self._validate_dimension(width)
        self._validate_symbol(symbol)

        lines = [(symbol * width) for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): A single printable character used for drawing.

        Returns:
            str: A string containing the ASCII art of a rectangle.

        Raises:
            ValueError: If invalid width, height or symbol is provided.
        """
        self._validate_dimension(width, height)
        self._validate_symbol(symbol)

        lines = [(symbol * width) for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that shifts one space to the right per row.

        Args:
            width (int): The number of symbols in the first row.
            height (int): The total number of rows.
            symbol (str): A single printable character used for drawing.

        Returns:
            str: A string containing the ASCII art of a parallelogram.

        Raises:
            ValueError: If invalid width, height or symbol is provided.
        """
        self._validate_dimension(width, height)
        self._validate_symbol(symbol)

        lines = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle.
        The triangle has a base of 'width' symbols and is 'height' rows tall.
        The number of symbols per row grows approximately proportionally
        from 1 (or more) symbol in the first row to 'width' symbols in the last row.

        Args:
            width (int): The number of symbols in the base (last row) of the triangle.
            height (int): The number of rows of the triangle.
            symbol (str): A single printable character used for drawing.

        Returns:
            str: A string containing the ASCII art of a right-angled triangle.

        Raises:
            ValueError: If invalid width, height or symbol is provided.
        """
        self._validate_dimension(width, height)
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Calculate the number of symbols for the current row.
            # Ensures that the last row has exactly 'width' symbols.
            num_symbols = math.ceil((i + 1) * width / height)
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid.
        The pyramid's base width is (2 * height - 1).

        Args:
            height (int): The number of rows of the pyramid.
            symbol (str): A single printable character used for drawing.

        Returns:
            str: A string containing the ASCII art of a pyramid.

        Raises:
            ValueError: If invalid height or symbol is provided.
        """
        self._validate_dimension(height)
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Number of symbols in the current row.
            count = 2 * i + 1
            # Calculate left padding to center the pyramid.
            padding = height - i - 1
            lines.append(" " * padding + symbol * count)
        return "\n".join(lines)


def main():
    """
    Main function for the console-based ASCII Art application.
    Allows the user to choose a shape, input parameters, and displays the resulting ASCII art.
    """
    art = AsciiArt()
    print("Welcome to the ASCII Art Drawer!")
    menu = (
        "\nPlease select a shape to draw:\n"
        "1. Square\n"
        "2. Rectangle\n"
        "3. Parallelogram\n"
        "4. Right-Angled Triangle\n"
        "5. Pyramid\n"
        "6. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "6":
            print("Goodbye!")
            break

        try:
            if choice == "1":
                width = int(input("Enter the width of the square: "))
                symbol = input("Enter a single character for the square: ").strip()
                result = art.draw_square(width, symbol)
            elif choice == "2":
                width = int(input("Enter the width of the rectangle: "))
                height = int(input("Enter the height of the rectangle: "))
                symbol = input("Enter a single character for the rectangle: ").strip()
                result = art.draw_rectangle(width, height, symbol)
            elif choice == "3":
                width = int(input("Enter the width of the parallelogram: "))
                height = int(input("Enter the height of the parallelogram: "))
                symbol = input("Enter a single character for the parallelogram: ").strip()
                result = art.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                width = int(input("Enter the width of the triangle's base: "))
                height = int(input("Enter the height of the triangle: "))
                symbol = input("Enter a single character for the triangle: ").strip()
                result = art.draw_triangle(width, height, symbol)
            elif choice == "5":
                height = int(input("Enter the height of the pyramid: "))
                symbol = input("Enter a single character for the pyramid: ").strip()
                result = art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please try again.")
                continue

            print("\n" + result)
        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
