class AsciiArt:
    """
    A class for drawing various ASCII art shapes.
    
    This class provides methods to generate ASCII art shapes like squares,
    rectangles, triangles, parallelograms, and pyramids using a specified symbol.
    """
    
    @staticmethod
    def _validate_input(width: int, height: int, symbol: str) -> None:
        """
        Validates the input parameters for all drawing functions.
        
        Args:
            width: Width of the shape
            height: Height of the shape
            symbol: Character to use for drawing
            
        Raises:
            ValueError: If inputs are invalid
            TypeError: If inputs are of wrong type
        """
        # Validate types
        if not isinstance(width, int):
            raise TypeError("Width must be an integer")
        if not isinstance(height, int):
            raise TypeError("Height must be an integer")
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string")
            
        # Validate values
        if width <= 0:
            raise ValueError("Width must be positive")
        if height <= 0:
            raise ValueError("Height must be positive")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width: Width and height of the square
            symbol: Character to use for drawing
            
        Returns:
            A string representation of the square
            
        Raises:
            ValueError: If inputs are invalid
            TypeError: If inputs are of wrong type
        """
        self._validate_input(width, width, symbol)
        
        # Create a single row of symbols
        row = symbol * width
        
        # Repeat the row for each line and join with newlines
        return '\n'.join([row for _ in range(width)])
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width: Width of the rectangle
            height: Height of the rectangle
            symbol: Character to use for drawing
            
        Returns:
            A string representation of the rectangle
            
        Raises:
            ValueError: If inputs are invalid
            TypeError: If inputs are of wrong type
        """
        self._validate_input(width, height, symbol)
        
        # Create a single row of symbols
        row = symbol * width
        
        # Repeat the row for each line and join with newlines
        return '\n'.join([row for _ in range(height)])
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        The triangle grows diagonally from top-left to bottom-right.
        
        Args:
            width: Width of the triangle (base)
            height: Height of the triangle
            symbol: Character to use for drawing
            
        Returns:
            A string representation of the triangle
            
        Raises:
            ValueError: If inputs are invalid
            TypeError: If inputs are of wrong type
        """
        self._validate_input(width, height, symbol)
        
        result = []
        # Calculate symbol count for each row
        for i in range(1, height + 1):
            # Determine how many symbols to draw in this row
            symbols_in_row = max(1, round(i * width / height))
            result.append(symbol * symbols_in_row)
        
        return '\n'.join(result)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        Each row is shifted one space to the right compared to the row above.
        
        Args:
            width: Width of the parallelogram (top and bottom sides)
            height: Height of the parallelogram
            symbol: Character to use for drawing
            
        Returns:
            A string representation of the parallelogram
            
        Raises:
            ValueError: If inputs are invalid
            TypeError: If inputs are of wrong type
        """
        self._validate_input(width, height, symbol)
        
        result = []
        for i in range(height):
            # Add spaces equal to the row index, then the symbols
            result.append(' ' * i + symbol * width)
        
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        Args:
            height: Height of the pyramid
            symbol: Character to use for drawing
            
        Returns:
            A string representation of the pyramid
            
        Raises:
            ValueError: If inputs are invalid
            TypeError: If inputs are of wrong type
        """
        # Base width is 2*height-1 for a symmetrical pyramid
        width = 2 * height - 1
        self._validate_input(width, height, symbol)
        
        result = []
        for i in range(1, height + 1):
            # Calculate number of symbols for this row: 2*i-1
            symbols_count = 2 * i - 1
            # Calculate number of spaces before symbols: (width-symbols_count)/2
            spaces_count = (width - symbols_count) // 2
            
            result.append(' ' * spaces_count + symbol * symbols_count)
        
        return '\n'.join(result)


def main():
    """Main function to demonstrate the AsciiArt class."""
    ascii_art = AsciiArt()
    
    try:
        # Example usage with proper error handling
        print("\nSquare (4x4):")
        print(ascii_art.draw_square(4, "#"))
        
        print("\nRectangle (6x3):")
        print(ascii_art.draw_rectangle(6, 3, "*"))
        
        print("\nTriangle (5x3):")
        print(ascii_art.draw_triangle(5, 3, "@"))
        
        print("\nParallelogram (5x3):")
        print(ascii_art.draw_parallelogram(5, 3, "+"))
        
        print("\nPyramid (height 4):")
        print(ascii_art.draw_pyramid(4, "^"))
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
