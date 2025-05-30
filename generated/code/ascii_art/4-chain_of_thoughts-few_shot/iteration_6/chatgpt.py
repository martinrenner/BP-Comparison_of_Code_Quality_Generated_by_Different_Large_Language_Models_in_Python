class AsciiArt:
    """
    A console-based ASCII art generator that implements functions for drawing various 2D shapes.
    The shapes include square, rectangle, parallelogram, right-angled triangle, and symmetrical pyramid.
    """

    def _validate_dimension(self, value: int, name: str) -> None:
        """
        Validates that a dimension is a positive integer.

        Args:
            value (int): The dimension value to validate.
            name (str): The name of the dimension (e.g., "width", "height").

        Raises:
            ValueError: If the value is not a positive integer.
        """
        if not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the symbol is a non-whitespace single character.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            ValueError: If the symbol is not a single non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a non-whitespace single character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square that is completely filled with the chosen symbol.

        Args:
            width (int): The side-length of the square.
            symbol (str): The printable symbol used to fill the square.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If width is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)

        # Create a square with 'width' rows and 'width' columns.
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle that is completely filled with the chosen symbol.

        Args:
            width (int): The number of symbols in each row.
            height (int): The number of rows.
            symbol (str): The printable symbol used to fill the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If width or height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram that grows diagonally to the right.
        Each row is shifted by one space compared to the previous row.
        
        Args:
            width (int): The number of symbols in each row.
            height (int): The number of rows.
            symbol (str): The printable symbol used to fill the parallelogram.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If width or height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally to the right.
        The triangle is constructed with 'height' rows where the number of symbols in each row
        increases from 1 (or close to 1) in the first row to 'width' in the last row.

        This function uses linear interpolation to determine the number of symbols per row.
        If integer division results in zero, it ensures at least one symbol is printed.

        Args:
            width (int): The number of symbols in the last (base) row.
            height (int): The total number of rows.
            symbol (str): The printable symbol used to fill the triangle.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            ValueError: If width or height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Compute the number of symbols for the current row using proportional scaling.
            # Ensuring at least one symbol per row.
            num_symbols = (i + 1) * width // height
            if num_symbols < 1:
                num_symbols = 1
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid that is completely filled with the chosen symbol.
        The pyramid has 'height' rows, where the base of the pyramid has (2*height - 1) symbols.

        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): The printable symbol used to fill the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Calculate the number of leading spaces and symbols for the current row.
            spaces = height - i - 1
            num_symbols = 2 * i + 1
            lines.append(" " * spaces + symbol * num_symbols)
        return "\n".join(lines)


def main():
    """
    Provides a simple console-based menu for the ASCII art generator.
    The user can choose a shape and provide the necessary dimensions and symbol.
    """
    art = AsciiArt()

    menu = (
        "\nASCII Art Generator Menu:\n"
        "1. Draw Square\n"
        "2. Draw Rectangle\n"
        "3. Draw Parallelogram\n"
        "4. Draw Right-Angled Triangle\n"
        "5. Draw Pyramid\n"
        "0. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Enter your choice (0-5): ").strip()

        if choice == "0":
            print("Exiting the ASCII Art Generator. Goodbye!")
            break

        try:
            if choice == "1":
                width = int(input("Enter the side length of the square: "))
                symbol = input("Enter a single non-whitespace character for drawing: ")
                result = art.draw_square(width, symbol)
            elif choice == "2":
                width = int(input("Enter the width of the rectangle: "))
                height = int(input("Enter the height of the rectangle: "))
                symbol = input("Enter a single non-whitespace character for drawing: ")
                result = art.draw_rectangle(width, height, symbol)
            elif choice == "3":
                width = int(input("Enter the width of the parallelogram: "))
                height = int(input("Enter the height of the parallelogram: "))
                symbol = input("Enter a single non-whitespace character for drawing: ")
                result = art.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                width = int(input("Enter the base width of the triangle (in symbols): "))
                height = int(input("Enter the height of the triangle (in rows): "))
                symbol = input("Enter a single non-whitespace character for drawing: ")
                result = art.draw_triangle(width, height, symbol)
            elif choice == "5":
                height = int(input("Enter the height of the pyramid: "))
                symbol = input("Enter a single non-whitespace character for drawing: ")
                result = art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please enter a number from 0 to 5.")
                continue

            print("\nGenerated ASCII Art:\n")
            print(result)
        except ValueError as err:
            print(f"Error: {err}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")


if __name__ == "__main__":
    main()
