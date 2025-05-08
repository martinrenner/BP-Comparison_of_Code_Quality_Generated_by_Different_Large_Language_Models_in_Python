class AsciiArt:
    """
    A class for generating various ASCII art shapes.
    Provides methods to draw shapes: square, rectangle, parallelogram,
    right-angled triangle, and pyramid.
    """

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validate that a dimension (width/height) is a positive integer.
        
        :param value: The dimension value to validate.
        :param name: The name of the dimension (for error messages).
        :raises ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer, got {value}.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the symbol is a single non-whitespace character.
        
        :param symbol: The symbol to validate.
        :raises ValueError: If symbol is not a single non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square with the given width using the specified symbol.

        :param width: The width of the square.
        :param symbol: The symbol to use for drawing.
        :return: A multi-line string representing the square.
        :raises ValueError: If width is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_symbol(symbol)

        lines = []
        for _ in range(width):
            line = symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle with the given width and height using the specified symbol.

        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        :param symbol: The symbol to use for drawing.
        :return: A multi-line string representing the rectangle.
        :raises ValueError: If width or height are not positive integers or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        lines = []
        for _ in range(height):
            line = symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram that grows diagonally to the right starting from
        the top-left corner. Each subsequent row is shifted by one space.

        :param width: The width of the parallelogram.
        :param height: The height of the parallelogram.
        :param symbol: The symbol to use for drawing.
        :return: A multi-line string representing the parallelogram.
        :raises ValueError: If width or height are not positive integers or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        
        lines = []
        for i in range(height):
            # Shift each row by i spaces.
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally to the right from the top-left corner.
        The triangle is defined so that the first row has 1 symbol and 
        the last row has exactly 'width' symbols. The number of symbols in the intermediate 
        rows is determined by linear interpolation.

        :param width: The width of the triangle's base.
        :param height: The height (number of rows) of the triangle.
        :param symbol: The symbol to use for drawing.
        :return: A multi-line string representing the triangle.
        :raises ValueError: If width or height are not positive integers or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        lines = []
        if height == 1:
            # In the degenerate case of one row, draw a full row.
            lines.append(symbol * width)
        else:
            # For each row, interpolate the number of symbols from 1 to width.
            for i in range(height):
                # Calculation: row i gets (i*(width-1)/(height-1) + 1) symbols
                num_symbols = int(i * (width - 1) / (height - 1)) + 1
                line = symbol * num_symbols
                lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the given height using the specified symbol.
        The pyramid is centered with the top row containing 1 symbol and each subsequent
        row increasing the symbol count by 2.

        :param height: The height of the pyramid (number of rows).
        :param symbol: The symbol to use for drawing.
        :return: A multi-line string representing the pyramid.
        :raises ValueError: If height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        
        lines = []
        for i in range(1, height + 1):
            # Number of symbols in the current row.
            num_symbols = 2 * i - 1
            # Center the symbols by padding with spaces.
            padding = " " * (height - i)
            line = padding + symbol * num_symbols + padding
            lines.append(line)
        return "\n".join(lines)


def main():
    """
    Main function that provides a console interface for selecting
    a shape and drawing its ASCII art.
    """
    art = AsciiArt()
    
    menu = """
Select a shape to draw:
1. Square
2. Rectangle
3. Parallelogram
4. Right-Angled Triangle
5. Pyramid
0. Exit
"""

    while True:
        print(menu)
        choice = input("Enter your choice (0-5): ").strip()
        if choice == "0":
            print("Exiting the ASCII Art application. Goodbye!")
            break

        try:
            if choice == "1":
                width = int(input("Enter the width of the square: ").strip())
                symbol = input("Enter the symbol to use: ").strip()
                output = art.draw_square(width, symbol)
            elif choice == "2":
                width = int(input("Enter the width of the rectangle: ").strip())
                height = int(input("Enter the height of the rectangle: ").strip())
                symbol = input("Enter the symbol to use: ").strip()
                output = art.draw_rectangle(width, height, symbol)
            elif choice == "3":
                width = int(input("Enter the width of the parallelogram: ").strip())
                height = int(input("Enter the height of the parallelogram: ").strip())
                symbol = input("Enter the symbol to use: ").strip()
                output = art.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                width = int(input("Enter the width (base) of the triangle: ").strip())
                height = int(input("Enter the height of the triangle: ").strip())
                symbol = input("Enter the symbol to use: ").strip()
                output = art.draw_triangle(width, height, symbol)
            elif choice == "5":
                height = int(input("Enter the height of the pyramid: ").strip())
                symbol = input("Enter the symbol to use: ").strip()
                output = art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please select a valid option.")
                continue

            print("\nGenerated ASCII Art:")
            print(output)
        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
