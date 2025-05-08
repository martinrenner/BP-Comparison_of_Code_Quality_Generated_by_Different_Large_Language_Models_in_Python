#!/usr/bin/env python3
"""
Console-based ASCII Art Drawer

This application provides functions for drawing ASCII shapes including a square,
rectangle, parallelogram, triangle, and pyramid. Each shape is generated using
the specified symbol, which must be a single, non-whitespace character.
"""

class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    Methods:
        draw_square(width: int, symbol: str) -> str
        draw_rectangle(width: int, height: int, symbol: str) -> str
        draw_parallelogram(width: int, height: int, symbol: str) -> str
        draw_triangle(width: int, height: int, symbol: str) -> str
        draw_pyramid(height: int, symbol: str) -> str
    """

    def _validate_dimensions(self, **dims) -> None:
        """
        Private helper to validate dimensions.

        Args:
            **dims: Arbitrary dimension names and their integer values.

        Raises:
            ValueError: If any provided dimension is not a positive integer.
        """
        for name, value in dims.items():
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name.capitalize()} must be a positive integer.")

    def _validate_symbol(self, symbol: str) -> None:
        """
        Private helper to validate the drawing symbol.

        Args:
            symbol (str): The symbol to be used for drawing.

        Raises:
            ValueError: If symbol is not a single, non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square with the given width.

        Args:
            width (int): The length of each side of the square.
            symbol (str): The character used to fill the square.

        Returns:
            str: A multi-line string representing the square.
        """
        self._validate_dimensions(width=width)
        self._validate_symbol(symbol)
        lines = []
        for _ in range(width):
            lines.append(symbol * width)
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle with the specified width and height.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character used to fill the rectangle.

        Returns:
            str: A multi-line string representing the rectangle.
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        lines = []
        for _ in range(height):
            lines.append(symbol * width)
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram that grows diagonally to the right.

        Each row is shifted by one space starting from the top-left corner.

        Args:
            width (int): The width of each row.
            height (int): The number of rows.
            symbol (str): The character used to fill the parallelogram.

        Returns:
            str: A multi-line string representing the parallelogram.
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with the right angle at the top-left.

        The triangle begins with a row of 'width' symbols and, with each subsequent row,
        it is indented by one additional space while the number of symbols decreases
        linearly (until at least one symbol is printed on the last row).

        Args:
            width (int): The number of symbols in the first row.
            height (int): The total number of rows in the triangle.
            symbol (str): The character used to fill the triangle.

        Returns:
            str: A multi-line string representing the triangle.
        """
        self._validate_dimensions(width=width, height=height)
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            if height == 1:
                count = width
            else:
                # Interpolate from `width` symbols on the first row to 1 symbol on the last row.
                count = round(width - (width - 1) * (row / (height - 1)))
            line = " " * row + symbol * count
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        The pyramid is centered horizontally, with the base having a width of (2 * height - 1).

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character used to fill the pyramid.

        Returns:
            str: A multi-line string representing the pyramid.
        """
        self._validate_dimensions(height=height)
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            num_symbols = 2 * row + 1
            num_spaces = height - row - 1
            line = " " * num_spaces + symbol * num_symbols
            lines.append(line)
        return "\n".join(lines)

def main():
    """
    Main function to run the ASCII Art application from the console.

    Provides a menu for selecting the type of shape to draw and prompts the user
    for the necessary parameters.
    """
    art = AsciiArt()
    menu = (
        "\nASCII Art Drawer\n"
        "1. Draw Square\n"
        "2. Draw Rectangle\n"
        "3. Draw Parallelogram\n"
        "4. Draw Triangle (Right-angled)\n"
        "5. Draw Pyramid\n"
        "6. Exit\n"
        "Enter your choice (1-6): "
    )

    while True:
        choice = input(menu).strip()
        if choice == "1":
            try:
                width = int(input("Enter the width of the square: "))
                symbol = input("Enter a single non-whitespace character symbol: ").strip()
                result = art.draw_square(width, symbol)
                print("\n" + result + "\n")
            except Exception as e:
                print("Error:", e)
        elif choice == "2":
            try:
                width = int(input("Enter the width of the rectangle: "))
                height = int(input("Enter the height of the rectangle: "))
                symbol = input("Enter a single non-whitespace character symbol: ").strip()
                result = art.draw_rectangle(width, height, symbol)
                print("\n" + result + "\n")
            except Exception as e:
                print("Error:", e)
        elif choice == "3":
            try:
                width = int(input("Enter the width of the parallelogram: "))
                height = int(input("Enter the height of the parallelogram: "))
                symbol = input("Enter a single non-whitespace character symbol: ").strip()
                result = art.draw_parallelogram(width, height, symbol)
                print("\n" + result + "\n")
            except Exception as e:
                print("Error:", e)
        elif choice == "4":
            try:
                width = int(input("Enter the number of symbols for the triangle's first row: "))
                height = int(input("Enter the height of the triangle: "))
                symbol = input("Enter a single non-whitespace character symbol: ").strip()
                result = art.draw_triangle(width, height, symbol)
                print("\n" + result + "\n")
            except Exception as e:
                print("Error:", e)
        elif choice == "5":
            try:
                height = int(input("Enter the height of the pyramid: "))
                symbol = input("Enter a single non-whitespace character symbol: ").strip()
                result = art.draw_pyramid(height, symbol)
                print("\n" + result + "\n")
            except Exception as e:
                print("Error:", e)
        elif choice == "6":
            print("Exiting the ASCII Art Drawer. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option (1-6).\n")

if __name__ == '__main__':
    main()
