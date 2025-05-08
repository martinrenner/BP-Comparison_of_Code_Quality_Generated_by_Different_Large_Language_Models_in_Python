import math

class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.

    Provides methods to draw a square, rectangle, parallelogram, right-angled triangle,
    and a symmetrical pyramid. Each shape is completely filled with a user-defined symbol.
    """

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        """
        Validates that the given dimension is a positive integer.

        Args:
            value (int): The dimension value.
            name (str): The name of the dimension for error messages.

        Raises:
            ValueError: If 'value' is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer. Received: {value}")

    @staticmethod
    def _validate_symbol(symbol: str) -> None:
        """
        Validates that the symbol provided is a single non-whitespace character.

        Args:
            symbol (str): The symbol to validate.

        Raises:
            ValueError: If 'symbol' is not exactly one non-whitespace character.
        """
        if not isinstance(symbol, str) or len(symbol) != 1 or symbol.isspace():
            raise ValueError("Symbol must be a single non-whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square with equal width and height using the specified symbol.

        Args:
            width (int): The side length of the square.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the square.

        Raises:
            ValueError: If 'width' is not a positive integer or if 'symbol' is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_symbol(symbol)
        
        # Generate each row of the square
        rows = [symbol * width for _ in range(width)]
        return "\n".join(rows)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height using the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the rectangle.

        Raises:
            ValueError: If 'width' or 'height' is not a positive integer or if 'symbol' is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        
        rows = [symbol * width for _ in range(height)]
        return "\n".join(rows)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram that shifts one space right on each subsequent row.

        Args:
            width (int): The number of symbols in each row.
            height (int): The number of rows.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the parallelogram.

        Raises:
            ValueError: If 'width' or 'height' is not a positive integer or if 'symbol' is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Each row is shifted by an increasing number of spaces.
            line = " " * row + symbol * width
            lines.append(line)
        return "\n".join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle that grows diagonally to the right starting from the top-left corner.
        The triangle is scaled such that the last row has 'width' symbols.

        Args:
            width (int): The maximum number of symbols (in the base row).
            height (int): The number of rows in the triangle.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the triangle.

        Raises:
            ValueError: If 'width' or 'height' is not a positive integer or if 'symbol' is invalid.
        """
        self._validate_dimension(width, "Width")
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Compute the number of symbols for the current row.
            # Ensures a linear increase from one symbol on the first row to 'width' symbols on the last.
            num_symbols = math.ceil((row + 1) * width / height)
            lines.append(symbol * num_symbols)
        return "\n".join(lines)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the given height. The base of the pyramid will have (2 * height - 1) symbols.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the pyramid.

        Raises:
            ValueError: If 'height' is not a positive integer or if 'symbol' is invalid.
        """
        self._validate_dimension(height, "Height")
        self._validate_symbol(symbol)
        
        lines = []
        for row in range(height):
            # Calculate leading spaces and the number of symbols for current row.
            spaces = " " * (height - row - 1)
            symbols = symbol * (2 * row + 1)
            lines.append(spaces + symbols)
        return "\n".join(lines)

def main():
    """
    Console-based 2D ASCII Art application.

    Provides a menu for the user to select the shape to draw, enter the required parameters,
    and then outputs the generated ASCII art. Input validations are performed to ensure safe and correct usage.
    """
    ascii_art = AsciiArt()
    
    menu = (
        "\nASCII Art Generator Menu:\n"
        "1. Draw Square\n"
        "2. Draw Rectangle\n"
        "3. Draw Parallelogram\n"
        "4. Draw Triangle (Right-angled)\n"
        "5. Draw Pyramid\n"
        "6. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            try:
                width = int(input("Enter the width of the square: ").strip())
                symbol = input("Enter a single non-whitespace character: ").strip()
                art = ascii_art.draw_square(width, symbol)
                print("\n" + art)
            except ValueError as ve:
                print("Error:", ve)
        elif choice == '2':
            try:
                width = int(input("Enter the width of the rectangle: ").strip())
                height = int(input("Enter the height of the rectangle: ").strip())
                symbol = input("Enter a single non-whitespace character: ").strip()
                art = ascii_art.draw_rectangle(width, height, symbol)
                print("\n" + art)
            except ValueError as ve:
                print("Error:", ve)
        elif choice == '3':
            try:
                width = int(input("Enter the width of the parallelogram: ").strip())
                height = int(input("Enter the height of the parallelogram: ").strip())
                symbol = input("Enter a single non-whitespace character: ").strip()
                art = ascii_art.draw_parallelogram(width, height, symbol)
                print("\n" + art)
            except ValueError as ve:
                print("Error:", ve)
        elif choice == '4':
            try:
                width = int(input("Enter the base width of the triangle: ").strip())
                height = int(input("Enter the height of the triangle: ").strip())
                symbol = input("Enter a single non-whitespace character: ").strip()
                art = ascii_art.draw_triangle(width, height, symbol)
                print("\n" + art)
            except ValueError as ve:
                print("Error:", ve)
        elif choice == '5':
            try:
                height = int(input("Enter the height of the pyramid: ").strip())
                symbol = input("Enter a single non-whitespace character: ").strip()
                art = ascii_art.draw_pyramid(height, symbol)
                print("\n" + art)
            except ValueError as ve:
                print("Error:", ve)
        elif choice == '6':
            print("Exiting the ASCII Art Generator. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == '__main__':
    main()
