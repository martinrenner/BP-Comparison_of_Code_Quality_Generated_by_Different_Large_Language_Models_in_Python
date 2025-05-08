class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.
    Each drawing method returns a multi-line string representing
    the desired shape. The implementation validates inputs and uses
    object-oriented principles for modularity and maintainability.
    """

    def _validate_dimension(self, dimension: int, name: str) -> None:
        """
        Validates that the given dimension (width or height) is a positive integer.

        Args:
            dimension (int): The value to validate.
            name (str): The name of the dimension (e.g., "width", "height").

        Raises:
            ValueError: If dimension is not a positive integer.
        """
        if not isinstance(dimension, int) or dimension < 1:
            raise ValueError(f"{name.capitalize()} must be a positive integer. Given: {dimension}")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the symbol is a single non-whitespace character.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            ValueError: If symbol is not a single non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of the specified width using the given symbol.

        Args:
            width (int): The side length of the square.
            symbol (str): A single character used to fill the square.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If width is invalid or symbol is not a valid character.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)
        # The square is built by repeating the same row 'width' times.
        rows = [symbol * width for _ in range(width)]
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle with provided width, height, and symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): A single character used to fill the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If width or height is invalid or symbol is not a valid character.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        rows = [symbol * width for _ in range(height)]
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that grows diagonally to the right.
        Each subsequent row is shifted one extra space to the right.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): A single character used to fill the shape.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If width or height is invalid or symbol is not a valid character.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        rows = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle that grows diagonally to
        the right, starting at the top-left corner. The first row contains
        one symbol and the last row contains 'width' symbols. If height > 1,
        the number of symbols in each row is scaled evenly.

        Args:
            width (int): The number of symbols in the triangle's base.
            height (int): The number of rows in the triangle.
            symbol (str): A single character used to fill the triangle.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            ValueError: If width or height is invalid or symbol is not a valid character.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows = []
        if height == 1:
            # For a single-row triangle, fill the entire row with the given width.
            rows.append(symbol * width)
        else:
            # Compute the incremental change between rows.
            ratio = (width - 1) / (height - 1)
            for i in range(height):
                # First row gets 1 symbol, the last row gets 'width' symbols.
                count = 1 + int(round(i * ratio))
                count = max(1, count)  # Ensure at least one symbol per row.
                rows.append(symbol * count)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled, symmetrical pyramid of the specified height.
        The base of the pyramid contains (2 * height - 1) symbols.

        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): A single character used to fill the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If height is invalid or symbol is not a valid character.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        rows = []
        for i in range(height):
            # Compute the number of spaces needed to center the symbols.
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            rows.append(spaces + symbols)
        return "\n".join(rows)


def main():
    """
    Main function for the console-based ASCII Art application.
    Users can select a shape from the menu and provide parameters.
    The generated ASCII art is printed to the console.
    """
    art = AsciiArt()
    while True:
        print("\n=== ASCII Art App Menu ===")
        print("1. Draw Square")
        print("2. Draw Rectangle")
        print("3. Draw Parallelogram")
        print("4. Draw Right-Angled Triangle")
        print("5. Draw Pyramid")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()
        if choice == '6':
            print("Exiting the application.")
            break

        try:
            if choice == '1':
                width = int(input("Enter the width of the square: ").strip())
                symbol = input("Enter a single non-whitespace symbol: ").strip()
                result = art.draw_square(width, symbol)
            elif choice == '2':
                width = int(input("Enter the width of the rectangle: ").strip())
                height = int(input("Enter the height of the rectangle: ").strip())
                symbol = input("Enter a single non-whitespace symbol: ").strip()
                result = art.draw_rectangle(width, height, symbol)
            elif choice == '3':
                width = int(input("Enter the width of the parallelogram: ").strip())
                height = int(input("Enter the height of the parallelogram: ").strip())
                symbol = input("Enter a single non-whitespace symbol: ").strip()
                result = art.draw_parallelogram(width, height, symbol)
            elif choice == '4':
                width = int(input("Enter the base width of the triangle: ").strip())
                height = int(input("Enter the height of the triangle: ").strip())
                symbol = input("Enter a single non-whitespace symbol: ").strip()
                result = art.draw_triangle(width, height, symbol)
            elif choice == '5':
                height = int(input("Enter the height of the pyramid: ").strip())
                symbol = input("Enter a single non-whitespace symbol: ").strip()
                result = art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please select a valid option (1-6).")
                continue

            print("\n--- Generated ASCII Art ---")
            print(result)
        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")


if __name__ == "__main__":
    main()
