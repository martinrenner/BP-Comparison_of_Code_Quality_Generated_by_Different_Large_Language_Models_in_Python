class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various ASCII art shapes such as
    squares, rectangles, triangles, parallelograms, and pyramids.
    """
    
    def __init__(self):
        """Initialize the AsciiArt class."""
        pass
    
    @staticmethod
    def _validate_inputs(symbol: str, *dimensions: int) -> None:
        """
        Validate the input parameters for the ASCII art functions.
        
        Args:
            symbol (str): The character to use for drawing.
            *dimensions (int): One or more dimensions (width, height, etc.).
            
        Raises:
            ValueError: If the symbol is not a single character or is a whitespace.
            ValueError: If any dimension is negative or zero.
        """
        # Validate the symbol
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        
        # Validate dimensions
        for dimension in dimensions:
            if dimension <= 0:
                raise ValueError("Dimensions must be positive integers.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square using the specified symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If the inputs are invalid.
        """
        self._validate_inputs(symbol, width)
        
        rows = []
        for _ in range(width):
            rows.append(symbol * width)
        
        return '\n'.join(rows)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle using the specified symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If the inputs are invalid.
        """
        self._validate_inputs(symbol, width, height)
        
        rows = []
        for _ in range(height):
            rows.append(symbol * width)
        
        return '\n'.join(rows)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram using the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        Each row is shifted by one space to the right.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If the inputs are invalid.
        """
        self._validate_inputs(symbol, width, height)
        
        rows = []
        for i in range(height):
            rows.append(' ' * i + symbol * width)
        
        return '\n'.join(rows)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle using the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the triangle.
            
        Raises:
            ValueError: If the inputs are invalid.
        """
        self._validate_inputs(symbol, width, height)
        
        rows = []
        for i in range(1, height + 1):
            # Calculate the number of symbols for this row
            symbols_count = max(1, int(i * width / height))
            rows.append(symbol * symbols_count)
        
        return '\n'.join(rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid using the specified symbol.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If the inputs are invalid.
        """
        self._validate_inputs(symbol, height)
        
        rows = []
        for i in range(height):
            # Calculate spaces and symbols
            spaces = ' ' * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            rows.append(spaces + symbols)
        
        return '\n'.join(rows)
