import math

class AsciiArt:
    """
    A class for generating 2D ASCII art shapes. Provides methods to draw various
    shapes including square, rectangle, parallelogram, right-angled triangle, and pyramid.
    """

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validates that a given dimension is a positive integer.

        Args:
            value (int): The dimension value to validate.
            name (str): The name of the dimension (for error messages).

        Raises:
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the symbol is a single non-whitespace character.

        Args:
            symbol (str): The character used for drawing.

        Raises:
            ValueError: If symbol is not a single non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square shape with each side of specified 'width'.

        Args:
            width (int): The length of each side of the square.
            symbol (str): A single non-whitespace character used to fill the square.

        Returns:
            str: A multi-line string representing the ASCII art square.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)

        # Create a list of rows, each row containing 'width' symbols.
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle shape with the given width and height.

        Args:
            width (int): The number of symbols in each row.
            height (int): The number of rows.
            symbol (str): A single non-whitespace character used to fill the rectangle.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram shape where each subsequent row is shifted by one space.

        Args:
            width (int): The number of symbols per row.
            height (int): The number of rows.
            symbol (str): A single non-whitespace character used to fill the shape.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        # Each row is indented with an increasing number of spaces.
        for row in range(height):
            # Leading spaces shift the shape to the right by the row number.
            line = " " * row + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally from the top-left corner.
        The triangle's base (last row) will contain 'width' symbols and it will have 'height' rows.
        The number of symbols in each row is scaled proportionally.

        Args:
            width (int): The number of symbols in the bottom row.
            height (int): The total number of rows in the triangle.
            symbol (str): A single non-whitespace character used to fill the triangle.

        Returns:
            str: A multi-line string representing the ASCII art right-angled triangle.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        # For each row, calculate the number of symbols such that the last row has 'width' symbols.
        for row in range(1, height + 1):
            # Compute the number of symbols for this row.
            symbols_count = max(1, int(math.ceil(width * row / height)))
            lines.append(symbol * symbols_count)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with a given height. The pyramid will be centered,
        with the first row containing one symbol and each subsequent row having two more symbols.

        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): A single non-whitespace character used to fill the pyramid.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        total_width = 2 * height - 1  # The base width of the pyramid
        
        for row in range(height):
            symbols_count = 2 * row + 1
            # Calculate leading spaces to center the pyramid row.
            spaces = (total_width - symbols_count) // 2
            line = " " * spaces + symbol * symbols_count
            lines.append(line)
        return "\n".join(lines)


def main():
    """
    A console-based interface for the ASCII Art app.
    Users can select a shape to draw and input the required parameters.
    """
    art_generator = AsciiArt()
    menu = (
        "\nChoose a shape to draw:\n"
        "1. Square\n"
        "2. Rectangle\n"
        "3. Parallelogram\n"
        "4. Triangle\n"
        "5. Pyramid\n"
        "6. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()
        if choice == '6':
            print("Exiting ASCII Art App. Goodbye!")
            break

        try:
            if choice == '1':
                width = int(input("Enter width: "))
                symbol = input("Enter a symbol (single non-whitespace character): ")
                art = art_generator.draw_square(width, symbol)
            elif choice == '2':
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                symbol = input("Enter a symbol (single non-whitespace character): ")
                art = art_generator.draw_rectangle(width, height, symbol)
            elif choice == '3':
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                symbol = input("Enter a symbol (single non-whitespace character): ")
                art = art_generator.draw_parallelogram(width, height, symbol)
            elif choice == '4':
                width = int(input("Enter base width: "))
                height = int(input("Enter height: "))
                symbol = input("Enter a symbol (single non-whitespace character): ")
                art = art_generator.draw_triangle(width, height, symbol)
            elif choice == '5':
                height = int(input("Enter height: "))
                symbol = input("Enter a symbol (single non-whitespace character): ")
                art = art_generator.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please select a valid option (1-6).")
                continue

            print("\n" + art + "\n")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()
