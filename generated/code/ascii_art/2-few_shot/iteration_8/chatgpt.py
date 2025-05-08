import math

class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    This class provides methods to draw various shapes such as a square,
    rectangle, parallelogram, right-angled triangle, and pyramid using a
    single printable character.
    """

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validates that the provided dimension is a positive integer.

        Args:
            value (int): The dimension to validate.
            name (str): The name of the dimension (for error messages).

        Raises:
            ValueError: If the value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the symbol is a single non-whitespace character.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            ValueError: If the symbol is not a single printable non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a completely filled square.

        Args:
            width (int): The width (and height) of the square.
            symbol (str): A single character used to draw the square.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If 'width' is not positive or 'symbol' is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_symbol(symbol)

        # Create a list of rows, each containing "width" number of symbols.
        rows = [symbol * width for _ in range(width)]
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled rectangle.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): A single character used to draw the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If 'width' or 'height' is not positive or 'symbol' is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        rows = [symbol * width for _ in range(height)]
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled parallelogram that shifts one space to the right per row.

        The shape starts at the top-left corner and grows diagonally to the right.

        Args:
            width (int): The width of each row of the parallelogram.
            height (int): The number of rows in the parallelogram.
            symbol (str): A single character used to draw the shape.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If 'width' or 'height' is not positive or 'symbol' is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        rows = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled right-angled triangle.
        
        The triangle is drawn starting from the top-left corner and grows diagonally to the right.
        The bottom row will have the specified 'width' number of symbols and the triangle will be
        scaled vertically to have 'height' rows.

        Args:
            width (int): The maximum number of symbols in the triangle's base.
            height (int): The number of rows of the triangle.
            symbol (str): A single character used to draw the triangle.
        
        Returns:
            str: A multi-line string representing the triangle.
        
        Raises:
            ValueError: If 'width' or 'height' is not positive or 'symbol' is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        rows = []
        # For each row, calculate the number of symbols proportionally.
        for i in range(height):
            # Scale the number of symbols so that the last row equals 'width'
            num_symbols = math.ceil((i + 1) * width / height)
            rows.append(symbol * num_symbols)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a completely filled symmetrical pyramid.

        The pyramid will have 'height' rows and its base will contain (2 * height - 1) symbols.
        
        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): A single character used to draw the pyramid.
        
        Returns:
            str: A multi-line string representing the pyramid.
        
        Raises:
            ValueError: If 'height' is not positive or 'symbol' is invalid.
        """
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            num_symbols = 2 * i + 1
            padding = " " * (height - i - 1)
            rows.append(padding + (symbol * num_symbols))
        return "\n".join(rows)

def main():
    """
    Console-based interface for the ASCII Art App.
    
    Allows the user to choose a shape, provide dimensions and a symbol, 
    and then displays the generated ASCII art.
    """
    art_generator = AsciiArt()

    menu = (
        "ASCII Art Application\n"
        "Select a shape to draw:\n"
        "1. Square\n"
        "2. Rectangle\n"
        "3. Parallelogram\n"
        "4. Right-Angled Triangle\n"
        "5. Pyramid\n"
        "6. Exit"
    )

    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "6":
            print("Exiting the app. Goodbye!")
            break

        try:
            if choice == "1":
                width = int(input("Enter width of the square: ").strip())
                symbol = input("Enter a single printable symbol (non-whitespace): ").strip()
                result = art_generator.draw_square(width, symbol)
            elif choice == "2":
                width = int(input("Enter width of the rectangle: ").strip())
                height = int(input("Enter height of the rectangle: ").strip())
                symbol = input("Enter a single printable symbol (non-whitespace): ").strip()
                result = art_generator.draw_rectangle(width, height, symbol)
            elif choice == "3":
                width = int(input("Enter width of the parallelogram: ").strip())
                height = int(input("Enter height of the parallelogram: ").strip())
                symbol = input("Enter a single printable symbol (non-whitespace): ").strip()
                result = art_generator.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                width = int(input("Enter maximum width of the triangle (base length): ").strip())
                height = int(input("Enter height of the triangle: ").strip())
                symbol = input("Enter a single printable symbol (non-whitespace): ").strip()
                result = art_generator.draw_triangle(width, height, symbol)
            elif choice == "5":
                height = int(input("Enter height of the pyramid: ").strip())
                symbol = input("Enter a single printable symbol (non-whitespace): ").strip()
                result = art_generator.draw_pyramid(height, symbol)
            else:
                print("Invalid selection. Please choose a number between 1 and 6.\n")
                continue

            print("\nGenerated ASCII Art:")
            print(result)
        except ValueError as ve:
            print(f"Error: {ve}")

        print("\n" + "-" * 40 + "\n")

if __name__ == "__main__":
    main()
