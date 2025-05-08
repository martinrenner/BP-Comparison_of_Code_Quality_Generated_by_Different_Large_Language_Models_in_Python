#!/usr/bin/env python3
"""
Console-based 2D ASCII ART App

This module provides an AsciiArt class that generates ASCII art for various shapes,
including square, rectangle, parallelogram, right-angled triangle, and pyramid.

Each function validates its inputs:
    - Dimensions (width, height) must be positive integers.
    - The drawing symbol must be a single non-whitespace character.

The generated shapes are completely filled with the chosen symbol.
"""

import math


class AsciiArt:
    """
    A class for generating filled ASCII art shapes.
    """

    @staticmethod
    def validate_symbol(symbol: str):
        """
        Validates that the provided symbol is a single non-whitespace character.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            ValueError: If the symbol is not exactly one non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    @staticmethod
    def validate_dimension(*dimensions):
        """
        Validates that all provided dimensions are positive integers.

        Args:
            *dimensions: One or more dimension values to validate.

        Raises:
            ValueError: If any dimension is not a positive integer.
        """
        for d in dimensions:
            if not isinstance(d, int) or d <= 0:
                raise ValueError("Dimensions must be positive integers.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of a given width using the provided symbol.

        Args:
            width (int): The width (and height) of the square.
            symbol (str): A single non-whitespace character to fill the square.

        Returns:
            str: A multi-line string representing the square.
        """
        self.validate_dimension(width)
        self.validate_symbol(symbol)
        return "\n".join([symbol * width for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of a given width and height using the provided symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): A single non-whitespace character to fill the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.
        """
        self.validate_dimension(width, height)
        self.validate_symbol(symbol)
        return "\n".join([symbol * width for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram of given width and height using the provided symbol.
        The parallelogram is slanted so that each row is indented by one additional space.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): A single non-whitespace character to fill the parallelogram.

        Returns:
            str: A multi-line string representing the parallelogram.
        """
        self.validate_dimension(width, height)
        self.validate_symbol(symbol)
        lines = []
        for i in range(height):
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle using the provided symbol.
        The triangle grows diagonally to the right, starting from the top-left corner.
        The number of symbols on row i is computed to scale from 1 symbol in the first row
        to 'width' symbols in the last row.

        Args:
            width (int): The base width of the triangle.
            height (int): The height of the triangle.
            symbol (str): A single non-whitespace character to fill the triangle.

        Returns:
            str: A multi-line string representing the triangle.
        """
        self.validate_dimension(width, height)
        self.validate_symbol(symbol)
        lines = []
        for i in range(height):
            # Compute the number of symbols for the current row (at least 1, with the last row having 'width' symbols)
            count = math.ceil((i + 1) * width / height)
            lines.append(symbol * count)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of a given height using the provided symbol.
        The pyramid's base width is (2 * height - 1), and each row is centered.

        Args:
            height (int): The height of the pyramid.
            symbol (str): A single non-whitespace character to fill the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.
        """
        self.validate_dimension(height)
        self.validate_symbol(symbol)
        lines = []
        for i in range(height):
            spaces = height - i - 1
            symbols_count = 2 * i + 1
            # Center the pyramid and remove trailing spaces for a clean look
            line = " " * spaces + symbol * symbols_count
            lines.append(line)
        return "\n".join(lines)


def main():
    """
    Main function to interact with the user and produce the desired ASCII art.
    It displays a menu, collects the required parameters from the user, and outputs the result.
    """
    art = AsciiArt()

    menu = """
Select a shape to draw:
1. Square
2. Rectangle
3. Parallelogram
4. Right-angled Triangle
5. Pyramid
6. Quit
"""
    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '6':
            print("Exiting the ASCII Art App. Goodbye!")
            break

        try:
            if choice == '1':  # Square
                width = int(input("Enter the width of the square: "))
                symbol = input("Enter a single non-whitespace character as symbol: ")
                result = art.draw_square(width, symbol)
            elif choice == '2':  # Rectangle
                width = int(input("Enter the width of the rectangle: "))
                height = int(input("Enter the height of the rectangle: "))
                symbol = input("Enter a single non-whitespace character as symbol: ")
                result = art.draw_rectangle(width, height, symbol)
            elif choice == '3':  # Parallelogram
                width = int(input("Enter the width of the parallelogram: "))
                height = int(input("Enter the height of the parallelogram: "))
                symbol = input("Enter a single non-whitespace character as symbol: ")
                result = art.draw_parallelogram(width, height, symbol)
            elif choice == '4':  # Right-angled Triangle
                width = int(input("Enter the base width of the triangle: "))
                height = int(input("Enter the height of the triangle: "))
                symbol = input("Enter a single non-whitespace character as symbol: ")
                result = art.draw_triangle(width, height, symbol)
            elif choice == '5':  # Pyramid
                height = int(input("Enter the height of the pyramid: "))
                symbol = input("Enter a single non-whitespace character as symbol: ")
                result = art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please select a valid option (1-6).")
                continue

            print("\nHere is your ASCII art:\n")
            print(result)
            print("\n" + "-" * 50 + "\n")

        except ValueError as ve:
            print(f"Input error: {ve}\nPlease try again.\n")
        except Exception as e:
            print(f"An unexpected error occurred: {e}\nPlease try again.\n")


if __name__ == "__main__":
    main()
