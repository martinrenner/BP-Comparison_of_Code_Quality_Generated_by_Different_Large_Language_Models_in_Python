"""
Console-based 2D ASCII Art Application

This module defines the AsciiArt class that implements functions to draw various
ASCII shapes including a square, rectangle, parallelogram, right-angled triangle,
and symmetrical pyramid. The application validates inputs to ensure dimensions
are positive integers and the symbol is a printable, single non‐whitespace character.

Usage:
    Run this module directly to launch an interactive console-based menu.
    Alternatively, import AsciiArt from this module in your own code.
"""

import math


class AsciiArt:
    """
    A class for drawing 2D ASCII art shapes.
    """

    def __init__(self) -> None:
        """
        Initialize an AsciiArt instance.
        No state is maintained in this implementation.
        """
        pass

    def _validate_symbol(self, symbol: str) -> None:
        """
        Validate that the symbol is a string of length one and is not whitespace.
        
        Args:
            symbol (str): The symbol to use for drawing.
        
        Raises:
            TypeError: If symbol is not a string.
            ValueError: If symbol is not exactly one character or is whitespace.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be of type str")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character")
        if symbol.isspace():
            raise ValueError("Symbol must not be a whitespace character")

    def _validate_dimension(self, **dims) -> None:
        """
        Validate that each provided dimension is a positive integer.
        
        Args:
            **dims: Arbitrary keyword dimensions (e.g. width=5, height=3).
        
        Raises:
            ValueError: If any dimension is not a positive integer.
        """
        for name, value in dims.items():
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square with the given side length using the specified symbol.

        Args:
            width (int): The side length of the square.
            symbol (str): The printable symbol to fill the square.

        Returns:
            str: A multi-line string representing the drawn square.

        Raises:
            ValueError: If width is not positive or symbol is invalid.
        """
        self._validate_dimension(width=width)
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle with the given width and height using the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The printable symbol to fill the rectangle.

        Returns:
            str: A multi-line string representing the drawn rectangle.
        """
        self._validate_dimension(width=width, height=height)
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram with the given width and height using the specified symbol.
        Each subsequent row is indented by one additional space to create a diagonal effect.

        Args:
            width (int): The width of the shape.
            height (int): The height of the shape.
            symbol (str): The printable symbol to fill the parallelogram.

        Returns:
            str: A multi-line string representing the drawn parallelogram.
        """
        self._validate_dimension(width=width, height=height)
        self._validate_symbol(symbol)
        lines = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle that grows diagonally to the right.
        The triangle has 'height' rows and the number of symbols in the last row
        equals 'width'. The number of symbols in each row is scaled proportionally.

        Args:
            width (int): The maximum number of symbols (base width) for the triangle.
            height (int): The number of rows in the triangle.
            symbol (str): The printable symbol to fill the triangle.

        Returns:
            str: A multi-line string representing the drawn triangle.
        """
        self._validate_dimension(width=width, height=height)
        self._validate_symbol(symbol)
        lines = []
        for row in range(height):
            # Scale the number of symbols proportionally so that:
            # - The first row has at least one symbol.
            # - The last row has exactly 'width' symbols.
            num_symbols = math.ceil((row + 1) / height * width)
            num_symbols = max(1, num_symbols)  # Ensure at least one symbol.
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid with the given height using the specified symbol.
        Each row is centered by prepending the appropriate number of spaces.

        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): The printable symbol to fill the pyramid.

        Returns:
            str: A multi-line string representing the drawn pyramid.
        """
        self._validate_dimension(height=height)
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # Calculate leading spaces and the number of symbols for the current row
            spaces = " " * (height - 1 - i)
            row_symbols = symbol * (2 * i + 1)
            lines.append(spaces + row_symbols)
        return "\n".join(lines)


def main():
    """
    Entry point for the console-based ASCII Art application.
    Provides an interactive menu for the user to select and draw shapes.
    """
    art = AsciiArt()

    menu = (
        "\nASCII Art Application\n"
        "======================\n"
        "1. Draw Square\n"
        "2. Draw Rectangle\n"
        "3. Draw Parallelogram\n"
        "4. Draw Triangle\n"
        "5. Draw Pyramid\n"
        "q. Quit\n"
    )

    while True:
        print(menu)
        choice = input("Enter your choice: ").strip().lower()

        if choice == "q":
            print("Exiting... Goodbye!")
            break

        try:
            if choice == "1":
                width = int(input("Enter side length for square: "))
                symbol = input("Enter a printable symbol (single character): ")
                print("\n" + art.draw_square(width, symbol) + "\n")

            elif choice == "2":
                width = int(input("Enter width for rectangle: "))
                height = int(input("Enter height for rectangle: "))
                symbol = input("Enter a printable symbol (single character): ")
                print("\n" + art.draw_rectangle(width, height, symbol) + "\n")

            elif choice == "3":
                width = int(input("Enter width for parallelogram: "))
                height = int(input("Enter height for parallelogram: "))
                symbol = input("Enter a printable symbol (single character): ")
                print("\n" + art.draw_parallelogram(width, height, symbol) + "\n")

            elif choice == "4":
                width = int(input("Enter maximum width (base) for triangle: "))
                height = int(input("Enter height for triangle: "))
                symbol = input("Enter a printable symbol (single character): ")
                print("\n" + art.draw_triangle(width, height, symbol) + "\n")

            elif choice == "5":
                height = int(input("Enter height for pyramid: "))
                symbol = input("Enter a printable symbol (single character): ")
                print("\n" + art.draw_pyramid(height, symbol) + "\n")

            else:
                print("Invalid choice. Please select a valid option.")

        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as ex:
            print(f"An error occurred: {ex}")


if __name__ == "__main__":
    main()
