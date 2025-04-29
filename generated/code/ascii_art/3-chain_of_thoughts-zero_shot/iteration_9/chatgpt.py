"""
Console-based ASCII Art Application

This application lets the user draw various 2D ASCII shapes on the console.
It implements the following shapes:
  • Square
  • Rectangle
  • Parallelogram (rows shifted diagonally)
  • Right-angled Triangle
  • Symmetrical Pyramid

Each drawing function validates inputs according to the requirements:
  - width/height must be positive integers.
  - symbol must be a single, non‐whitespace character.

The implementation follows object-oriented principles and is designed for clarity,
modularity, security and testability.
"""

import math


class AsciiArt:
    """
    Class providing methods to generate ASCII art of different shapes.
    """

    def _validate_dimension(self, value: int, name: str):
        """
        Validate that a dimension (width or height) is a positive integer.
        Raises:
            ValueError: if value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer.")

    def _validate_symbol(self, symbol: str):
        """
        Validate that symbol is a single non-whitespace character.
        Raises:
            ValueError: if symbol is not a single printable character.
        """
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square with side length 'width' using the given symbol.
        
        Args:
            width (int): The side length of the square.
            symbol (str): The printable symbol (single character) to use.
        
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If width is not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_symbol(symbol)

        # Build the square: same row repeated 'width' times.
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle with the specified width and height using the given symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The printable symbol (single character) to use.
        
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If width or height is not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram that grows diagonally to the right.
        Each row is shifted one space relative to the previous row.
        
        Args:
            width (int): The number of symbols per row.
            height (int): The total number of rows.
            symbol (str): The printable symbol (single character) to use.
        
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If width or height is not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.
        The triangle is defined by a horizontal leg on the top and a vertical leg on the left,
        with the hypotenuse running diagonally from the top-right to the bottom-left.
        The shape is completely filled with the given symbol.
        The dimensions 'width' (horizontal leg) and 'height' (vertical leg) are used to linearly
        interpolate the number of symbols per row. For height > 1, the first row has 'width'
        symbols and the last row has one symbol.
        
        For example, draw_triangle(10, 5, "#") might output:
            ##########
            ########
            ######
            ###
            #
        
        Args:
            width (int): The length of the horizontal leg (top row length).
            height (int): The number of rows (vertical leg length).
            symbol (str): The printable symbol (single character) to use.
        
        Returns:
            str: A multi-line string representing the right-angled triangle.
            
        Raises:
            ValueError: If width or height is not positive or symbol is invalid.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        if height == 1:
            # Only one row; print the top row.
            lines.append(symbol * width)
        else:
            # Interpolate so that the first row has 'width' symbols and
            # the last row has 1 symbol; rounding is applied.
            for i in range(height):
                # Linear interpolation:
                # When i == 0 -> count = width,
                # when i == height - 1 -> count = 1.
                count = int(round(width - ((width - 1) * (i / (height - 1)))))
                # Ensure at least one symbol is printed.
                count = max(1, count)
                lines.append(symbol * count)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.
        Each row of the pyramid is centered with the left padding such that the pyramid
        base has width (2 * height - 1) symbols.
        
        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): The printable symbol (single character) to use.
        
        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_dimension(height, "height")
        self._validate_symbol(symbol)

        lines = []
        for i in range(height):
            # Calculate the number of symbols in the current row.
            symbols_in_row = 2 * i + 1
            # Calculate left padding for centering.
            padding = height - i - 1
            lines.append(" " * padding + symbol * symbols_in_row)
        return "\n".join(lines)


def main():
    """
    Main function: provides a console-based menu for users to generate ASCII art shapes.
    """
    art = AsciiArt()

    menu = """
ASCII Art Drawing Menu:
1. Draw Square
2. Draw Rectangle
3. Draw Parallelogram
4. Draw Right-Angled Triangle
5. Draw Pyramid
0. Exit
"""
    print("Welcome to the ASCII Art App!")
    while True:
        print(menu)
        choice = input("Enter your choice (0-5): ").strip()
        if choice == "0":
            print("Exiting the ASCII Art App. Goodbye!")
            break

        try:
            if choice == "1":
                width = int(input("Enter the side length for the square: "))
                symbol = input("Enter a printable symbol (one character): ").strip()
                result = art.draw_square(width, symbol)
            elif choice == "2":
                width = int(input("Enter the rectangle width: "))
                height = int(input("Enter the rectangle height: "))
                symbol = input("Enter a printable symbol (one character): ").strip()
                result = art.draw_rectangle(width, height, symbol)
            elif choice == "3":
                width = int(input("Enter the parallelogram width: "))
                height = int(input("Enter the parallelogram height: "))
                symbol = input("Enter a printable symbol (one character): ").strip()
                result = art.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                width = int(input("Enter the triangle's top row symbol count (horizontal leg): "))
                height = int(input("Enter the triangle height (vertical leg): "))
                symbol = input("Enter a printable symbol (one character): ").strip()
                result = art.draw_triangle(width, height, symbol)
            elif choice == "5":
                height = int(input("Enter the pyramid height: "))
                symbol = input("Enter a printable symbol (one character): ").strip()
                result = art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please choose a valid option (0-5).")
                continue

            print("\nGenerated ASCII Art:\n")
            print(result)
            print("\n" + "-" * 40 + "\n")
        except (ValueError, TypeError) as e:
            print(f"Error: {e}\nPlease try again.\n")


if __name__ == "__main__":
    main()
