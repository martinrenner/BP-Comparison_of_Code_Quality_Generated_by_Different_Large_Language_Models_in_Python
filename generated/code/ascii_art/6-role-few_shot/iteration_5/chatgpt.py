class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.
    
    This class provides methods to generate a square, rectangle, parallelogram,
    right-angled triangle, and symmetrical pyramid using a single printable symbol.
    Each method returns a multi-line string containing the ASCII art.
    """

    def _validate_dimensions(self, *dimensions: int) -> None:
        """
        Validates that provided dimensions are positive integers.

        Args:
            *dimensions (int): One or more dimension values.

        Raises:
            ValueError: If any dimension is not a positive integer.
        """
        for dim in dimensions:
            if not isinstance(dim, int) or dim < 1:
                raise ValueError("Dimensions must be positive integers.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the provided symbol is a single, non-whitespace character.

        Args:
            symbol (str): A string representing the drawing symbol.

        Raises:
            ValueError: If the symbol is not exactly one non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a completely filled square.

        Args:
            width (int): The number of characters on each side of the square.
            symbol (str): The character to use in drawing the square.

        Returns:
            str: A multi-line string representing the square.
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)

        row = symbol * width
        return "\n".join([row for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled rectangle.

        Args:
            width (int): The number of characters in each row.
            height (int): The number of rows.
            symbol (str): The character to use in drawing the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        row = symbol * width
        return "\n".join([row for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that grows diagonally to the right.

        Each subsequent row is indented by one additional space relative to the previous row.

        Args:
            width (int): The number of characters in each row (before shifting).
            height (int): The number of rows.
            symbol (str): The character to use in drawing the parallelogram.

        Returns:
            str: A multi-line string representing the parallelogram.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally to the right.

        This method generates a triangle with a given number of rows (height) where the
        number of symbols in each row is scaled proportionally so that the last row has a total
        of 'width' symbols. The growth factor is computed by linear interpolation.

        Args:
            width (int): The desired maximum width (number of symbols in the last row).
            height (int): The number of rows of the triangle.
            symbol (str): The character to use in drawing the triangle.

        Returns:
            str: A multi-line string representing the right-angled triangle.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        lines = []
        # For each row, compute the number of symbols by linear interpolation.
        for i in range(height):
            # Calculate proportionally how many symbols to print.
            # Ensure at least one symbol per row.
            count = max(1, round((i + 1) * width / height))
            lines.append(symbol * count)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a completely filled symmetrical pyramid.

        The pyramid will have the specified height with the base having (2 * height - 1)
        symbols. Each row is centered with preceding spaces.

        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): The character to use in drawing the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Number of spaces for left padding.
            padding = " " * (height - i - 1)
            # Number of symbols in the current row is 2*i + 1.
            symbols = symbol * (2 * i + 1)
            lines.append(padding + symbols)
        return "\n".join(lines)


def main():
    """
    The main function to run the console-based ASCII Art application.
    
    This function presents a menu for the user to choose a shape and enter its parameters.
    It then prints the corresponding ASCII art.
    """
    art = AsciiArt()

    menu = (
        "ASCII Art Generator\n"
        "-------------------\n"
        "Select a shape to draw:\n"
        "1. Square\n"
        "2. Rectangle\n"
        "3. Parallelogram\n"
        "4. Triangle (right-angled)\n"
        "5. Pyramid\n"
        "0. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            print("Exiting the ASCII Art Generator. Goodbye!")
            break

        try:
            if choice == "1":
                width = int(input("Enter the width of the square: "))
                symbol = input("Enter a single non-whitespace symbol: ")
                result = art.draw_square(width, symbol)
            elif choice == "2":
                width = int(input("Enter the width of the rectangle: "))
                height = int(input("Enter the height of the rectangle: "))
                symbol = input("Enter a single non-whitespace symbol: ")
                result = art.draw_rectangle(width, height, symbol)
            elif choice == "3":
                width = int(input("Enter the width of the parallelogram: "))
                height = int(input("Enter the height of the parallelogram: "))
                symbol = input("Enter a single non-whitespace symbol: ")
                result = art.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                width = int(input("Enter the maximum width of the triangle (symbols in the last row): "))
                height = int(input("Enter the height of the triangle (number of rows): "))
                symbol = input("Enter a single non-whitespace symbol: ")
                result = art.draw_triangle(width, height, symbol)
            elif choice == "5":
                height = int(input("Enter the height of the pyramid: "))
                symbol = input("Enter a single non-whitespace symbol: ")
                result = art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please try again.\n")
                continue

            print("\nHere is your shape:")
            print(result)
        except ValueError as ve:
            print(f"Error: {ve}")
        print("\n" + "=" * 40 + "\n")


if __name__ == '__main__':
    main()
