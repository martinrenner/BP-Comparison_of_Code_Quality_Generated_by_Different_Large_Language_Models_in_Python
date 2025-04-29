#!/usr/bin/env python3
"""
Console-based 2D ASCII Art Application

This module provides a class, AsciiArt, that implements methods to draw various 
ASCII shapes: square, rectangle, parallelogram, right-angled triangle, and pyramid.
Each method validates its parameters and returns a multi-line string representing the shape.

Requirements: ISO/IEC 25010 compliant in terms of functionality, performance, modularity,
security, testability, and maintainability.
"""

from math import ceil


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    @staticmethod
    def _validate(symbol: str, width: int = None, height: int = None) -> None:
        """
        Validates the input parameters.

        Args:
            symbol (str): The character used for drawing; must be a single, non-whitespace character.
            width (int, optional): The horizontal dimension (width). Must be a positive integer if provided.
            height (int, optional): The vertical dimension (height). Must be a positive integer if provided.

        Raises:
            TypeError: If any parameter has the wrong type.
            ValueError: If any parameter has an invalid value.
        """
        # Validate symbol
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character.")

        # Validate dimensions (if provided)
        if width is not None:
            if not isinstance(width, int):
                raise TypeError("Width must be an integer.")
            if width <= 0:
                raise ValueError("Width must be a positive integer.")
        if height is not None:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer.")
            if height <= 0:
                raise ValueError("Height must be a positive integer.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a completely filled square.

        Args:
            width (int): The width of the square.
            symbol (str): A single printable character to fill the square.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is not a positive integer or symbol is invalid.
        """
        self._validate(symbol, width=width)
        row = symbol * width
        square_lines = [row for _ in range(width)]
        return "\n".join(square_lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled rectangle.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): A single printable character to fill the rectangle.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is not a positive integer or if symbol is invalid.
        """
        self._validate(symbol, width=width, height=height)
        row = symbol * width
        rectangle_lines = [row for _ in range(height)]
        return "\n".join(rectangle_lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled parallelogram. The figure grows diagonally to the right 
        by shifting each row one space compared to the previous row.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): A single printable character to fill the parallelogram.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height is not a positive integer or if symbol is invalid.
        """
        self._validate(symbol, width=width, height=height)
        lines = []
        for i in range(height):
            # Each row is shifted by i spaces to the right.
            line = (" " * i) + (symbol * width)
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally downward.
        The triangle is drawn with the right angle at the bottom-left: 
        the top row starts with a few symbols and the last row has 'width' symbols.
        The number of symbols per row is computed proportionally based on the given width and height.

        Args:
            width (int): The number of symbols in the base (last row) of the triangle.
            height (int): The total number of rows in the triangle.
            symbol (str): A single printable character to fill the triangle.

        Returns:
            str: A multi-line string representing the ASCII art triangle.

        Raises:
            ValueError: If width or height is not a positive integer or if symbol is invalid.
        """
        self._validate(symbol, width=width, height=height)
        lines = []
        prev_count = 0
        # For each row, compute the number of symbols using proportional scaling.
        for i in range(height):
            if i == height - 1:
                count = width  # Ensure the last row always has the full width.
            else:
                # Calculate the number based on the proportion of the row.
                count = ceil((i + 1) * width / height)
            # Guarantee monotonic increase in symbol count.
            if count <= prev_count:
                count = prev_count + 1
                count = min(count, width)
            lines.append(symbol * count)
            prev_count = count
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical, completely filled pyramid.

        The pyramid is centered using spaces. For a pyramid with the given height,
        the maximum width will be (2 * height - 1) characters.

        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): A single printable character to fill the pyramid.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is not a positive integer or if symbol is invalid.
        """
        self._validate(symbol, height=height)
        max_width = 2 * height - 1
        lines = []
        for i in range(height):
            # Determine the number of symbols for row i.
            n_symbols = 2 * i + 1
            line = symbol * n_symbols
            # Center the row within the maximum pyramid width.
            lines.append(line.center(max_width))
        return "\n".join(lines)


def main():
    """
    Main function to run the console-based ASCII Art application.
    Allows the user to choose a shape, input the dimensions and symbol,
    and then prints the generated ASCII art.
    """
    art_generator = AsciiArt()
    menu = (
        "\nPlease select a shape to draw:\n"
        "1. Square\n"
        "2. Rectangle\n"
        "3. Parallelogram\n"
        "4. Triangle (Right-angled, bottom-left right angle)\n"
        "5. Pyramid\n"
        "6. Exit\n"
        "Enter your choice (1-6): "
    )

    print("Welcome to the ASCII Art App!")

    while True:
        choice = input(menu).strip()
        if choice == "6":
            print("Exiting the app. Goodbye!")
            break

        try:
            if choice == "1":
                width = int(input("Enter width of the square: ").strip())
                symbol = input("Enter a single character symbol: ").strip()
                result = art_generator.draw_square(width, symbol)
            elif choice == "2":
                width = int(input("Enter width of the rectangle: ").strip())
                height = int(input("Enter height of the rectangle: ").strip())
                symbol = input("Enter a single character symbol: ").strip()
                result = art_generator.draw_rectangle(width, height, symbol)
            elif choice == "3":
                width = int(input("Enter width of the parallelogram: ").strip())
                height = int(input("Enter height of the parallelogram: ").strip())
                symbol = input("Enter a single character symbol: ").strip()
                result = art_generator.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                width = int(input("Enter base width of the triangle: ").strip())
                height = int(input("Enter height of the triangle: ").strip())
                symbol = input("Enter a single character symbol: ").strip()
                result = art_generator.draw_triangle(width, height, symbol)
            elif choice == "5":
                height = int(input("Enter height of the pyramid: ").strip())
                symbol = input("Enter a single character symbol: ").strip()
                result = art_generator.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
                continue

            print("\n" + result)
        except Exception as error:
            print(f"Error: {error}")


if __name__ == '__main__':
    main()
