class AsciiArt:
    """
    A class for generating 2D ASCII art for various shapes.
    
    Methods:
        draw_square(width: int, symbol: str) -> str
        draw_rectangle(width: int, height: int, symbol: str) -> str
        draw_parallelogram(width: int, height: int, symbol: str) -> str
        draw_triangle(width: int, height: int, symbol: str) -> str
        draw_pyramid(height: int, symbol: str) -> str
    """

    def _validate_dimensions(self, *dimensions: int) -> None:
        """
        Validates that all provided dimensions are positive integers.

        Args:
            dimensions (int): One or more dimension values (width, height).

        Raises:
            ValueError: If any dimension is not a positive integer.
            TypeError: If any dimension is not an integer.
        """
        for d in dimensions:
            if not isinstance(d, int):
                raise TypeError("Dimension must be an integer")
            if d <= 0:
                raise ValueError("Dimension must be a positive integer")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates that the symbol is a single non-whitespace character.

        Args:
            symbol (str): The character to be used for drawing.

        Raises:
            ValueError: If the symbol is not exactly one non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width using the specified symbol.

        Args:
            width (int): The width (and height) of the square.
            symbol (str): A single non-whitespace character to fill the square.

        Returns:
            str: A multi-line string representing the square.
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height using the specified symbol.

        Args:
            width (int): The horizontal dimension.
            height (int): The vertical dimension.
            symbol (str): A single non-whitespace character to fill the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified dimensions.
        Each row is shifted by one additional space to simulate a diagonal growth to the right.

        Args:
            width (int): The number of symbols per row.
            height (int): The number of rows.
            symbol (str): A single non-whitespace character to fill the shape.

        Returns:
            str: A multi-line string representing the parallelogram.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        lines = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        The triangle is drawn starting at the top-left corner; each subsequent row is indented by one space.
        The number of symbols per row decreases from the first row (having 'width' symbols) to the last row (at least 1 symbol).
        For height > 1, the decrement is linearly distributed.

        Args:
            width (int): The number of symbols in the first row.
            height (int): The total number of rows.
            symbol (str): A single non-whitespace character to fill the triangle.

        Returns:
            str: A multi-line string representing the right-angled triangle.

        Example (width=5, height=5, symbol='*'):
            *****
             ****
              ***
               **
                *
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        
        lines = []
        if height == 1:
            # Single row triangle.
            lines.append(symbol * width)
        else:
            # Compute a linear decrement ratio so that the first row has 'width' symbols 
            # and the last row has at least one symbol.
            ratio = (width - 1) / (height - 1)
            for i in range(height):
                # Use floor division of the decrement; ensure that at least one symbol is printed.
                count = width - int(i * ratio)
                if count < 1:
                    count = 1
                line = (" " * i) + (symbol * count)
                lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the specified height.
        The pyramid's base width is (2 * height - 1) and each row is centered.

        Args:
            height (int): The number of rows for the pyramid.
            symbol (str): A single non-whitespace character to fill the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.

        Example (height=4, symbol='#'):
              #
             ###
            #####
           #######
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)
        lines = []
        base_width = 2 * height - 1
        for i in range(height):
            num_symbols = 2 * i + 1
            num_spaces = (base_width - num_symbols) // 2
            # Only add left spaces; trailing spaces are not necessary.
            line = (" " * num_spaces) + (symbol * num_symbols)
            lines.append(line)
        return "\n".join(lines)


def main():
    """
    Main function for the console-based ASCII Art application.
    Presents a menu for the user to select a shape, 
    gathers input for dimensions and symbol, and then prints the resulting ASCII art.
    """
    ascii_art = AsciiArt()
    menu = (
        "\nSelect a shape to draw:\n"
        "1. Square\n"
        "2. Rectangle\n"
        "3. Parallelogram\n"
        "4. Right-angled Triangle\n"
        "5. Pyramid\n"
        "6. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "6":
            print("Exiting application.")
            break

        try:
            if choice == "1":
                width = int(input("Enter the width of the square: ").strip())
                symbol = input("Enter a printing symbol (single non-whitespace character): ").strip()
                art = ascii_art.draw_square(width, symbol)
            elif choice == "2":
                width = int(input("Enter the width of the rectangle: ").strip())
                height = int(input("Enter the height of the rectangle: ").strip())
                symbol = input("Enter a printing symbol (single non-whitespace character): ").strip()
                art = ascii_art.draw_rectangle(width, height, symbol)
            elif choice == "3":
                width = int(input("Enter the width of the parallelogram: ").strip())
                height = int(input("Enter the height of the parallelogram: ").strip())
                symbol = input("Enter a printing symbol (single non-whitespace character): ").strip()
                art = ascii_art.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                width = int(input("Enter the width of the triangle (symbols in the first row): ").strip())
                height = int(input("Enter the height of the triangle (number of rows): ").strip())
                symbol = input("Enter a printing symbol (single non-whitespace character): ").strip()
                art = ascii_art.draw_triangle(width, height, symbol)
            elif choice == "5":
                height = int(input("Enter the height of the pyramid: ").strip())
                symbol = input("Enter a printing symbol (single non-whitespace character): ").strip()
                art = ascii_art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please select a valid option (1-6).")
                continue

        except ValueError as ve:
            print(f"Input error: {ve}")
            continue
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            continue

        print("\nASCII Art:\n")
        print(art)
        print("\n" + "-" * 40)


if __name__ == "__main__":
    main()
