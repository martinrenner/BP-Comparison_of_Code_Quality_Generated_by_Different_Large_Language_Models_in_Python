#!/usr/bin/env python3
"""
Console-based 2D ASCII Art App

This application lets you draw several filled ASCII shapes on the console.
Shapes implemented:
  - Square
  - Rectangle
  - Parallelogram
  - Right-angled Triangle (grows diagonally from the top-left)
  - Pyramid (symmetrical)

Each shape is generated based on user input and validated against improper values.
The implementation follows OOP principles by encapsulating all drawing logic
inside the AsciiArt class. The code is structured to be modular, testable, and easy to maintain.
"""

import math


class AsciiArt:
    """
    Class for generating 2D ASCII art shapes.

    All shapes are completely filled with a chosen, validated symbol.
    """

    def __init__(self):
        """Initialize an AsciiArt instance (no internal state is required)."""
        pass

    @staticmethod
    def _validate_dimension(value: int, name: str):
        """
        Validate that a dimension (width or height) is a positive integer.

        Args:
            value (int): The dimension value to validate.
            name (str): The name of the dimension (for error messages).

        Raises:
            TypeError: If the value is not an integer.
            ValueError: If the value is not positive.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer, got {type(value).__name__}.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    @staticmethod
    def _validate_symbol(symbol: str):
        """
        Validate that the symbol is a single, non-whitespace printable character.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            TypeError: If symbol is not a string.
            ValueError: If symbol is not exactly one character or is a whitespace.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw and return a square as a multi-line string.

        Args:
            width (int): The side length of the square.
            symbol (str): The single character used to fill the square.

        Returns:
            str: A string representing the square.

        Raises:
            TypeError, ValueError: For invalid dimensions or symbol.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)
        line = symbol * width
        return "\n".join(line for _ in range(width))

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw and return a rectangle as a multi-line string.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The single character used to fill the rectangle.

        Returns:
            str: A string representing the rectangle.

        Raises:
            TypeError, ValueError: For invalid dimensions or symbol.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        line = symbol * width
        return "\n".join(line for _ in range(height))

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw and return a parallelogram as a multi-line string.
        The shape grows diagonally to the right by adding one leading space each row.

        Args:
            width (int): The number of symbols in each row.
            height (int): The number of rows.
            symbol (str): The single character used to fill the shape.

        Returns:
            str: A string representing the parallelogram.

        Raises:
            TypeError, ValueError: For invalid dimensions or symbol.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # Each row is shifted right by i spaces.
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw and return a right-angled triangle as a multi-line string.
        The triangle grows diagonally from the top-left corner.
        It has 'height' rows and its base (last row) has exactly 'width' symbols.
        The number of symbols per row is computed via linear interpolation so that:
          - The first row has 1 symbol.
          - The last row has 'width' symbols.
          - Intermediate rows increase gradually.

        Args:
            width (int): The number of symbols in the triangle's base.
            height (int): The total number of rows.
            symbol (str): The single character used to fill the triangle.

        Returns:
            str: A string representing the triangle.

        Raises:
            TypeError, ValueError: For invalid dimensions or symbol.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        lines = []
        if height == 1:
            # Only one row; use the full width.
            lines.append(symbol * width)
        else:
            for i in range(height):
                if i == height - 1:
                    # Ensure the base row has exactly 'width' symbols.
                    count = width
                else:
                    # Linear interpolation: scale from 1 up to width.
                    # Using the formula: count = int(i * (width - 1) / (height - 1)) + 1
                    count = int(i * (width - 1) / (height - 1)) + 1
                lines.append(symbol * count)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw and return a symmetrical pyramid as a multi-line string.
        The pyramid has 'height' rows and a base width of (2 * height - 1) symbols.
        Each row is centered by adding appropriate leading spaces.

        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): The single character used to build the pyramid.

        Returns:
            str: A string representing the pyramid.

        Raises:
            TypeError, ValueError: For invalid height or symbol.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # Calculate leading spaces to center the pyramid.
            spaces = height - i - 1
            symbols_count = 2 * i + 1
            line = " " * spaces + symbol * symbols_count
            lines.append(line)
        return "\n".join(lines)


def main():
    """
    Main routine for the console-based ASCII Art app.
    Presents a menu to the user to select and draw a shape.
    """
    art = AsciiArt()
    menu = (
        "\nASCII Art Drawing App\n"
        "-----------------------\n"
        "1. Draw Square\n"
        "2. Draw Rectangle\n"
        "3. Draw Parallelogram\n"
        "4. Draw Triangle\n"
        "5. Draw Pyramid\n"
        "6. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "6":
            print("Exiting the ASCII Art app. Goodbye!")
            break

        try:
            if choice == "1":
                width = int(input("Enter the side length of the square: ").strip())
                symbol = input("Enter a symbol (single non-whitespace character): ").strip()
                result = art.draw_square(width, symbol)
            elif choice == "2":
                width = int(input("Enter the width of the rectangle: ").strip())
                height = int(input("Enter the height of the rectangle: ").strip())
                symbol = input("Enter a symbol (single non-whitespace character): ").strip()
                result = art.draw_rectangle(width, height, symbol)
            elif choice == "3":
                width = int(input("Enter the width of the parallelogram: ").strip())
                height = int(input("Enter the height of the parallelogram: ").strip())
                symbol = input("Enter a symbol (single non-whitespace character): ").strip()
                result = art.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                width = int(input("Enter the base width of the triangle: ").strip())
                height = int(input("Enter the height of the triangle: ").strip())
                symbol = input("Enter a symbol (single non-whitespace character): ").strip()
                result = art.draw_triangle(width, height, symbol)
            elif choice == "5":
                height = int(input("Enter the height of the pyramid: ").strip())
                symbol = input("Enter a symbol (single non-whitespace character): ").strip()
                result = art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please select an option from 1 to 6.")
                continue

            print("\nGenerated ASCII Art:\n")
            print(result)
            print("\n")
        except (ValueError, TypeError) as error:
            print(f"\nInput error: {error}\nPlease try again.\n")


if __name__ == "__main__":
    main()
