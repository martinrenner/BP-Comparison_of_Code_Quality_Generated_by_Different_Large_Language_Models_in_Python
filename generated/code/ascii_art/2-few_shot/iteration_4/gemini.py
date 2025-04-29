class AsciiArt:
    """
    A class for generating ASCII art shapes.

    This class provides methods to draw various geometric shapes filled with a specified symbol.
    It adheres to the principles of OOP and includes input validation to ensure robustness and security.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width filled with the given symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to fill the square with.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If width is negative or symbol is invalid.
        """
        self._validate_input(width, symbol)

        if width == 0:  # handle edge case, return empty string instead of raising error
            return ""

        square = ""
        for _ in range(width):
            square += symbol * width + "\n"
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height filled with the given symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to fill the rectangle with.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If width or height is negative, or symbol is invalid.
        """
        self._validate_input(width, symbol, height)

        if width == 0 or height == 0:
            return ""

        rectangle = ""
        for _ in range(height):
            rectangle += symbol * width + "\n"
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the given width, height, and fill symbol.

        The parallelogram's top-left corner starts at the origin, and each subsequent row
        is shifted one space to the right.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to fill the parallelogram with.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height is negative, or symbol is invalid.
        """
        self._validate_input(width, symbol, height)

        if width == 0 or height == 0:
            return ""

        parallelogram = ""
        for i in range(height):
            parallelogram += " " * i + symbol * width + "\n"
        return parallelogram

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The character to fill the triangle with.

        Returns:
            str: A multi-line string representing the ASCII art triangle.

        Raises:
            ValueError: If width or height is negative, or symbol is invalid.
        """

        self._validate_input(width, symbol, height)

        if width == 0 or height == 0:
            return ""
        
        if width < height:
            raise ValueError("For the triangle, width must be greater or equal than height.")


        triangle = ""
        for i in range(height):
            triangle += symbol * (i + 1) + "\n"
        return triangle

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a pyramid of the specified height filled with the given symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to fill the pyramid with.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is negative or symbol is invalid.
        """
        self._validate_input(height, symbol)  # Height acts as a dimension

        if height == 0:
            return ""

        pyramid = ""
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            pyramid += spaces + symbols + "\n"
        return pyramid
    

    def _validate_input(self, *args):
        """
        Validates the input parameters for the drawing functions.

        Args:
            *args: Variable number of arguments.  Assumes the last argument is the symbol,
                   and all preceding arguments are dimensions (width, height).

        Raises:
            ValueError: If any dimension is negative, or if the symbol is invalid
                        (not a single character or is whitespace).
        """

        *dimensions, symbol = args

        for dim in dimensions:
            if not isinstance(dim, int):
                raise TypeError("Dimensions must be integers.")
            if dim < 0:
                raise ValueError("Dimensions cannot be negative.")

        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")


def main():
    """
    Main function to demonstrate the AsciiArt class.
    """

    art = AsciiArt()

    # Get symbol choice from the user
    while True:
        try:
            symbol = input("Enter the symbol you want to use for drawing: ")
            # Attempt validation to catch errors early.  We use a dummy validation call.
            art._validate_input(1, symbol)
            break  # Exit loop if validation is successful.
        except ValueError as e:
            print(f"Error: {e}")


    print("\nSquare:")
    try:
        print(art.draw_square(5, symbol)) 
    except ValueError as e:
        print(e)    

    print("\nRectangle:")
    try:
        print(art.draw_rectangle(7, 3, symbol))
    except ValueError as e:
        print(e) 

    print("\nParallelogram:")
    try:
        print(art.draw_parallelogram(6, 4, symbol))
    except ValueError as e:
        print(e)
    

    print("\nTriangle:")
    try:
        print(art.draw_triangle(5, 5, symbol))
    except ValueError as e:
        print(e)

    print("\nPyramid:")
    try:
        print(art.draw_pyramid(5, symbol))
    except ValueError as e:
        print(e)

    # ---Demonstrate error handling---
    print("\n--- Error Handling Examples ---")

    print("\nInvalid Square:")
    try:
        #negative width
        print(art.draw_square(-5, symbol))
    except ValueError as e:
        print(e)

    print("\nInvalid Symbol (Rectangle):")
    try:
        #multi-char symbol
        print(art.draw_rectangle(4, 2, "XX"))
    except ValueError as e:
        print(e)

    print("\nWhitespace Symbol (Parallelogram):")
    try:
        #" " (space) symbol
        print(art.draw_parallelogram(4, 2, ' '))
    except ValueError as e:
        print(e)
    
    print("\nZero width (Square):")
    try:
        # width 0
        print(art.draw_square(0, symbol)) # Should not raise error (empty string)
    except ValueError as e:
        print(e)

    print("\nZero height and zero width (Rectangle):")
    try:
        # height and width 0
        print(art.draw_rectangle(0, 0, symbol))
    except ValueError as e:
        print(e)    

    print("\nInvalid Triangle (height > width):")
    try:
        print(art.draw_triangle(2, 5, symbol))
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()

