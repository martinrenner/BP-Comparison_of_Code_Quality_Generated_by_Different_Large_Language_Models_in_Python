#!/usr/bin/env python3
"""
Console-based 2D ASCII Art Application

This module implements the AsciiArt class that provides methods to create various
ASCII art shapes. The available shapes include:
    - Square
    - Rectangle
    - Parallelogram (diagonally shifted per row)
    - Right-angled Triangle (growing from the top-left corner)
    - Symmetrical Pyramid

Each shape is completely filled with a user-specified symbol (only one printable,
non-whitespace character is allowed).

The application validates all dimensions and symbols, ensuring they are valid
inputs. The code is structured using an object-oriented approach for increased
modularity, testability, and maintainability.
"""

import math


class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.
    
    Methods:
        draw_square(width: int, symbol: str) -> str
        draw_rectangle(width: int, height: int, symbol: str) -> str
        draw_parallelogram(width: int, height: int, symbol: str) -> str
        draw_triangle(width: int, height: int, symbol: str) -> str
        draw_pyramid(height: int, symbol: str) -> str
    """

    def __init__(self):
        # Currently no state is maintained.
        pass

    def _validate_dimension(self, *dimensions: int):
        """
        Validate that all dimension values are positive integers.

        Args:
            *dimensions (int): One or more dimension values (width, height)

        Raises:
            ValueError: If any provided dimension is not a positive integer.
        """
        for d in dimensions:
            if not isinstance(d, int) or d <= 0:
                raise ValueError(f"Dimensions must be positive integers. Received: {d}")

    def _validate_symbol(self, symbol: str):
        """
        Validate that the symbol input is a single, non-whitespace character.

        Args:
            symbol (str): The symbol to be used in drawing the shape.

        Raises:
            ValueError: If the symbol is not a single non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError(f"Symbol must be a single non-whitespace character. Received: {symbol}")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.

        Args:
            width (int): The length of each side of the square.
            symbol (str): The character used to fill the square.

        Returns:
            str: A multi-line string representing the square.
        """
        self._validate_dimension(width)
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character used to fill the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.
        """
        self._validate_dimension(width, height)
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram that shifts one space to the right each row.

        Each row starts with an increasing number of spaces, followed by a row of symbols.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character used to fill the parallelogram.

        Returns:
            str: A multi-line string representing the parallelogram.
        """
        self._validate_dimension(width, height)
        self._validate_symbol(symbol)
        lines = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally from the top-left corner.

        The number of symbols in each row scales linearly from 1 (first row) to
        'width' (last row). If height is 1, the row will contain 'width' symbols.

        Args:
            width (int): The maximum width (base) of the triangle.
            height (int): The height (number of rows) of the triangle.
            symbol (str): The character used to fill the triangle.

        Returns:
            str: A multi-line string representing the triangle.
        """
        self._validate_dimension(width, height)
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # For a triangle with more than one row, compute the number of symbols for this row.
            count = width if height == 1 else math.ceil((i + 1) * width / height)
            lines.append(symbol * count)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.

        The pyramid is centered by adding leading spaces such that the widest
        row (base) is exactly centered.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character used to fill the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.
        """
        self._validate_dimension(height)
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # Calculate the number of leading spaces and symbols for the current row.
            leading_spaces = " " * (height - i - 1)
            symbol_count = 2 * i + 1
            lines.append(leading_spaces + symbol * symbol_count)
        return "\n".join(lines)


def main():
    """
    Interactive main function for the console-based ASCII Art app.

    Presents a menu of shape options to the user, reads input parameters,
    generates the requested ASCII art using the AsciiArt class, and prints it.
    """
    art_creator = AsciiArt()
    menu = """
ASCII Art Menu:
1. Draw Square
2. Draw Rectangle
3. Draw Parallelogram
4. Draw Right-Angled Triangle
5. Draw Pyramid
6. Exit
"""
    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            try:
                width = int(input("Enter side length for the square: ").strip())
                symbol = input("Enter a single non-whitespace character as the symbol: ").strip()
                result = art_creator.draw_square(width, symbol)
                print("\n" + result + "\n")
            except ValueError as e:
                print("Error:", e)
        elif choice == "2":
            try:
                width = int(input("Enter width of the rectangle: ").strip())
                height = int(input("Enter height of the rectangle: ").strip())
                symbol = input("Enter a single non-whitespace character as the symbol: ").strip()
                result = art_creator.draw_rectangle(width, height, symbol)
                print("\n" + result + "\n")
            except ValueError as e:
                print("Error:", e)
        elif choice == "3":
            try:
                width = int(input("Enter width of the parallelogram: ").strip())
                height = int(input("Enter height of the parallelogram: ").strip())
                symbol = input("Enter a single non-whitespace character as the symbol: ").strip()
                result = art_creator.draw_parallelogram(width, height, symbol)
                print("\n" + result + "\n")
            except ValueError as e:
                print("Error:", e)
        elif choice == "4":
            try:
                width = int(input("Enter the maximum width (base) of the triangle: ").strip())
                height = int(input("Enter the height (number of rows) of the triangle: ").strip())
                symbol = input("Enter a single non-whitespace character as the symbol: ").strip()
                result = art_creator.draw_triangle(width, height, symbol)
                print("\n" + result + "\n")
            except ValueError as e:
                print("Error:", e)
        elif choice == "5":
            try:
                height = int(input("Enter the height of the pyramid: ").strip())
                symbol = input("Enter a single non-whitespace character as the symbol: ").strip()
                result = art_creator.draw_pyramid(height, symbol)
                print("\n" + result + "\n")
            except ValueError as e:
                print("Error:", e)
        elif choice == "6":
            print("Thank you for using the ASCII Art App. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 6.")


if __name__ == "__main__":
    main()
