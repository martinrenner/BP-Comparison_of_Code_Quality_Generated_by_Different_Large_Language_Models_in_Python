#!/usr/bin/env python3
"""
Console-based 2D ASCII Art application.

This module defines the AsciiArt class which provides methods to draw various ASCII art shapes
(square, rectangle, parallelogram, right-angled triangle, and pyramid). It also includes a simple
console interface to interact with the user.

Each drawing method returns a multi-line string representing the ASCII art. Input validation is
performed to ensure dimensions are positive integers and the symbol is a single, non‐whitespace character.

Author: Senior Software Developer
"""

import math


class AsciiArt:
    """
    A class for generating ASCII art shapes.

    The class provides methods to draw:
      - A square (draw_square)
      - A rectangle (draw_rectangle)
      - A parallelogram (draw_parallelogram)
      - A right-angled triangle (draw_triangle)
      - A symmetrical pyramid (draw_pyramid)
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a filled square of a given width using the specified symbol.

        Args:
            width (int): The number of symbols per side.
            symbol (str): A single non-whitespace character used for drawing.

        Returns:
            str: Multi-line string representing the square.

        Raises:
            TypeError: If width is not an integer or symbol is not a string.
            ValueError: If width is <= 0, or if symbol is not a single non-whitespace character.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)

        row = symbol * width
        # Create a list with 'width' identical rows and join them using newline.
        square = "\n".join(row for _ in range(width))
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled rectangle of given width and height using the specified symbol.

        Args:
            width (int): The number of symbols per row.
            height (int): The number of rows.
            symbol (str): A single non-whitespace character used for drawing.

        Returns:
            str: Multi-line string representing the rectangle.

        Raises:
            TypeError: If width/height is not an integer or symbol is not a string.
            ValueError: If width or height is <= 0, or if symbol is not a single non-whitespace character.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        row = symbol * width
        rectangle = "\n".join(row for _ in range(height))
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled parallelogram of given width and height using the specified symbol.

        The parallelogram is drawn such that each row is shifted one space to the right relative to the
        previous row, starting from the top-left corner.

        Args:
            width (int): The number of symbols per row.
            height (int): The number of rows.
            symbol (str): A single non-whitespace character used for drawing.

        Returns:
            str: Multi-line string representing the parallelogram.

        Raises:
            TypeError: If width/height is not an integer or symbol is not a string.
            ValueError: If width or height is <= 0, or if symbol is not a single non-whitespace character.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Each row is shifted i spaces and then filled with the symbol repeating 'width' times.
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a filled right-angled triangle using the specified symbol.

        The triangle is drawn with the right-angle at the bottom-left and is anchored at the top-left of the console.
        It has 'height' rows and its bottom row contains exactly 'width' symbols. The number of symbols increases
        each row proportionally.

        Args:
            width (int): The desired number of symbols in the bottom row.
            height (int): The number of rows in the triangle.
            symbol (str): A single non-whitespace character used for drawing.

        Returns:
            str: Multi-line string representing the right-angled triangle.

        Raises:
            TypeError: If width/height is not an integer or symbol is not a string.
            ValueError: If width or height is <= 0, or if symbol is not a single non-whitespace character.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Calculate the number of symbols for the current row.
            # math.ceil ensures that at least one symbol appears and the bottom row exactly equals 'width'.
            num_symbols = math.ceil((i + 1) * width / height)
            line = symbol * num_symbols
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid with the specified height using the given symbol.

        The pyramid has a centered structure with a base width of (2 * height - 1) symbols.

        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): A single non-whitespace character used for drawing.

        Returns:
            str: Multi-line string representing the pyramid.

        Raises:
            TypeError: If height is not an integer or symbol is not a string.
            ValueError: If height is <= 0, or if symbol is not a single non-whitespace character.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Compute the number of leading spaces to center the pyramid.
            spaces = " " * (height - i - 1)
            # The number of symbols follows an odd number sequence: 1, 3, 5, ...
            symbols = symbol * (2 * i + 1)
            # Trailing spaces are optional; here they are not necessary.
            line = spaces + symbols
            lines.append(line)
        return "\n".join(lines)

    @staticmethod
    def _validate_symbol(symbol: str):
        """
        Validate that the provided symbol is a single non-whitespace character.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            TypeError: If symbol is not a string.
            ValueError: If symbol is not exactly one character or if it is a whitespace.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    @staticmethod
    def _validate_dimension(value: int, name: str):
        """
        Validate that a dimension (width or height) is a positive integer.

        Args:
            value (int): The dimension value to validate.
            name (str): The name of the dimension (used for error messages).

        Raises:
            TypeError: If the provided value is not an integer.
            ValueError: If the value is not greater than 0.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name.capitalize()} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name.capitalize()} must be greater than 0.")


def main():
    """
    Main function to run the interactive console-based ASCII Art application.
    """
    art = AsciiArt()

    menu = (
        "\nChoose a shape to draw:\n"
        "1. Square\n"
        "2. Rectangle\n"
        "3. Parallelogram\n"
        "4. Triangle (right-angled)\n"
        "5. Pyramid\n"
        "6. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "6":
            print("Exiting the application.")
            break

        try:
            if choice == "1":
                width = int(input("Enter the width of the square: ").strip())
                symbol = input("Enter the symbol to use: ").strip()
                print("\n" + art.draw_square(width, symbol) + "\n")
            elif choice == "2":
                width = int(input("Enter the width of the rectangle: ").strip())
                height = int(input("Enter the height of the rectangle: ").strip())
                symbol = input("Enter the symbol to use: ").strip()
                print("\n" + art.draw_rectangle(width, height, symbol) + "\n")
            elif choice == "3":
                width = int(input("Enter the width of the parallelogram: ").strip())
                height = int(input("Enter the height of the parallelogram: ").strip())
                symbol = input("Enter the symbol to use: ").strip()
                print("\n" + art.draw_parallelogram(width, height, symbol) + "\n")
            elif choice == "4":
                width = int(input("Enter the width (base) of the triangle: ").strip())
                height = int(input("Enter the height of the triangle: ").strip())
                symbol = input("Enter the symbol to use: ").strip()
                print("\n" + art.draw_triangle(width, height, symbol) + "\n")
            elif choice == "5":
                height = int(input("Enter the height of the pyramid: ").strip())
                symbol = input("Enter the symbol to use: ").strip()
                print("\n" + art.draw_pyramid(height, symbol) + "\n")
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except (ValueError, TypeError) as error:
            # Display error message and continue the loop.
            print(f"Error: {error}. Please try again.")


if __name__ == "__main__":
    main()
