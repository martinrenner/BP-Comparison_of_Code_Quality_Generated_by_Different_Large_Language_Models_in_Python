class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various ASCII art shapes such as
    squares, rectangles, parallelograms, triangles, and pyramids using a 
    specified symbol.
    """
    
    @staticmethod
    def _validate_input(width: int, height: int, symbol: str) -> None:
        """
        Validates the input parameters for the ASCII art generation methods.
        
        Args:
            width (int): The width of the shape.
            height (int): The height of the shape.
            symbol (str): The symbol to use for drawing the shape.
            
        Raises:
            ValueError: If width or height is not positive.
            ValueError: If symbol is not exactly one character long.
            ValueError: If symbol is whitespace.
        """
        if width <= 0:
            raise ValueError("Width must be a positive integer")
        if height <= 0:
            raise ValueError("Height must be a positive integer")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square with the specified width using the given symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A string representation of the ASCII art square.
            
        Raises:
            ValueError: If inputs are invalid (see _validate_input).
        """
        self._validate_input(width, width, symbol)
        return self.draw_rectangle(width, width, symbol)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle with the specified dimensions using the given symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A string representation of the ASCII art rectangle.
            
        Raises:
            ValueError: If inputs are invalid (see _validate_input).
        """
        self._validate_input(width, height, symbol)
        
        result = []
        line = symbol * width
        for _ in range(height):
            result.append(line)
            
        return '\n'.join(result)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified dimensions using the given symbol.
        The parallelogram grows diagonally to the right, with each row shifted by one space.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A string representation of the ASCII art parallelogram.
            
        Raises:
            ValueError: If inputs are invalid (see _validate_input).
        """
        self._validate_input(width, height, symbol)
        
        result = []
        for i in range(height):
            # Add spaces for the diagonal shift, then add symbols
            line = ' ' * i + symbol * width
            result.append(line)
            
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with the specified dimensions using the given symbol.
        The triangle grows diagonally to the right from the top-left corner.
        
        Args:
            width (int): The maximum width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A string representation of the ASCII art triangle.
            
        Raises:
            ValueError: If inputs are invalid (see _validate_input).
        """
        self._validate_input(width, height, symbol)
        
        result = []
        # Calculate the width increment for each row
        width_increment = width / height if height > 1 else width
        
        for i in range(height):
            # Calculate symbols for current row (at least 1)
            symbols_count = max(1, round((i + 1) * width_increment))
            line = symbol * symbols_count
            result.append(line)
            
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the specified height using the given symbol.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A string representation of the ASCII art pyramid.
            
        Raises:
            ValueError: If inputs are invalid (see _validate_input with width=1).
        """
        # Pass width=1 just to reuse validation logic
        self._validate_input(1, height, symbol)
        
        result = []
        for i in range(height):
            # Calculate spaces and symbols for each row
            spaces = ' ' * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            result.append(spaces + symbols)
            
        return '\n'.join(result)


def main():
    """
    Main function to demonstrate the ASCII Art generator.
    """
    ascii_art = AsciiArt()
    
    print("ASCII Art Generator")
    print("-" * 30)
    
    # Example usage
    try:
        print("\nSquare (4x4 with '#'):")
        print(ascii_art.draw_square(4, "#"))
        
        print("\nRectangle (6x3 with '*'):")
        print(ascii_art.draw_rectangle(6, 3, "*"))
        
        print("\nParallelogram (5x3 with '@'):")
        print(ascii_art.draw_parallelogram(5, 3, "@"))
        
        print("\nTriangle (5x5 with '+'):")
        print(ascii_art.draw_triangle(5, 5, "+"))
        
        print("\nPyramid (5 height with '^'):")
        print(ascii_art.draw_pyramid(5, "^"))
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
