"""
Console-based 2D ASCII Art application

This module defines the AsciiArt class which provides methods to draw different
ASCII shapes (square, rectangle, parallelogram, right-angled triangle, and pyramid).
Each method returns a multi-line string representing the shape, and parameters are validated
to ensure correct input.

Usage:
    Run the script and follow on-screen instructions to draw shapes.

Author: Senior Software Developer
Date: 2023-10-09
"""

class AsciiArt:
    """
    A class for generating ASCII art shapes with proper input validation.
    
    Methods:
        draw_square(width: int, symbol: str) -> str
        draw_rectangle(width: int, height: int, symbol: str) -> str
        draw_parallelogram(width: int, height: int, symbol: str) -> str
        draw_triangle(width: int, height: int, symbol: str) -> str
        draw_pyramid(height: int, symbol: str) -> str
    """
    
    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validate that a dimension (width or height) is a positive integer.
        Raises:
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer. Got: {value}")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validate that the symbol is a single, non-whitespace character.
        Raises:
            ValueError: If the symbol is not exactly one non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a filled square of the given width using the specified symbol.
        
        Parameters:
            width (int): The width (and height) of the square.
            symbol (str): A single non-whitespace character used to fill the square.
        
        Returns:
            str: A multi-line string representing the square.
        
        Raises:
            ValueError: If width is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_symbol(symbol)
        # Build the square: each row is a string of repeated symbol
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled rectangle of the given width and height using the specified symbol.
        
        Parameters:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): A single non-whitespace character used to fill the rectangle.
        
        Returns:
            str: A multi-line string representing the rectangle.
        
        Raises:
            ValueError: If width or height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled parallelogram of the given width and height.
        The parallelogram is shifted diagonally to the right by one space per row.
        
        Parameters:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): A single non-whitespace character used to fill the shape.
        
        Returns:
            str: A multi-line string representing the parallelogram.
        
        Raises:
            ValueError: If width or height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # Each row is shifted i spaces to the right
            line = " " * i + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a filled right-angled triangle with its right angle at the top-left corner.
        The triangle grows diagonally to the right, starting from a single symbol on the top row,
        up to 'width' symbols on the bottom row. The growth in number of symbols per row is
        linearly interpolated.
        
        Parameters:
            width (int): The number of symbols in the bottom row (base width).
            height (int): The total number of rows in the triangle.
            symbol (str): A single non-whitespace character used to fill the triangle.
        
        Returns:
            str: A multi-line string representing the triangle.
        
        Raises:
            ValueError: If width or height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        
        lines = []
        if height == 1:
            # Only one row; the entire base is drawn.
            lines.append(symbol * width)
        else:
            # For each row, compute the number of symbols using linear interpolation.
            for i in range(height):
                # Linear interpolation: when i==0, one symbol; when i==height-1, width symbols.
                count = int((i / (height - 1)) * (width - 1)) + 1
                lines.append(symbol * count)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a filled symmetrical pyramid.
        The pyramid has a height 'height' and a base width of (2 * height - 1) symbols.
        Each row is centered with appropriate leading spaces.
        
        Parameters:
            height (int): The height of the pyramid.
            symbol (str): A single non-whitespace character used to form the pyramid.
        
        Returns:
            str: A multi-line string representing the pyramid.
        
        Raises:
            ValueError: If height is not a positive integer or symbol is invalid.
        """
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        lines = []
        base_width = 2 * height - 1
        for i in range(height):
            # Number of symbols on this row grows by 2 each time (odd numbers)
            num_symbols = 2 * i + 1
            # Center the symbols: compute left padding
            left_padding = (base_width - num_symbols) // 2
            line = " " * left_padding + symbol * num_symbols
            lines.append(line)
        return "\n".join(lines)

def main():
    """
    Entry point for the console-based ASCII Art application.
    Prompts the user to select a shape and enter parameters, then prints the ASCII art.
    """
    art = AsciiArt()
    
    menu = (
        "\nSelect a shape to draw:\n"
        "1. Square\n"
        "2. Rectangle\n"
        "3. Parallelogram\n"
        "4. Triangle (right-angled)\n"
        "5. Pyramid\n"
        "q. Quit\n"
    )
    
    while True:
        print(menu)
        choice = input("Enter your choice: ").strip().lower()
        
        if choice == 'q':
            print("Exiting ASCII Art application. Goodbye!")
            break
        
        try:
            if choice == '1':
                width = int(input("Enter the width of the square: ").strip())
                symbol = input("Enter a single symbol: ").strip()
                result = art.draw_square(width, symbol)
            elif choice == '2':
                width = int(input("Enter the width of the rectangle: ").strip())
                height = int(input("Enter the height of the rectangle: ").strip())
                symbol = input("Enter a single symbol: ").strip()
                result = art.draw_rectangle(width, height, symbol)
            elif choice == '3':
                width = int(input("Enter the width of the parallelogram: ").strip())
                height = int(input("Enter the height of the parallelogram: ").strip())
                symbol = input("Enter a single symbol: ").strip()
                result = art.draw_parallelogram(width, height, symbol)
            elif choice == '4':
                width = int(input("Enter the base width of the triangle: ").strip())
                height = int(input("Enter the height of the triangle: ").strip())
                symbol = input("Enter a single symbol: ").strip()
                result = art.draw_triangle(width, height, symbol)
            elif choice == '5':
                height = int(input("Enter the height of the pyramid: ").strip())
                symbol = input("Enter a single symbol: ").strip()
                result = art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please try again.")
                continue

            print("\n" + result + "\n")
        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    main()
