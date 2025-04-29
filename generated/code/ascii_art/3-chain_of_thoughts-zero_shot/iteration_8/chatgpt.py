import math

class AsciiArt:
    """
    A class to generate various ASCII art shapes.
    Implements methods to draw a square, rectangle, parallelogram,
    right-angled triangle, and symmetrical pyramid.
    
    All shapes are completely filled with a user-provided symbol.
    """

    def __init__(self):
        pass

    def _validate_dimensions(self, *dims: int):
        """
        Validate that all provided dimensions (width, height, etc.) are positive integers.
        
        Args:
            dims (int): One or more dimension values.
        
        Raises:
            ValueError: If any dimension is not a positive integer.
        """
        for dim in dims:
            if not isinstance(dim, int) or dim <= 0:
                raise ValueError("Dimensions (width/height) must be positive integers.")

    def _validate_symbol(self, symbol: str):
        """
        Validate that the symbol is a single (non-whitespace) character.
        
        Args:
            symbol (str): The character to validate.
        
        Raises:
            ValueError: If symbol is not a single printable, non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width. Both width and height are equal.
        
        Args:
            width (int): The number of symbols on each side of the square.
            symbol (str): The character used to fill the square.
        
        Returns:
            str: A multi-line string representing the square.
        """
        self._validate_dimensions(width)
        self._validate_symbol(symbol)
        # Create each row by repeating the symbol and assemble the rows.
        lines = [symbol * width for _ in range(width)]
        return "\n".join(lines)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle with the provided width and height.
        
        Args:
            width (int): The number of symbols per row.
            height (int): The number of rows.
            symbol (str): The character used to fill the rectangle.
        
        Returns:
            str: A multi-line string representing the rectangle.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        lines = [symbol * width for _ in range(height)]
        return "\n".join(lines)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram that grows diagonally to the right.
        Each subsequent row is indented by one additional space.
        
        Args:
            width (int): The number of symbols in each row.
            height (int): The total number of rows.
            symbol (str): The character used to fill the shape.
        
        Returns:
            str: A multi-line string representing the parallelogram.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        lines = [(" " * i) + (symbol * width) for i in range(height)]
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally to the right,
        starting from the top-left corner.
        
        The triangle is drawn over 'height' rows. The number of symbols 
        in each row increases from 1 (or a small number) up to 'width' on the 
        bottom row. Additionally, each row is indented by one more space than 
        the previous row to accentuate the diagonal growth.
        
        Args:
            width (int): The number of symbols in the base (last row) of the triangle.
            height (int): The total number of rows for the triangle.
            symbol (str): The character used to fill the triangle.
        
        Returns:
            str: A multi-line string representing the triangle.
        """
        self._validate_dimensions(width, height)
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # Determine how many symbols to print. This calculation
            # ensures that the final row contains exactly 'width' symbols.
            n_symbols = math.ceil((i + 1) * width / height)
            # Add leading spaces to create a diagonal effect.
            line = " " * i + symbol * n_symbols
            lines.append(line)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a centered, symmetrical pyramid of the specified height.
        
        The pyramid uses (2*i + 1) symbols on the i-th row (0-indexed)
        and is padded with spaces to center it.
        
        Args:
            height (int): The number of rows in the pyramid.
            symbol (str): The character used to fill the pyramid.
        
        Returns:
            str: A multi-line string representing the pyramid.
        """
        self._validate_dimensions(height)
        self._validate_symbol(symbol)
        lines = []
        for i in range(height):
            # Compute left-padding to center the pyramid.
            spaces = " " * (height - i - 1)
            symbols_count = 2 * i + 1
            line = spaces + symbol * symbols_count
            lines.append(line)
        return "\n".join(lines)


def main():
    """
    Console-based interface for the ASCII Art application.
    
    Users can interactively choose a shape to draw and provide parameters.
    The generated ASCII art is then printed to the console.
    """
    ascii_art = AsciiArt()
    menu = """
Choose a shape to draw:
1. Square
2. Rectangle
3. Parallelogram
4. Right-angled Triangle
5. Pyramid
6. Quit
"""
    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "6":
            print("Exiting the ASCII Art App. Goodbye!")
            break

        try:
            if choice == "1":
                width = int(input("Enter the width of the square: "))
                symbol = input("Enter a single printable symbol: ")
                art = ascii_art.draw_square(width, symbol)
            elif choice == "2":
                width = int(input("Enter the width of the rectangle: "))
                height = int(input("Enter the height of the rectangle: "))
                symbol = input("Enter a single printable symbol: ")
                art = ascii_art.draw_rectangle(width, height, symbol)
            elif choice == "3":
                width = int(input("Enter the width of the parallelogram: "))
                height = int(input("Enter the height of the parallelogram: "))
                symbol = input("Enter a single printable symbol: ")
                art = ascii_art.draw_parallelogram(width, height, symbol)
            elif choice == "4":
                width = int(input("Enter the base width of the triangle: "))
                height = int(input("Enter the height of the triangle: "))
                symbol = input("Enter a single printable symbol: ")
                art = ascii_art.draw_triangle(width, height, symbol)
            elif choice == "5":
                height = int(input("Enter the height of the pyramid: "))
                symbol = input("Enter a single printable symbol: ")
                art = ascii_art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please choose a valid option (1-6).")
                continue

            print("\nGenerated ASCII Art:")
            print(art)
        except ValueError as ve:
            print("Input Error:", ve)
        except Exception as e:
            print("An unexpected error occurred:", e)

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
