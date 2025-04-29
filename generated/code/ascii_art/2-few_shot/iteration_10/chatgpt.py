class AsciiArt:
    """
    A class for generating console-based 2D ASCII art.
    It implements methods to draw various shapes and validates inputs according
    to the requirements of ISO/IEC 25010.
    """

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the symbol is a single, non-whitespace character.

        Args:
            symbol (str): The symbol to be used for drawing.

        Raises:
            ValueError: If the symbol is not exactly one character or is whitespace.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validates that a given dimension is a positive integer.

        Args:
            value (int): The dimension value.
            name (str): The name of the dimension (for error messages).

        Raises:
            ValueError: If the value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width using the given symbol.

        Args:
            width (int): The width (and height) of the square.
            symbol (str): A single non-whitespace character to fill the square.

        Returns:
            str: A multi-line string representing the drawn square.

        Raises:
            ValueError: If width is not positive or if the symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_symbol(symbol)

        row = symbol * width
        square = "\n".join([row for _ in range(width)])
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified dimensions using the given symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): A single non-whitespace character to fill the rectangle.

        Returns:
            str: A multi-line string representing the drawn rectangle.

        Raises:
            ValueError: If width/height is not positive or if the symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        row = symbol * width
        rectangle = "\n".join([row for _ in range(height)])
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram that grows diagonally to the right.
        Each subsequent row is indented by one extra space.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): A single non-whitespace character to fill the shape.

        Returns:
            str: A multi-line string representing the drawn parallelogram.

        Raises:
            ValueError: If width/height is not positive or if the symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            spaces = " " * i  # Each row is shifted one space further to the right.
            row_content = symbol * width
            lines.append(spaces + row_content)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with the right angle at the top-left.
        The triangle grows diagonally and the number of symbols in the last row is equal to 'width'.
        For proper scaling when height > 1, the number of symbols per row is calculated
        using linear interpolation.

        Args:
            width (int): The number of symbols in the base (last row) of the triangle.
            height (int): The total number of rows in the triangle.
            symbol (str): A single non-whitespace character to fill the triangle.

        Returns:
            str: A multi-line string representing the drawn triangle.

        Raises:
            ValueError: If width/height is not positive or if the symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        lines = []
        if height == 1:
            # Single row triangle equals the base.
            lines.append(symbol * width)
        else:
            for i in range(height):
                # Use linear interpolation so that:
                #   First row = 1 symbol, Last row = width symbols.
                num_symbols = int((width - 1) * (i / (height - 1))) + 1
                lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the specified height.
        Each row is centered and contains an odd number of symbols.

        Args:
            height (int): The height of the pyramid.
            symbol (str): A single non-whitespace character to fill the pyramid.

        Returns:
            str: A multi-line string representing the drawn pyramid.

        Raises:
            ValueError: If height is not positive or if the symbol is invalid.
        """
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Calculate the number of symbols for the current row.
            num_symbols = 2 * i + 1
            # Calculate leading spaces to center the pyramid.
            spaces = " " * (height - i - 1)
            lines.append(spaces + symbol * num_symbols)
        return "\n".join(lines)


def main():
    """
    Console-based interface for the ASCII Art Generator.
    Presents a menu to the user to draw various ASCII shapes.
    """
    ascii_art = AsciiArt()

    menu = (
        "\n=== ASCII Art Generator ===\n"
        "1. Draw Square\n"
        "2. Draw Rectangle\n"
        "3. Draw Parallelogram\n"
        "4. Draw Right-angled Triangle\n"
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
                width = int(input("Enter the width of the square: "))
                symbol = input("Enter a single character symbol: ")
                shape_str = ascii_art.draw_square(width, symbol)
            elif choice == "2":
                width = int(input("Enter the width of the rectangle: "))
                height = int(input("Enter the height of the rectangle: "))
                symbol = input("Enter a single character symbol: ")
                shape_str = ascii_art.draw_rectangle(width, height, symbol)
            elif choice == "3":
                width = int(input("Enter the width of the parallelogram: "))
                height = int(input("Enter the height of the parallelogram: "))
                symbol = input("Enter a single character symbol: ")
                shape_str = ascii_art.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                width = int(input("Enter the base width of the triangle: "))
                height = int(input("Enter the height of the triangle: "))
                symbol = input("Enter a single character symbol: ")
                shape_str = ascii_art.draw_triangle(width, height, symbol)
            elif choice == "5":
                height = int(input("Enter the height of the pyramid: "))
                symbol = input("Enter a single character symbol: ")
                shape_str = ascii_art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
                continue

            print("\nGenerated ASCII Art:\n")
            print(shape_str)
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            # Catch unexpected errors.
            print(f"An unexpected error occurred: {e}")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
