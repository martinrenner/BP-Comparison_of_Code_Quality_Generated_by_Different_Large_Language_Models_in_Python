#!/usr/bin/env python3
"""
Console-based 2D ASCII ART application that provides methods
to draw various shapes according to ISO/IEC 25010 quality requirements.

The AsciiArt class implements the following methods:
  - draw_square(width: int, symbol: str) -> str
  - draw_rectangle(width: int, height: int, symbol: str) -> str
  - draw_parallelogram(width: int, height: int, symbol: str) -> str
  - draw_triangle(width: int, height: int, symbol: str) -> str
  - draw_pyramid(height: int, symbol: str) -> str

Each method validates its inputs:
  • width and height must be positive integers (> 0)
  • symbol must be a single, non-whitespace printable character

Additionally, the module includes a main() function providing a simple
console-based menu to interact with the shapes.
"""

import math


class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.
    """

    @staticmethod
    def _validate_dimensions(*dimensions: int) -> None:
        """
        Validate that all provided dimensions are positive integers.
        Raises:
            ValueError: if any dimension is not a positive integer.
        """
        for d in dimensions:
            if not isinstance(d, int):
                raise ValueError("Dimension values must be integers.")
            if d <= 0:
                raise ValueError("Dimension values must be greater than zero.")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the symbol is exactly one non-whitespace character.
        Raises:
            ValueError: if symbol is not a single character or is whitespace.
        """
        if not isinstance(symbol, str):
            raise ValueError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a completely filled square.
        
        Args:
            width (int): The width of the square (also the height).
            symbol (str): A single, non-whitespace character to fill the square.
        
        Returns:
            str: A multi-line string representing the square.
        
        Raises:
            ValueError: If width is non-positive or symbol is invalid.
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)

        rows = [symbol * width for _ in range(width)]
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled rectangle.
        
        Args:
            width (int): The number of symbols horizontally.
            height (int): The number of rows.
            symbol (str): A single, non-whitespace character to fill the rectangle.
        
        Returns:
            str: A multi-line string representing the rectangle.
        
        Raises:
            ValueError: If width or height is non-positive or symbol is invalid.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        rows = [symbol * width for _ in range(height)]
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a completely filled parallelogram that shifts by one space each row.
        
        The parallelogram is drawn such that the top row starts at the left margin,
        and each subsequent row is indented by one additional space.
        
        Args:
            width (int): The number of symbols per row.
            height (int): The number of rows.
            symbol (str): A single, non-whitespace character to fill the parallelogram.
        
        Returns:
            str: A multi-line string representing the parallelogram.
        
        Raises:
            ValueError: If width or height is non-positive or symbol is invalid.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        rows = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle that grows diagonally to the right,
        starting from the top-left corner.
        
        The triangle is drawn over a given number of rows (height) such that:
          - the first row has 1 symbol (with no offset)
          - the last row has 'width' symbols (with maximum offset)
          - each row is additionally indented by its row index (to create the diagonal effect)
          - the number of symbols in between is computed by linear interpolation.
          
        Args:
            width (int): The number of symbols in the last row.
            height (int): The total number of rows.
            symbol (str): A single, non-whitespace character to fill the triangle.
        
        Returns:
            str: A multi-line string representing the triangle.
        
        Raises:
            ValueError: If width or height is non-positive or symbol is invalid.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)

        # When height == 1, the triangle is a single row.
        if height == 1:
            return symbol * width

        # Determine the incremental step to go from 1 symbol up to width symbols.
        step = (width - 1) / (height - 1)
        rows = []
        for i in range(height):
            # Calculate current number of symbols (ensuring at least one)
            current_count = int(round(1 + i * step))
            # Add i leading spaces to produce the diagonal effect
            row = (" " * i) + (symbol * current_count)
            rows.append(row)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical filled pyramid.
        
        The pyramid is centered and drawn over 'height' rows. For each row 'i' the number of
        symbols is given by (2 * i + 1) and the row is preceded by (height - i - 1) spaces.
        
        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): A single, non-whitespace character to fill the pyramid.
        
        Returns:
            str: A multi-line string representing the pyramid.
        
        Raises:
            ValueError: If height is non-positive or symbol is invalid.
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)

        rows = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            rows.append(spaces + symbols)
        return "\n".join(rows)


def main():
    """
    Main entry point for the console-based ASCII Art app.
    Presents a menu to the user to select and draw various shapes.
    """
    ascii_art = AsciiArt()
    
    menu = """
    ===== ASCII Art Application =====
    1. Draw Square
    2. Draw Rectangle
    3. Draw Parallelogram
    4. Draw Right-Angled Triangle
    5. Draw Pyramid
    0. Exit
    =================================
    """
    
    while True:
        print(menu)
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter an integer corresponding to a menu option.\n")
            continue
        
        if choice == 0:
            print("Exiting the application. Goodbye!")
            break
        
        try:
            # For every shape require the symbol first.
            symbol = input("Enter a printable symbol (exactly one non-whitespace character): ")
            # Based on the method, get additional parameters.
            if choice == 1:
                width = int(input("Enter width for the square: "))
                art = ascii_art.draw_square(width, symbol)
            elif choice == 2:
                width = int(input("Enter width for the rectangle: "))
                height = int(input("Enter height for the rectangle: "))
                art = ascii_art.draw_rectangle(width, height, symbol)
            elif choice == 3:
                width = int(input("Enter width for the parallelogram: "))
                height = int(input("Enter height for the parallelogram: "))
                art = ascii_art.draw_parallelogram(width, height, symbol)
            elif choice == 4:
                width = int(input("Enter the number of symbols in the last row (width) for the triangle: "))
                height = int(input("Enter height (number of rows) for the triangle: "))
                art = ascii_art.draw_triangle(width, height, symbol)
            elif choice == 5:
                height = int(input("Enter height for the pyramid: "))
                art = ascii_art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please select a valid option.\n")
                continue

            print("\nGenerated ASCII Art:")
            print(art)
            print("\n")
            
        except ValueError as ve:
            print(f"Error: {ve}\n")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}\n")


if __name__ == '__main__':
    main()
