class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various ASCII art shapes
    such as squares, rectangles, parallelograms, triangles, and pyramids.
    Each shape is filled with a specified character symbol.
    """
    
    @staticmethod
    def _validate_input(width: int, height: int, symbol: str) -> None:
        """
        Validates the input parameters for all shape drawing methods.
        
        Args:
            width (int): Width of the shape.
            height (int): Height of the shape.
            symbol (str): Symbol to create the shape with.
            
        Raises:
            ValueError: If width or height is negative.
            ValueError: If symbol is empty, whitespace, or more than one character.
        """
        if width < 0 or height < 0:
            raise ValueError("Width and height must be non-negative integers.")
            
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
            
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): Width and height of the square.
            symbol (str): Symbol to create the square with.
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(width, width, symbol)
        
        if width == 0:
            return ""
            
        row = symbol * width
        return '\n'.join([row] * width)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width (int): Width of the rectangle.
            height (int): Height of the rectangle.
            symbol (str): Symbol to create the rectangle with.
            
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(width, height, symbol)
        
        if width == 0 or height == 0:
            return ""
            
        row = symbol * width
        return '\n'.join([row] * height)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, with each row
        shifted one space to the right relative to the previous row.
        
        Args:
            width (int): Width of the parallelogram.
            height (int): Height of the parallelogram.
            symbol (str): Symbol to create the parallelogram with.
            
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(width, height, symbol)
        
        if width == 0 or height == 0:
            return ""
            
        result = []
        for i in range(height):
            result.append(' ' * i + symbol * width)
            
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally from the top-left corner.
        
        Args:
            width (int): Width (base) of the triangle.
            height (int): Height of the triangle.
            symbol (str): Symbol to create the triangle with.
            
        Returns:
            str: A multi-line string representing the triangle.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(width, height, symbol)
        
        if width == 0 or height == 0:
            return ""
            
        result = []
        # Calculate width of each row to ensure proportional growth
        if height > 1:
            width_increment = width / (height - 1)
        else:
            width_increment = 0
            
        for i in range(height):
            # Calculate current row width and ensure it's an integer
            current_width = min(round(i * width_increment), width) if height > 1 else width
            current_width = max(1, current_width)  # Ensure minimum width of 1
            result.append(symbol * current_width)
            
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        Args:
            height (int): Height of the pyramid.
            symbol (str): Symbol to create the pyramid with.
            
        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If input validation fails.
        """
        # For pyramid, width is determined by height, so we use 0 as a placeholder for _validate_input
        self._validate_input(0, height, symbol)
        
        if height == 0:
            return ""
            
        result = []
        for i in range(height):
            # Calculate number of symbols for the current row
            symbols_count = 2 * i + 1
            # Calculate total width of the pyramid
            total_width = 2 * height - 1
            # Calculate padding on each side
            padding = (total_width - symbols_count) // 2
            
            result.append(' ' * padding + symbol * symbols_count)
            
        return '\n'.join(result)
