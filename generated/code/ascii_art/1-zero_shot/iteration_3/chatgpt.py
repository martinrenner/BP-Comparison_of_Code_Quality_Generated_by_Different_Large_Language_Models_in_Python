"""
Console-based 2D ASCII ART application.

This module defines the AsciiArt class that implements several functions for drawing
filled ASCII shapes: square, rectangle, parallelogram, right-angled triangle, and pyramid.

Each function validates its inputs and returns a multi‐line string with the ASCII art.
The application also provides a simple console menu to let the user choose a shape and
its parameters.

Requirements (ISO/IEC 25010 compliant):
    • Functionality: Implements drawing functions for the five shapes.
    • Correctness & Performance: Uses straightforward looping and string‐joining.
    • Modularity: Organized as an OOP class with helper validation methods.
    • Security: Validates inputs using built-in error types.
    • Testability: Each method returns a string and can be easily tested.
    • Readability & Documentation: Includes type hints, docstrings, and clear variable names.
"""

import math


class AsciiArt:
    """
    A class for generating 2D ASCII art for various shapes.
    """

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validate that a given dimension is a positive integer.

        :param value: The dimension value.
        :param name: Name of the parameter (for error messages).
        :raises ValueError: If the value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer. Got: {value}.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the symbol is a single non-whitespace character.

        :param symbol: The symbol string.
        :raises ValueError: If the symbol is not exactly one printable, non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square using the specified symbol.

        :param width: The side length of the square.
        :param symbol: A single non-whitespace character to fill the square.
        :return: A multi-line string representing the square.
        :raises ValueError: For invalid width or symbol.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)

        # Create each row as a string of repeated symbols and join with newline.
        rows = [symbol * width for _ in range(width)]
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle using the specified symbol.

        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        :param symbol: A single non-whitespace character to fill the rectangle.
        :return: A multi-line string representing the rectangle.
        :raises ValueError: For invalid width, height, or symbol.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows = [symbol * width for _ in range(height)]
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that shifts one space to the right in each subsequent row.

        :param width: The width of the parallelogram.
        :param height: The height (number of rows) of the parallelogram.
        :param symbol: A single non-whitespace character to fill the shape.
        :return: A multi-line string representing the parallelogram.
        :raises ValueError: For invalid width, height, or symbol.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        # Each row is shifted to the right by a number of spaces equal to its row index.
        rows = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle that grows diagonally to the right.

        The triangle is constructed row by row, with the number of symbols in each row
        computed via linear interpolation so that the last row exactly has 'width' symbols.
        If the computed symbol count is less than 1, at least one symbol is printed per row.

        :param width: The desired width of the triangle's base (last row).
        :param height: The total number of rows in the triangle.
        :param symbol: A single non-whitespace character to fill the triangle.
        :return: A multi-line string representing the triangle.
        :raises ValueError: For invalid width, height, or symbol.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        rows = []
        for row in range(height):
            # Calculate the number of symbols for the current row using math.ceil.
            num_symbols = math.ceil((row + 1) * width / height)
            # Ensure at least one symbol per row.
            num_symbols = max(1, num_symbols)
            rows.append(symbol * num_symbols)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical filled pyramid centered horizontally.

        The pyramid has 'height' rows; the i-th row (0-indexed) contains (2*i + 1) symbols,
        padded on the left with spaces so that the pyramid is centered.

        :param height: The height (number of rows) of the pyramid.
        :param symbol: A single non-whitespace character to fill the pyramid.
        :return: A multi-line string representing the pyramid.
        :raises ValueError: For invalid height or symbol.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        pyramid_width = 2 * height - 1  # Maximum width of the pyramid.
        rows = []
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = (pyramid_width - num_symbols) // 2
            rows.append(" " * num_spaces + symbol * num_symbols)
        return "\n".join(rows)


def main():
    """
    Runs the interactive console-based ASCII art application.

    The user is presented with a menu to select a shape, enter the required parameters,
    and the resulting ASCII art is printed to the console.
    """
    art = AsciiArt()

    menu = (
        "\nASCII Art Generator\n"
        "-------------------\n"
        "1. Square\n"
        "2. Rectangle\n"
        "3. Parallelogram\n"
        "4. Right-angled Triangle\n"
        "5. Pyramid\n"
        "6. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Select a shape (1-6): ").strip()

        if choice == "6":
            print("Exiting ASCII Art Generator. Goodbye!")
            break

        try:
            # For shapes that require width and height.
            if choice in {"1", "2", "3", "4"}:
                width_input = input("Enter width (positive integer): ").strip()
                width = int(width_input)
            if choice in {"2", "3", "4"}:
                height_input = input("Enter height (positive integer): ").strip()
                height = int(height_input)
            # For pyramid, only height is needed.
            if choice == "5":
                height_input = input("Enter height (positive integer): ").strip()
                height = int(height_input)

            symbol = input("Enter a symbol (a single non-whitespace character): ").strip()
            if len(symbol) != 1:
                raise ValueError("Symbol must be exactly one character and not whitespace.")

            if choice == "1":
                result = art.draw_square(width, symbol)
            elif choice == "2":
                result = art.draw_rectangle(width, height, symbol)
            elif choice == "3":
                result = art.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                result = art.draw_triangle(width, height, symbol)
            elif choice == "5":
                result = art.draw_pyramid(height, symbol)
            else:
                print("Invalid selection. Please choose a valid option.")
                continue

            print("\nGenerated ASCII Art:")
            print(result)
        except ValueError as err:
            print(f"Input error: {err}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")


if __name__ == '__main__':
    main()
