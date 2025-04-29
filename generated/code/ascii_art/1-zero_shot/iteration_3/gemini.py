class AsciiArt:
    """
    A class for generating ASCII art shapes.

    This class provides methods to draw various shapes using ASCII characters,
    adhering to the principles of OOP and meeting the requirements of
    ISO/IEC 25010 regarding quality characteristics.
    """

    def _validate_input(self, symbol: str, dimensions: tuple[int, ...]):
        """
        Validates the input parameters for shape drawing functions.

        Args:
            symbol (str): The character to use for drawing the shape.
            dimensions (tuple[int, ...]):  A tuple containing the dimensions (width, height, etc.)

        Raises:
            TypeError: If symbol is not a string, or if dimensions are not integers.
            ValueError: If symbol is not a single character, is whitespace,
                         or if any dimension is not a positive integer.
        """

        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
        for dim in dimensions:
            if not isinstance(dim, int):
                raise TypeError("Dimensions must be integers.")
            if dim <= 0:
                raise ValueError("Dimensions must be positive integers.")


    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width using the specified symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to use for drawing the square.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            (Exceptions are raised by _validate_input)
        """
        self._validate_input(symbol, (width,))
        return '\n'.join([symbol * width for _ in range(width)])


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given dimensions using the specified symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

            (Exceptions are raised by _validate_input)
        """
        self._validate_input(symbol, (width, height))
        return '\n'.join([symbol * width for _ in range(height)])


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.

            (Exceptions are raised by _validate_input)
        """
        self._validate_input(symbol, (width, height))
        lines = []
        for i in range(height):
            lines.append(' ' * i + symbol * width)  # Efficient string concatenation
        return '\n'.join(lines)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width (int): Width of the triangle's base
            height (int): The height of the triangle.
            symbol (str): The character to use.

        Returns:
            str:  A multi-line string representing the ASCII art triangle.

            (Exceptions are raised by _validate_input)
       """
        self._validate_input(symbol, (width, height))

        # For a right-angled triangle, we constrain the visible part.
        # We draw based on the 'height'. The 'width' parameter is present to conform
        # to the function specified in the requirements,
        # but effective width will depend on row number.
        lines = []
        for i in range(1, height + 1):
              lines.append(symbol * i)
        return '\n'.join(lines)


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid of the given height using the specified symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.

            (Exceptions are raised by _validate_input)
        """
        self._validate_input(symbol, (height,))
        lines = []
        for i in range(height):
            spaces = ' ' * (height - 1 - i)
            symbols = symbol * (2 * i + 1)
            lines.append(spaces + symbols)
        return '\n'.join(lines)



def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    art = AsciiArt()

    # Get user input with error handling
    while True:
        try:
            symbol = input("Enter the symbol to use for drawing: ")
            width = int(input("Enter width (positive integer): "))
            height = int(input("Enter height (positive integer, for applicable shapes): "))

            #  Input validation is now handled in the class,
            #  but we keep this outer try/except block for handling
            #   cases where input() itself fails
            #  (e.g., user just types "ctrl c").
            break;  # Exit the loop if input is valid.

        except ValueError as e:  # Catch general ValueError from int() conversion
           print(f"Invalid input: {e}. Please enter valid integer values.")
        except Exception as e:
            print(f"An unexpected error occurred during input: {e}")


    # Draw shapes and print them, handling potential errors from class methods.
    try:
        print("\nSquare:")
        print(art.draw_square(width, symbol))

        print("\nRectangle:")
        print(art.draw_rectangle(width, height, symbol))

        print("\nParallelogram:")
        print(art.draw_parallelogram(width, height, symbol))

        print("\nTriangle:")
        print(art.draw_triangle(width, height, symbol))

        print("\nPyramid:")
        print(art.draw_pyramid(height, symbol))  # Use height for pyramid

    except (TypeError, ValueError) as e: # Catch exceptions from AsciiArt methods.
        print(f"Error during shape generation: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during shape drawing: {e}")

if __name__ == "__main__":
    main()

