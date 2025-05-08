class AsciiArt:
    """
    A class that provides functionality to generate ASCII art shapes.
    
    This class implements various methods to create 2D ASCII art shapes
    including squares, rectangles, parallelograms, triangles, and pyramids.
    Each shape is completely filled with a user-specified symbol.
    """
    
    @staticmethod
    def _validate_input(width=None, height=None, symbol=None):
        """
        Validates the input parameters.
        
        Args:
            width (int, optional): Width of the shape.
            height (int, optional): Height of the shape.
            symbol (str, optional): Symbol to use for drawing.
            
        Raises:
            ValueError: If any of the parameters fail validation.
        """
        # Validate symbol
        if symbol is not None:
            if len(symbol) != 1:
                raise ValueError("Symbol must be exactly one character")
            if symbol.isspace():
                raise ValueError("Symbol cannot be whitespace")
        
        # Validate dimensions
        if width is not None and width <= 0:
            raise ValueError("Width must be positive")
        if height is not None and height <= 0:
            raise ValueError("Height must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The symbol to use for drawing the square.
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If width is not positive or symbol is invalid.
        """
        self._validate_input(width=width, symbol=symbol)
        
        # Create a square by generating 'width' rows of 'width' symbols each
        return '\n'.join([symbol * width for _ in range(width)])
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing the rectangle.
            
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If width/height is not positive or symbol is invalid.
        """
        self._validate_input(width=width, height=height, symbol=symbol)
        
        # Create a rectangle by generating 'height' rows of 'width' symbols each
        return '\n'.join([symbol * width for _ in range(height)])
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        The parallelogram grows diagonally to the right, starting from the top-left corner,
        with each row shifted by one space.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing the parallelogram.
            
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If width/height is not positive or symbol is invalid.
        """
        self._validate_input(width=width, height=height, symbol=symbol)
        
        # Create a parallelogram by generating 'height' rows,
        # each shifted one space to the right from the previous
        return '\n'.join([' ' * i + symbol * width for i in range(height)])
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The base width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol to use for drawing the triangle.
            
        Returns:
            str: A multi-line string representing the triangle.
            
        Raises:
            ValueError: If width/height is not positive or symbol is invalid.
        """
        self._validate_input(width=width, height=height, symbol=symbol)
        
        # Calculate the step size for width increase per row
        if height <= 1:
            return symbol * width
        
        step = width / height
        result = []
        
        for i in range(height):
            # Calculate current width based on current row
            current_width = max(1, round((i + 1) * step))
            result.append(symbol * current_width)
        
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing the pyramid.
            
        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_input(height=height, symbol=symbol)
        
        result = []
        # For each row, calculate padding and symbols needed
        for i in range(height):
            # Width of symbols at this row
            symbols_count = 2 * i + 1
            # Padding needed at the start of the row
            padding = height - i - 1
            result.append(' ' * padding + symbol * symbols_count)
        
        return '\n'.join(result)


def main():
    """
    Main function that demonstrates the ASCII art functionality.
    """
    ascii_art = AsciiArt()
    
    # Example usage of each method
    print("Square (4x4, '*'):")
    print(ascii_art.draw_square(4, '*'))
    print()
    
    print("Rectangle (5x3, '#'):")
    print(ascii_art.draw_rectangle(5, 3, '#'))
    print()
    
    print("Parallelogram (6x4, '@'):")
    print(ascii_art.draw_parallelogram(6, 4, '@'))
    print()
    
    print("Triangle (8x4, '+'):")
    print(ascii_art.draw_triangle(8, 4, '+'))
    print()
    
    print("Pyramid (5, '^'):")
    print(ascii_art.draw_pyramid(5, '^'))

if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}")
