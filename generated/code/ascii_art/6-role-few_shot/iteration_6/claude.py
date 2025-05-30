class AsciiArt:
    """
    A class for creating ASCII art shapes.
    
    This class provides methods to generate various ASCII shapes
    such as squares, rectangles, parallelograms, triangles, and pyramids.
    """
    
    @staticmethod
    def _validate_input(symbol: str, width: int = None, height: int = None) -> None:
        """
        Validates the input parameters for ASCII art generation.
        
        Args:
            symbol (str): The character to use for drawing the shape.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.
            
        Raises:
            ValueError: If symbol is not a single character or contains whitespace.
            ValueError: If width or height is negative or zero.
        """
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        
        if width is not None and width <= 0:
            raise ValueError("Width must be a positive integer.")
            
        if height is not None and height <= 0:
            raise ValueError("Height must be a positive integer.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square ASCII art.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The character to use for drawing the square.
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, width)
        
        # Create a square by drawing 'width' rows, each with 'width' symbols
        rows = [symbol * width for _ in range(width)]
        return '\n'.join(rows)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangular ASCII art.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing the rectangle.
            
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, width, height)
        
        # Create a rectangle by drawing 'height' rows, each with 'width' symbols
        rows = [symbol * width for _ in range(height)]
        return '\n'.join(rows)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram ASCII art.
        
        The parallelogram grows diagonally to the right, with each row
        shifted one space to the right compared to the row above it.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing the parallelogram.
            
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, width, height)
        
        # Create a parallelogram by adding spaces at the beginning of each row
        rows = []
        for i in range(height):
            # Add i spaces, then add width symbols
            rows.append(' ' * i + symbol * width)
        
        return '\n'.join(rows)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle ASCII art.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The character to use for drawing the triangle.
            
        Returns:
            str: A multi-line string representing the triangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, width, height)
        
        rows = []
        # Calculate how many symbols to add per row
        step = width / height if height > 1 else width
        
        for i in range(height):
            # Calculate how many symbols to draw in this row
            # We use min to ensure we don't exceed the width
            symbols_count = min(width, round((i + 1) * step))
            rows.append(symbol * symbols_count)
        
        return '\n'.join(rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid ASCII art.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing the pyramid.
            
        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, height=height)
        
        rows = []
        for i in range(height):
            # Calculate spaces on left side and symbols in this row
            spaces = height - i - 1
            symbols_count = 2 * i + 1
            
            # Construct the row with proper spacing and symbols
            row = ' ' * spaces + symbol * symbols_count
            rows.append(row)
        
        return '\n'.join(rows)


if __name__ == "__main__":
    ascii_art = AsciiArt()
    square = ascii_art.draw_square(5, "*")
    print(square)
    print("\n" + ascii_art.draw_pyramid(4, "#"))
