#!/usr/bin/env python3
"""
Console-based 2D ASCII ART Drawing App

This application allows users to draw various filled ASCII shapes
(square, rectangle, parallelogram, right-angled triangle, and pyramid)
using a user-selected printable symbol. Input values are validated to prevent
invalid or malicious inputs.

Each shape is generated as a multi-line string.
"""

import math


class AsciiArt:
    """
    A class to generate 2D ASCII art shapes.

    Methods:
        draw_square(width: int, symbol: str) -> str
        draw_rectangle(width: int, height: int, symbol: str) -> str
        draw_parallelogram(width: int, height: int, symbol: str) -> str
        draw_triangle(width: int, height: int, symbol: str) -> str
        draw_pyramid(height: int, symbol: str) -> str
    """

    @staticmethod
    def _validate_positive_int(value: int, name: str) -> None:
        """
        Validates that a given value is a positive integer.

        Args:
            value (int): The value to validate.
            name (str): The name of the parameter (for error messages).

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
            ValueError: If the symbol is not a single non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square with the specified width and symbol.

        Args:
            width (int): The width (and height) of the square.
            symbol (str): A single printable non-whitespace character.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If width is not positive or symbol is invalid.
        """
        self._validate_positive_int(width, "Width")
        self._validate_symbol(symbol)
        # A square is simply a rectangle with equal width and height.
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle with the specified width, height, and symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): A single printable non-whitespace character.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If width or height is not positive or symbol is invalid.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified width, height, and symbol.
        Each row is shifted by one space to the right relative to the previous row.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): A single printable non-whitespace character.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If width or height is not positive or symbol is invalid.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)
        lines = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally from the top-left corner.
        The triangle is "filled" such that the first row has 1 symbol and the last row
        (base) has exactly 'width' symbols. The triangle has exactly 'height' rows.
        
        The number of symbols in each row is determined by linear interpolation:
            n = round((i / (height - 1)) * (width - 1)) + 1, for row index i, 0 <= i < height.
        For height == 1, the triangle is a single row with 'width' symbols.
        
        Args:
            width (int): The number of symbols in the triangle's last row.
            height (int): The number of rows (height) of the triangle.
            symbol (str): A single printable non-whitespace character.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            ValueError: If width or height is not positive or symbol is invalid.
        """
        self._validate_positive_int(width, "Width")
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)

        lines = []
        if height == 1:
            lines.append(symbol * width)
        else:
            for i in range(height):
                # Linear interpolation ensures the first row has 1 symbol and
                # the last row has 'width' symbols.
                num_symbols = int(round((i / (height - 1)) * (width - 1))) + 1
                lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the specified height and symbol.
        The pyramid has a base width of (2 * height - 1) and is centered.

        Args:
            height (int): The height of the pyramid.
            symbol (str): A single printable non-whitespace character.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_positive_int(height, "Height")
        self._validate_symbol(symbol)

        lines = []
        base_width = 2 * height - 1
        for i in range(height):
            # Number of symbols increases by 2 every row: (2*i + 1)
            num_symbols = 2 * i + 1
            # Center the pyramid row within the base width.
            padding = (base_width - num_symbols) // 2
            lines.append(" " * padding + symbol * num_symbols)
        return "\n".join(lines)


def main():
    """
    Main interactive loop for the ASCII Art Drawing App.
    
    Presents a console-based menu, processes user input,
    validates parameters, and outputs the generated ASCII art.
    """
    art = AsciiArt()

    menu = (
        "\nASCII Art Drawing App\n"
        "-----------------------\n"
        "Select a shape to draw:\n"
        "1. Square\n"
        "2. Rectangle\n"
        "3. Parallelogram\n"
        "4. Right-Angled Triangle\n"
        "5. Pyramid\n"
        "6. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()

        try:
            if choice == "1":
                width = int(input("Enter the square width: "))
                symbol = input("Enter a single non-whitespace character for drawing: ").strip()
                result = art.draw_square(width, symbol)
            elif choice == "2":
                width = int(input("Enter the rectangle width: "))
                height = int(input("Enter the rectangle height: "))
                symbol = input("Enter a single non-whitespace character for drawing: ").strip()
                result = art.draw_rectangle(width, height, symbol)
            elif choice == "3":
                width = int(input("Enter the parallelogram width: "))
                height = int(input("Enter the parallelogram height: "))
                symbol = input("Enter a single non-whitespace character for drawing: ").strip()
                result = art.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                width = int(
                    input("Enter the triangle base width (number of symbols in the last row): ")
                )
                height = int(input("Enter the triangle height (number of rows): "))
                symbol = input("Enter a single non-whitespace character for drawing: ").strip()
                result = art.draw_triangle(width, height, symbol)
            elif choice == "5":
                height = int(input("Enter the pyramid height: "))
                symbol = input("Enter a single non-whitespace character for drawing: ").strip()
                result = art.draw_pyramid(height, symbol)
            elif choice == "6":
                print("Exiting the ASCII Art Drawing App. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 6.")
                continue

            print("\n" + result + "\n")
        except ValueError as error:
            print(f"Input error: {error}\n")
        except Exception as error:
            print(f"An unexpected error occurred: {error}\n")


if __name__ == "__main__":
    main()
