class AsciiArt:
    """
    A class for creating ASCII art shapes.
    
    This class provides methods to draw various ASCII art shapes
    like squares, rectangles, parallelograms, triangles, and pyramids.
    Each shape is filled with a specified symbol.
    """
    
    @staticmethod
    def _validate_input(width: int, height: int, symbol: str) -> None:
        """
        Validates the input parameters for all drawing functions.
        
        Args:
            width (int): Width of the shape.
            height (int): Height of the shape.
            symbol (str): Symbol to use for drawing the shape.
            
        Raises:
            ValueError: If the width or height is non-positive.
            ValueError: If the symbol is not a single character or is whitespace.
        """
        if width <= 0:
            raise ValueError("Width must be a positive integer.")
        if height <= 0:
            raise ValueError("Height must be a positive integer.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): Width of the square.
            symbol (str): Symbol to use for drawing the square.
            
        Returns:
            str: A multi-line string representing the square in ASCII art.
            
        Raises:
            ValueError: If the width is non-positive or the symbol is invalid.
        """
        self._validate_input(width, width, symbol)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        # Create a list of rows to form the square
        square = [row for _ in range(width)]
        
        return "\n".join(square)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width (int): Width of the rectangle.
            height (int): Height of the rectangle.
            symbol (str): Symbol to use for drawing the rectangle.
            
        Returns:
            str: A multi-line string representing the rectangle in ASCII art.
            
        Raises:
            ValueError: If the width or height is non-positive or the symbol is invalid.
        """
        self._validate_input(width, height, symbol)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        # Create a list of rows to form the rectangle
        rectangle = [row for _ in range(height)]
        
        return "\n".join(rectangle)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): Width of the parallelogram.
            height (int): Height of the parallelogram.
            symbol (str): Symbol to use for drawing the parallelogram.
            
        Returns:
            str: A multi-line string representing the parallelogram in ASCII art.
            
        Raises:
            ValueError: If the width or height is non-positive or the symbol is invalid.
        """
        self._validate_input(width, height, symbol)
        
        parallelogram = []
        for i in range(height):
            # Add spaces for the diagonal effect - each row shifted by one space
            spaces = " " * i
            # Add symbols for the width of the parallelogram
            row = spaces + symbol * width
            parallelogram.append(row)
        
        return "\n".join(parallelogram)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): Width of the triangle.
            height (int): Height of the triangle.
            symbol (str): Symbol to use for drawing the triangle.
            
        Returns:
            str: A multi-line string representing the triangle in ASCII art.
            
        Raises:
            ValueError: If the width or height is non-positive or the symbol is invalid.
        """
        self._validate_input(width, height, symbol)
        
        triangle = []
        # Calculate the number of symbols to add for each row
        symbols_per_row = [round(width * (i + 1) / height) for i in range(height)]
        
        for symbols in symbols_per_row:
            row = symbol * symbols
            triangle.append(row)
        
        return "\n".join(triangle)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        Args:
            height (int): Height of the pyramid.
            symbol (str): Symbol to use for drawing the pyramid.
            
        Returns:
            str: A multi-line string representing the pyramid in ASCII art.
            
        Raises:
            ValueError: If the height is non-positive or the symbol is invalid.
        """
        self._validate_input(1, height, symbol)
        
        pyramid = []
        for i in range(height):
            # Calculate the number of symbols for the current row
            symbols_count = 2 * i + 1
            # Calculate the number of spaces needed before the symbols
            spaces_count = height - i - 1
            # Create the row with the appropriate spacing and symbols
            row = " " * spaces_count + symbol * symbols_count
            pyramid.append(row)
        
        return "\n".join(pyramid)


def main():
    """
    Main function to demonstrate the ASCII art functionalities.
    """
    ascii_art = AsciiArt()
    
    try:
        # Draw and display a square
        print("\nSquare (5x5 using '#'):")
        print(ascii_art.draw_square(5, "#"))
        
        # Draw and display a rectangle
        print("\nRectangle (8x4 using '*'):")
        print(ascii_art.draw_rectangle(8, 4, "*"))
        
        # Draw and display a parallelogram
        print("\nParallelogram (6x4 using '@'):")
        print(ascii_art.draw_parallelogram(6, 4, "@"))
        
        # Draw and display a right-angled triangle
        print("\nTriangle (5x5 using '+'):")
        print(ascii_art.draw_triangle(5, 5, "+"))
        
        # Draw and display a pyramid
        print("\nPyramid (height 5 using '^'):")
        print(ascii_art.draw_pyramid(5, "^"))
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
