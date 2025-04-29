class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to draw various ASCII art shapes
    including squares, rectangles, parallelograms, triangles, and pyramids.
    """
    
    @staticmethod
    def _validate_input(symbol: str, *dimensions: int) -> None:
        """
        Validates the input parameters for all drawing functions.
        
        Args:
            symbol (str): The character to use for drawing the shape.
            *dimensions (int): Variable number of dimension parameters (width, height, etc.).
            
        Raises:
            ValueError: If symbol is not a single character, is whitespace, or dimensions are negative.
            TypeError: If dimensions are not integers.
        """
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
            
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
            
        for dimension in dimensions:
            if not isinstance(dimension, int):
                raise TypeError(f"Dimension must be an integer, got {type(dimension).__name__}")
            if dimension <= 0:
                raise ValueError(f"Dimension must be positive, got {dimension}")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The character to use for drawing the square.
            
        Returns:
            str: A multi-line string representing the ASCII square.
            
        Raises:
            ValueError: If width is negative or symbol is invalid.
            TypeError: If width is not an integer.
        """
        self._validate_input(symbol, width)
        
        # For a square, we can reuse the rectangle method with equal dimensions
        return self.draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing the rectangle.
            
        Returns:
            str: A multi-line string representing the ASCII rectangle.
            
        Raises:
            ValueError: If width or height is negative or symbol is invalid.
            TypeError: If width or height is not an integer.
        """
        self._validate_input(symbol, width, height)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        
        # Repeat the row for the specified height, joining with newlines
        return '\n'.join([row] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        
        This draws a parallelogram where each row is shifted one space to the right
        compared to the row above it, starting from the top-left corner.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing the parallelogram.
            
        Returns:
            str: A multi-line string representing the ASCII parallelogram.
            
        Raises:
            ValueError: If width or height is negative or symbol is invalid.
            TypeError: If width or height is not an integer.
        """
        self._validate_input(symbol, width, height)
        
        rows = []
        for i in range(height):
            # Add increasing indentation for each row
            padding = ' ' * i
            row = padding + symbol * width
            rows.append(row)
            
        return '\n'.join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        
        This draws a triangle growing from top-left to bottom-right.
        
        Args:
            width (int): The base width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The character to use for drawing the triangle.
            
        Returns:
            str: A multi-line string representing the ASCII triangle.
            
        Raises:
            ValueError: If width or height is negative or symbol is invalid.
            TypeError: If width or height is not an integer.
        """
        self._validate_input(symbol, width, height)
        
        rows = []
        # Calculate the number of symbols to add per row
        symbols_per_row = width / height if height > 0 else 0
        
        for i in range(height):
            # Calculate how many symbols should be in the current row
            # using linear interpolation from 1 to width
            num_symbols = max(1, round(1 + i * symbols_per_row))
            row = symbol * num_symbols
            rows.append(row)
            
        return '\n'.join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing the pyramid.
            
        Returns:
            str: A multi-line string representing the ASCII pyramid.
            
        Raises:
            ValueError: If height is negative or symbol is invalid.
            TypeError: If height is not an integer.
        """
        self._validate_input(symbol, height)
        
        rows = []
        width = 2 * height - 1  # Width at the base of the pyramid
        
        for i in range(height):
            # Calculate number of symbols in the current row
            num_symbols = 2 * i + 1
            
            # Calculate padding to center the symbols
            padding = ' ' * ((width - num_symbols) // 2)
            
            # Create the row with symbols and padding
            row = padding + symbol * num_symbols
            rows.append(row)
            
        return '\n'.join(rows)
