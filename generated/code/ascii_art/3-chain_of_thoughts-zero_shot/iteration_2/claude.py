class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to draw various ASCII shapes using a specified symbol.
    All shapes are represented as multi-line strings and can be printed to the console.
    """

    @staticmethod
    def _validate_input(symbol: str, *dimensions: int) -> None:
        """
        Validates the input parameters for all drawing methods.
        
        Args:
            symbol: The character used to draw the shape.
            *dimensions: Variable number of integer dimensions (width, height, etc.).
            
        Raises:
            ValueError: If symbol is not a single character or is whitespace,
                       or if any dimension is negative or zero.
        """
        # Validate symbol
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character")
        
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
            
        # Validate dimensions
        for i, dimension in enumerate(dimensions):
            if dimension <= 0:
                dimension_name = ["width", "height"][min(i, 1)]
                raise ValueError(f"{dimension_name.capitalize()} must be positive")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width: The width and height of the square.
            symbol: The character used to draw the square.
            
        Returns:
            A multi-line string representing the square.
            
        Raises:
            ValueError: If width is not positive or symbol is invalid.
        """
        self._validate_input(symbol, width)
        
        # Create a square by generating 'width' rows, each containing 'width' symbols
        return '\n'.join([symbol * width] * width)
        
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character used to draw the rectangle.
            
        Returns:
            A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If width or height is not positive or symbol is invalid.
        """
        self._validate_input(symbol, width, height)
        
        # Create a rectangle by generating 'height' rows, each containing 'width' symbols
        return '\n'.join([symbol * width] * height)
        
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, with each row shifted
        by one space to the right compared to the row above it.
        
        Args:
            width: The width of the parallelogram (base length).
            height: The height of the parallelogram.
            symbol: The character used to draw the parallelogram.
            
        Returns:
            A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If width or height is not positive or symbol is invalid.
        """
        self._validate_input(symbol, width, height)
        
        # Create a parallelogram by adding increasing spaces before each row
        result = []
        for i in range(height):
            result.append(' ' * i + symbol * width)
        
        return '\n'.join(result)
        
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        The width parameter determines the maximum width at the bottom of the triangle.
        
        Args:
            width: The maximum width of the triangle (base length).
            height: The height of the triangle.
            symbol: The character used to draw the triangle.
            
        Returns:
            A multi-line string representing the right-angled triangle.
            
        Raises:
            ValueError: If width or height is not positive or symbol is invalid.
        """
        self._validate_input(symbol, width, height)
        
        result = []
        # Calculate how many symbols to add in each row
        symbols_per_row = [round(width * (i + 1) / height) for i in range(height)]
        
        # Create the triangle by adding the calculated number of symbols in each row
        for num_symbols in symbols_per_row:
            result.append(symbol * num_symbols)
        
        return '\n'.join(result)
        
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        The pyramid's width at the base will be 2 * height - 1.
        
        Args:
            height: The height of the pyramid.
            symbol: The character used to draw the pyramid.
            
        Returns:
            A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_input(symbol, height)
        
        result = []
        for i in range(height):
            # Calculate padding and number of symbols for each row
            spaces = height - i - 1
            symbols_count = 2 * i + 1
            # Create the row with proper spacing and symbols
            row = ' ' * spaces + symbol * symbols_count
            result.append(row)
        
        return '\n'.join(result)


def main():
    """
    Main function to demonstrate the AsciiArt class functionality.
    
    Creates an instance of AsciiArt and shows examples of each shape.
    """
    ascii_art = AsciiArt()
    
    print("ASCII Art Generator\n")
    
    try:
        # Example usage
        print("Square (4x4, using '*'):")
        print(ascii_art.draw_square(4, '*'))
        print()
        
        print("Rectangle (6x3, using '#'):")
        print(ascii_art.draw_rectangle(6, 3, '#'))
        print()
        
        print("Parallelogram (5x3, using '@'):")
        print(ascii_art.draw_parallelogram(5, 3, '@'))
        print()
        
        print("Triangle (5x5, using '+'):")
        print(ascii_art.draw_triangle(5, 5, '+'))
        print()
        
        print("Pyramid (4 high, using 'O'):")
        print(ascii_art.draw_pyramid(4, 'O'))
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
