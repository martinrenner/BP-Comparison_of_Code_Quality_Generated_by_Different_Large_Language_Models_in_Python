#!/usr/bin/env python3
"""
Console-based ASCII Art application.

This module provides an AsciiArt class with methods to generate various 2D ASCII shapes:
    - Square
    - Rectangle
    - Parallelogram (diagonally shifted)
    - Right-angled triangle (with linear growth from 1 symbol in the first row to full width in the last row)
    - Symmetrical pyramid

Each method validates its inputs (dimensions must be positive integers and the symbol must be a single, non‐whitespace character)
and returns a multi‐line string containing the ASCII art.
"""

from typing import Union


class AsciiArt:
    """Class to create various ASCII art shapes."""

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """Validate that a dimension is a positive integer.

        Args:
            value (int): The dimension value.
            name (str): The name of the dimension (e.g., "width", "height").

        Raises:
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name.capitalize()} must be a positive integer.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """Validate that the drawing symbol is a single, non-whitespace character.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            ValueError: If symbol is not a single character or is whitespace.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """Draw a filled square.

        Args:
            width (int): The side length of the square.
            symbol (str): A single, printable character used to draw the shape.

        Returns:
            str: A multi-line string representing the square.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)

        line = symbol * width
        square = "\n".join(line for _ in range(width))
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Draw a filled rectangle.

        Args:
            width (int): The number of characters in each row.
            height (int): The number of rows.
            symbol (str): A single, printable character used to draw the shape.

        Returns:
            str: A multi-line string representing the rectangle.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        line = symbol * width
        rectangle = "\n".join(line for _ in range(height))
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """Draw a filled parallelogram that shifts one space to the right each row.

        Args:
            width (int): The number of characters in each row.
            height (int): The number of rows.
            symbol (str): A single, printable character used to draw the shape.

        Returns:
            str: A multi-line string representing the parallelogram.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for row in range(height):
            # Each row is shifted to the right by the row index in spaces.
            line = " " * row + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """Draw a filled right-angled triangle.

        The triangle is left-aligned and its number of symbols per row grows linearly
        from 1 symbol in the first row to 'width' symbols in the last row.
        The left edge (first column) is always filled, forming a vertical side
        with the right angle located at the bottom-left.

        Args:
            width (int): The number of symbols in the triangle's base (last row).
            height (int): The total number of rows.
            symbol (str): A single, printable character used to draw the shape.
        
        Returns:
            str: A multi-line string representing the triangle.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        # When only one row, output the full width.
        if height == 1:
            lines.append(symbol * width)
        else:
            for row in range(height):
                # Linear interpolation: first row has 1 symbol, last row has width symbols.
                symbol_count = 1 + ((width - 1) * row) // (height - 1)
                lines.append(symbol * symbol_count)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """Draw a filled symmetrical pyramid.

        The pyramid is centered and each row has an odd number of symbols:
        row i contains 2*i + 1 symbols, padded by leading spaces to center it.

        Args:
            height (int): The number of rows of the pyramid.
            symbol (str): A single, printable character used to draw the shape.
        
        Returns:
            str: A multi-line string representing the pyramid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        base_width = 2 * height - 1
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = (base_width - num_symbols) // 2
            line = " " * num_spaces + symbol * num_symbols + " " * num_spaces
            lines.append(line)
        return "\n".join(lines)


def get_positive_int(prompt: str) -> int:
    """Prompt the user for a positive integer and return its value."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Value must be a positive integer. Please try again.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def get_symbol(prompt: str) -> str:
    """Prompt the user for a single, non-whitespace character."""
    while True:
        symbol = input(prompt)
        try:
            # Use the same validation as in AsciiArt class.
            AsciiArt._validate_symbol(symbol)
            return symbol
        except ValueError as e:
            print(e)


def main():
    """Main console application loop."""
    art = AsciiArt()
    menu = """
Select a shape to draw:
1. Square
2. Rectangle
3. Parallelogram
4. Right-angled Triangle
5. Pyramid
0. Exit
Enter your choice: """

    while True:
        choice = input(menu).strip()
        if choice == "0":
            print("Exiting the application.")
            break

        if choice not in {"1", "2", "3", "4", "5"}:
            print("Invalid option. Please try again.\n")
            continue

        try:
            if choice == "1":
                print("\nDraw a Square:")
                width = get_positive_int("Enter the side length (width): ")
                symbol = get_symbol("Enter a single drawing symbol: ")
                print("\n" + art.draw_square(width, symbol) + "\n")
            elif choice == "2":
                print("\nDraw a Rectangle:")
                width = get_positive_int("Enter the width: ")
                height = get_positive_int("Enter the height: ")
                symbol = get_symbol("Enter a single drawing symbol: ")
                print("\n" + art.draw_rectangle(width, height, symbol) + "\n")
            elif choice == "3":
                print("\nDraw a Parallelogram:")
                width = get_positive_int("Enter the width: ")
                height = get_positive_int("Enter the height: ")
                symbol = get_symbol("Enter a single drawing symbol: ")
                print("\n" + art.draw_parallelogram(width, height, symbol) + "\n")
            elif choice == "4":
                print("\nDraw a Right-angled Triangle:")
                width = get_positive_int("Enter the base width (number of symbols in the last row): ")
                height = get_positive_int("Enter the height (number of rows): ")
                symbol = get_symbol("Enter a single drawing symbol: ")
                print("\n" + art.draw_triangle(width, height, symbol) + "\n")
            elif choice == "5":
                print("\nDraw a Pyramid:")
                height = get_positive_int("Enter the height (number of rows): ")
                symbol = get_symbol("Enter a single drawing symbol: ")
                print("\n" + art.draw_pyramid(height, symbol) + "\n")
        except Exception as error:
            print(f"An error occurred: {error}\n")


if __name__ == "__main__":
    main()
