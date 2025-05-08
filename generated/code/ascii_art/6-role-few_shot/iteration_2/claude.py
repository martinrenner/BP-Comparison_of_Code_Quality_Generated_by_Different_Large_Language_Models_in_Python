class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create different geometric shapes using ASCII characters.
    All shapes are represented as multi-line strings filled with a specified symbol.
    """
    
    @staticmethod
    def _validate_inputs(width: int, height: int, symbol: str) -> None:
        """
        Validates the input parameters for the drawing functions.
        
        Args:
            width (int): The width of the shape.
            height (int): The height of the shape.
            symbol (str): The character to use for drawing the shape.
            
        Raises:
            ValueError: If width or height is negative, or if symbol is not a single character.
            TypeError: If width or height is not an integer, or if symbol is not a string.
        """
        if not isinstance(width, int):
            raise TypeError("Width must be an integer.")
        if not isinstance(height, int):
            raise TypeError("Height must be an integer.")
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
            
        if width < 1:
            raise ValueError("Width must be positive.")
        if height < 1:
            raise ValueError("Height must be positive.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square with the specified width and symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The character to use for drawing the square.
            
        Returns:
            str: A multi-line string representing the square ASCII art.
            
        Raises:
            ValueError: If width is negative, or if symbol is not a single character.
            TypeError: If width is not an integer, or if symbol is not a string.
        """
        self._validate_inputs(width, width, symbol)
        return self.draw_rectangle(width, width, symbol)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle with the specified width, height, and symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing the rectangle.
            
        Returns:
            str: A multi-line string representing the rectangle ASCII art.
            
        Raises:
            ValueError: If width or height is negative, or if symbol is not a single character.
            TypeError: If width or height is not an integer, or if symbol is not a string.
        """
        self._validate_inputs(width, height, symbol)
        
        row = symbol * width
        return '\n'.join([row for _ in range(height)])
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified width, height, and symbol.
        
        The parallelogram grows diagonally to the right, with each row shifted by one space.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing the parallelogram.
            
        Returns:
            str: A multi-line string representing the parallelogram ASCII art.
            
        Raises:
            ValueError: If width or height is negative, or if symbol is not a single character.
            TypeError: If width or height is not an integer, or if symbol is not a string.
        """
        self._validate_inputs(width, height, symbol)
        
        result = []
        row = symbol * width
        for i in range(height):
            result.append(' ' * i + row)
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with the specified width, height, and symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The maximum width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The character to use for drawing the triangle.
            
        Returns:
            str: A multi-line string representing the triangle ASCII art.
            
        Raises:
            ValueError: If width or height is negative, or if symbol is not a single character.
            TypeError: If width or height is not an integer, or if symbol is not a string.
        """
        self._validate_inputs(width, height, symbol)
        
        result = []
        for i in range(height):
            # Calculate the width of the current row
            current_width = max(1, int(width * (i + 1) / height))
            result.append(symbol * current_width)
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the specified height and symbol.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing the pyramid.
            
        Returns:
            str: A multi-line string representing the pyramid ASCII art.
            
        Raises:
            ValueError: If height is negative, or if symbol is not a single character.
            TypeError: If height is not an integer, or if symbol is not a string.
        """
        self._validate_inputs(height, height, symbol)
        
        result = []
        for i in range(height):
            # Calculate the number of symbols and spaces for this row
            symbols = 2 * i + 1
            spaces = height - i - 1
            result.append(' ' * spaces + symbol * symbols)
        return '\n'.join(result)
