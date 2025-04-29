#!/usr/bin/env python3
"""
Console-based 2D ASCII ART application.

This module provides an AsciiArt class with methods to draw various 2D shapes
using ASCII characters. The shapes include a square, rectangle, parallelogram,
right-angled triangle, and symmetrical pyramid. Each shape is completely filled
with the user‐chosen symbol.

The code validates inputs (e.g., positive dimensions, single non‐whitespace printable symbol)
and adheres to software quality standards according to ISO/IEC 25010.
"""

class AsciiArt:
    """
    A class for generating ASCII art shapes.
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
            if not isinstance(dim, int) or dim <= 0:
                raise ValueError("Dimensions must be positive integers.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validates the chosen symbol.

        The symbol must be a string, exactly one character long,
        non-whitespace, and printable.

        Args:
            symbol (str): The symbol to be used in drawing.

        Raises:
            ValueError: If the symbol is invalid.
        """
        if not isinstance(symbol, str):
            raise ValueError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace() or not symbol.isprintable():
            raise ValueError("Symbol must be a non-whitespace printable character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width using the specified symbol.

        Args:
            width (int): The width (and height) of the square.
            symbol (str): A single non-whitespace character to fill the square.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If width is not a positive integer or symbol is invalid.
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)

        # Build each row as a string of repeated symbols and join rows with newline.
        rows = [symbol * width for _ in range(width)]
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height using the given symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): A single non-whitespace character to fill the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If width/height are not positive integers or symbol is invalid.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        rows = [symbol * width for _ in range(height)]
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram that grows diagonally to the right.

        Each row is shifted by one additional space compared to the previous row.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height (number of rows) of the parallelogram.
            symbol (str): A single non-whitespace character to fill the shape.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If width/height are not positive integers or symbol is invalid.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        rows = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with the right angle at the top-left corner.

        The triangle grows diagonally to the right. The first row has a single symbol,
        and the last row contains exactly 'width' symbols. Intermediate rows are scaled
        linearly using the formula:
            n_symbols = ((width - 1) * i) // (height - 1) + 1
        for rows i in [0, height-1]. For the degenerate case when height is 1,
        the single row will have 'width' symbols.

        Args:
            width (int): The number of symbols in the base (last row) of the triangle.
            height (int): The number of rows (vertical size) of the triangle.
            symbol (str): A single non-whitespace character to fill the triangle.

        Returns:
            str: A multi-line string representing the right-angled triangle.

        Raises:
            ValueError: If width/height are not positive integers or symbol is invalid.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        rows = []
        if height == 1:
            # If there's only one row, simply print the base.
            rows.append(symbol * width)
        else:
            for i in range(height):
                # Compute the number of symbols in row i.
                # This formula ensures the first row has 1 symbol and the last row has width symbols.
                n_symbols = ((width - 1) * i) // (height - 1) + 1
                rows.append(symbol * n_symbols)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the specified height.

        The pyramid has a base width of (2*height - 1) symbols, and each row is centered.

        Args:
            height (int): The number of rows (vertical height) of the pyramid.
            symbol (str): A single non-whitespace character to fill the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If height is not a positive integer or symbol is invalid.
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)

        pyramid_lines = []
        base_width = 2 * height - 1  # Total width of the pyramid's base.
        for i in range(height):
            n_symbols = 2 * i + 1
            n_spaces = height - i - 1
            line = (" " * n_spaces) + (symbol * n_symbols)
            pyramid_lines.append(line)
        return "\n".join(pyramid_lines)


def main():
    """
    Main function providing a simple console-based interface for ASCII Art drawing.
    The user can select from various shapes and input corresponding dimensions and the symbol.
    """
    art = AsciiArt()
    menu = (
        "\nASCII Art Generator Menu:\n"
        "1. Draw Square\n"
        "2. Draw Rectangle\n"
        "3. Draw Parallelogram\n"
        "4. Draw Triangle (Right-Angled, Top-Left)\n"
        "5. Draw Pyramid\n"
        "6. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()
        try:
            if choice == "1":
                width = int(input("Enter the width of the square: "))
                symbol = input("Enter a symbol (a single non-whitespace character): ").strip()
                print("\n" + art.draw_square(width, symbol))
            elif choice == "2":
                width = int(input("Enter the width of the rectangle: "))
                height = int(input("Enter the height of the rectangle: "))
                symbol = input("Enter a symbol (a single non-whitespace character): ").strip()
                print("\n" + art.draw_rectangle(width, height, symbol))
            elif choice == "3":
                width = int(input("Enter the width of the parallelogram: "))
                height = int(input("Enter the height of the parallelogram: "))
                symbol = input("Enter a symbol (a single non-whitespace character): ").strip()
                print("\n" + art.draw_parallelogram(width, height, symbol))
            elif choice == "4":
                width = int(input("Enter the base width of the triangle: "))
                height = int(input("Enter the height (number of rows) of the triangle: "))
                symbol = input("Enter a symbol (a single non-whitespace character): ").strip()
                print("\n" + art.draw_triangle(width, height, symbol))
            elif choice == "5":
                height = int(input("Enter the height of the pyramid: "))
                symbol = input("Enter a symbol (a single non-whitespace character): ").strip()
                print("\n" + art.draw_pyramid(height, symbol))
            elif choice == "6":
                print("Exiting ASCII Art Generator. Goodbye!")
                break
            else:
                print("Invalid choice. Please select an option between 1 and 6.")
        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
