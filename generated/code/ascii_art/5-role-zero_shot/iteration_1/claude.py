class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various ASCII art shapes like
    squares, rectangles, parallelograms, triangles, and pyramids.
    """
    
    @staticmethod
    def _validate_input(width: int, height: int, symbol: str) -> None:
        """
        Validates the input parameters for the drawing methods.
        
        Args:
            width: The width of the shape.
            height: The height of the shape.
            symbol: The character to draw the shape with.
            
        Raises:
            ValueError: If width or height is negative, or symbol is invalid.
            TypeError: If inputs are of incorrect type.
        """
        # Type checking
        if not isinstance(width, int):
            raise TypeError("Width must be an integer")
        if not isinstance(height, int):
            raise TypeError("Height must be an integer")
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string")
            
        # Value validation
        if width < 1:
            raise ValueError("Width must be positive")
        if height < 1:
            raise ValueError("Height must be positive")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square using the specified symbol.
        
        Args:
            width: The width and height of the square.
            symbol: The character to draw the square with.
            
        Returns:
            A multi-line string representing the ASCII art square.
            
        Raises:
            ValueError: If width is negative or zero, or symbol is invalid.
        """
        self._validate_input(width, width, symbol)
        
        # Create a single row of the square
        row = symbol * width
        
        # Repeat the row for each line of the square
        return '\n'.join([row] * width)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle using the specified symbol.
        
        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to draw the rectangle with.
            
        Returns:
            A multi-line string representing the ASCII art rectangle.
            
        Raises:
            ValueError: If width or height is negative or zero, or symbol is invalid.
        """
        self._validate_input(width, height, symbol)
        
        # Create a single row of the rectangle
        row = symbol * width
        
        # Repeat the row for each line of the rectangle
        return '\n'.join([row] * height)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram using the specified symbol.
        
        Each row is shifted one space to the right of the previous row.
        
        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to draw the parallelogram with.
            
        Returns:
            A multi-line string representing the ASCII art parallelogram.
            
        Raises:
            ValueError: If width or height is negative or zero, or symbol is invalid.
        """
        self._validate_input(width, height, symbol)
        
        result = []
        for i in range(height):
            # Add appropriate number of spaces for indentation
            # followed by the symbols to form the row
            result.append(' ' * i + symbol * width)
        
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle using the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width: The width of the triangle.
            height: The height of the triangle.
            symbol: The character to draw the triangle with.
            
        Returns:
            A multi-line string representing the ASCII art triangle.
            
        Raises:
            ValueError: If width or height is negative or zero, or symbol is invalid.
        """
        self._validate_input(width, height, symbol)
        
        result = []
        # Calculate symbol count for each row based on the proportion
        for i in range(height):
            symbols_count = max(1, round((i + 1) * width / height))
            result.append(symbol * symbols_count)
        
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid using the specified symbol.
        
        The pyramid grows downward with each row wider than the previous.
        
        Args:
            height: The height of the pyramid.
            symbol: The character to draw the pyramid with.
            
        Returns:
            A multi-line string representing the ASCII art pyramid.
            
        Raises:
            ValueError: If height is negative or zero, or symbol is invalid.
        """
        self._validate_input(height, height, symbol)
        
        result = []
        for i in range(height):
            # Calculate the number of symbols for this row
            symbols_count = 2 * i + 1
            # Calculate padding to center the symbols
            padding = height - i - 1
            # Build the row with proper padding and symbols
            result.append(' ' * padding + symbol * symbols_count)
        
        return '\n'.join(result)


def main():
    """
    Main function to demonstrate the ASCII Art generator.
    """
    ascii_art = AsciiArt()
    
    # Example usage
    print("Square:")
    print(ascii_art.draw_square(5, '#'))
    
    print("\nRectangle:")
    print(ascii_art.draw_rectangle(8, 4, '*'))
    
    print("\nParallelogram:")
    print(ascii_art.draw_parallelogram(7, 5, '@'))
    
    print("\nTriangle:")
    print(ascii_art.draw_triangle(6, 5, '+'))
    
    print("\nPyramid:")
    print(ascii_art.draw_pyramid(6, '^'))

if __name__ == "__main__":
    main()
