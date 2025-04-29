class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various ASCII art shapes using a specified symbol.
    Each shape is returned as a multi-line string that can be printed to the console.
    """
    
    @staticmethod
    def _validate_input(width: int, height: int, symbol: str) -> None:
        """
        Validates the input parameters for ASCII art generation.
        
        Args:
            width (int): The width of the shape.
            height (int): The height of the shape.
            symbol (str): The symbol to use for drawing.
            
        Raises:
            ValueError: If width or height is negative, or if symbol is not a single character.
            TypeError: If width or height is not an integer, or if symbol is not a string.
        """
        # Validate types
        if not isinstance(width, int):
            raise TypeError("Width must be an integer")
        if not isinstance(height, int):
            raise TypeError("Height must be an integer")
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string")
            
        # Validate values
        if width < 0:
            raise ValueError("Width must be a non-negative integer")
        if height < 0:
            raise ValueError("Height must be a non-negative integer")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")

    @classmethod
    def draw_square(cls, width: int, symbol: str) -> str:
        """
        Draws a square ASCII art shape.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If width is negative, or if symbol is not a single character.
            TypeError: If width is not an integer, or if symbol is not a string.
        """
        cls._validate_input(width, width, symbol)
        
        if width == 0:
            return ""
        
        # Create a square by repeating the symbol
        row = symbol * width
        return "\n".join([row] * width)
    
    @classmethod
    def draw_rectangle(cls, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangular ASCII art shape.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If width or height is negative, or if symbol is not a single character.
            TypeError: If width or height is not an integer, or if symbol is not a string.
        """
        cls._validate_input(width, height, symbol)
        
        if width == 0 or height == 0:
            return ""
        
        # Create a rectangle by repeating the symbol
        row = symbol * width
        return "\n".join([row] * height)
    
    @classmethod
    def draw_parallelogram(cls, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram ASCII art shape.
        Each row is shifted one space to the right from the previous row.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If width or height is negative, or if symbol is not a single character.
            TypeError: If width or height is not an integer, or if symbol is not a string.
        """
        cls._validate_input(width, height, symbol)
        
        if width == 0 or height == 0:
            return ""
        
        # Create a parallelogram by shifting each row
        result = []
        row = symbol * width
        for i in range(height):
            result.append(" " * i + row)
        
        return "\n".join(result)
    
    @classmethod
    def draw_triangle(cls, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle ASCII art shape.
        
        Args:
            width (int): The base width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the right-angled triangle.
            
        Raises:
            ValueError: If width or height is negative, or if symbol is not a single character.
            TypeError: If width or height is not an integer, or if symbol is not a string.
        """
        cls._validate_input(width, height, symbol)
        
        if width == 0 or height == 0:
            return ""
        
        # Calculate width increment per row
        if height == 1:
            increment = width
        else:
            increment = width / (height - 1)
        
        result = []
        for i in range(height):
            # Calculate symbols to draw in this row (rounded to nearest int)
            symbols_count = min(round(increment * i), width) if i < height - 1 else width
            result.append(symbol * symbols_count)
        
        return "\n".join(result)
    
    @classmethod
    def draw_pyramid(cls, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid ASCII art shape.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the symmetrical pyramid.
            
        Raises:
            ValueError: If height is negative, or if symbol is not a single character.
            TypeError: If height is not an integer, or if symbol is not a string.
        """
        cls._validate_input(height, height, symbol)
        
        if height == 0:
            return ""
        
        result = []
        for i in range(height):
            # Calculate number of symbols and spaces for this row
            symbols_count = 2 * i + 1
            padding = height - i - 1
            
            # Create the row with proper padding and symbols
            row = " " * padding + symbol * symbols_count
            result.append(row)
        
        return "\n".join(result)
