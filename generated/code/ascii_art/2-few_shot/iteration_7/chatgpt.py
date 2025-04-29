#!/usr/bin/env python3
"""
Console-based 2D ASCII Art Application

This module defines a class AsciiArt that generates various ASCII shapes,
including square, rectangle, parallelogram, right-angled triangle, and pyramid.
Each shape is completely filled with a user-selected symbol and validated
for proper dimensions and input parameters.

The application is designed with high-quality code practices meeting the
requirements specified in ISO/IEC 25010.
"""

import math


class AsciiArt:
    """
    A class to generate ASCII art shapes.
    """

    def __init__(self):
        """
        Initialize the AsciiArt object.
        Currently, no initialization parameters are required.
        """
        pass

    @staticmethod
    def _validate_dimension(name: str, value: int):
        """
        Validates that a given dimension (width/height) is a positive integer.

        Args:
            name (str): The name of the dimension (e.g., 'Width', 'Height').
            value (int): The numeric value of the dimension.

        Raises:
            ValueError: If the dimension is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    @staticmethod
    def _validate_symbol(symbol: str):
        """
        Validates that the symbol is a single non-whitespace character.

        Args:
            symbol (str): The symbol to be used for drawing.

        Raises:
            ValueError: If the symbol is not a single printable non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square with the given width, using the provided symbol.

        Args:
            width (int): The side length of the square.
            symbol (str): The symbol used to fill the shape.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If the width is not a positive integer or the symbol is invalid.
        """
        self._validate_dimension("Width", width)
        self._validate_symbol(symbol)

        # Each row of the square is a string with 'width' symbols.
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle with the given dimensions and symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol used to fill the shape.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If the dimensions are not positive integers or the symbol is invalid.
        """
        self._validate_dimension("Width", width)
        self._validate_dimension("Height", height)
        self._validate_symbol(symbol)

        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram that shifts to the right on each subsequent row.

        The shape grows diagonally to the right, starting from the top-left corner,
        with each row indented by an increasing number of spaces.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol used to fill the shape.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If the dimensions are not positive integers or the symbol is invalid.
        """
        self._validate_dimension("Width", width)
        self._validate_dimension("Height", height)
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Each row is indented by 'i' spaces.
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with a base width scaled to the given 'width'
        and with the specified 'height'. The triangle grows gradually, starting from
        a single symbol and increasing so that the bottom row contains exactly 'width' symbols.

        Args:
            width (int): The desired width of the triangle's base.
            height (int): The height of the triangle (number of rows).
            symbol (str): The symbol used to fill the shape.

        Returns:
            str: A multi-line string representing the right-angled triangle.

        Raises:
            ValueError: If the dimensions are not positive integers or the symbol is invalid.
        """
        self._validate_dimension("Width", width)
        self._validate_dimension("Height", height)
        self._validate_symbol(symbol)

        lines = []
        # Calculate the number of symbols per row such that the bottom row
        # exactly matches the specified width.
        for i in range(1, height + 1):
            # Use ceiling to ensure progressive growth resulting in exactly 'width' symbols at the base.
            num_symbols = math.ceil(i * width / height)
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid with the given height.

        Each row of the pyramid centers an odd number of symbols. The base width
        is calculated as (2 * height - 1).

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol used to fill the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If the height is not a positive integer or the symbol is invalid.
        """
        self._validate_dimension("Height", height)
        self._validate_symbol(symbol)

        lines = []
        base_width = 2 * height - 1
        for i in range(height):
            num_symbols = 2 * i + 1  # Odd number of symbols per row.
            # Calculate the left padding to center the pyramid row.
            spaces = (base_width - num_symbols) // 2
            # Build the line and remove trailing spaces for a cleaner output.
            line = " " * spaces + symbol * num_symbols
            lines.append(line)
        return "\n".join(lines)


def main():
    """
    Main function to run the console-based ASCII Art application.

    Users can select from a menu of shapes and provide the required dimensions and symbol.
    The selected shape is then generated and printed to the console.
    """
    art = AsciiArt()

    print("Welcome to the ASCII Art App!")
    print("------------------------------")
    print("Choose a shape to draw:")
    print("1. Square")
    print("2. Rectangle")
    print("3. Parallelogram")
    print("4. Right-angled Triangle")
    print("5. Pyramid")
    print("0. Exit")
    print("------------------------------")

    while True:
        try:
            choice = input("Enter your choice (0-5): ").strip()
            if choice == "0":
                print("Exiting the ASCII Art App. Goodbye!")
                break
            elif choice == "1":
                width = int(input("Enter the side length of the square: "))
                symbol = input("Enter a single printable symbol: ").strip()
                art_str = art.draw_square(width, symbol)
            elif choice == "2":
                width = int(input("Enter the width of the rectangle: "))
                height = int(input("Enter the height of the rectangle: "))
                symbol = input("Enter a single printable symbol: ").strip()
                art_str = art.draw_rectangle(width, height, symbol)
            elif choice == "3":
                width = int(input("Enter the width of the parallelogram: "))
                height = int(input("Enter the height of the parallelogram: "))
                symbol = input("Enter a single printable symbol: ").strip()
                art_str = art.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                width = int(input("Enter the base width of the triangle: "))
                height = int(input("Enter the height of the triangle: "))
                symbol = input("Enter a single printable symbol: ").strip()
                art_str = art.draw_triangle(width, height, symbol)
            elif choice == "5":
                height = int(input("Enter the height of the pyramid: "))
                symbol = input("Enter a single printable symbol: ").strip()
                art_str = art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please choose a valid option (0-5).\n")
                continue

            print("\nGenerated ASCII Art:\n")
            print(art_str)
            print("\n------------------------------\n")
        except ValueError as ve:
            print(f"Error: {ve}\n")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}\n")


if __name__ == "__main__":
    main()
