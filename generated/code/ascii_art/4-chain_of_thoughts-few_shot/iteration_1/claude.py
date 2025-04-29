class AsciiArt:
    """
    A class for generating various ASCII art shapes.
    
    This class implements various methods to generate ASCII art shapes
    such as squares, rectangles, parallelograms, triangles, and pyramids.
    Each method validates inputs and returns a multi-line string representation
    of the requested shape.
    """
    
    @staticmethod
    def _validate_inputs(symbol: str, *dimensions: int) -> None:
        """
        Validates the inputs for all shape drawing methods.
        
        Args:
            symbol (str): The symbol to use for drawing the shape.
            *dimensions: Variable length argument list containing dimensions (width, height).
            
        Raises:
            ValueError: If symbol is not exactly one character or is whitespace.
            ValueError: If any dimension is negative or zero.
        """
        # Validate the symbol
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
            
        # Validate dimensions (width, height)
        for dimension in dimensions:
            if dimension <= 0:
                raise ValueError("Dimensions must be positive integers.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The symbol to use for drawing the square.
            
        Returns:
            str: A multi-line string representation of the square.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, width)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        # Return a string with 'width' number of rows
        return '\n'.join([row for _ in range(width)])
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing the rectangle.
            
        Returns:
            str: A multi-line string representation of the rectangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, width, height)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        # Return a string with 'height' number of rows
        return '\n'.join([row for _ in range(height)])
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        The parallelogram grows diagonally to the right, with each row shifted by one space.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing the parallelogram.
            
        Returns:
            str: A multi-line string representation of the parallelogram.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, width, height)
        
        result = []
        for i in range(height):
            # Add spaces to shift each row to the right
            spaces = ' ' * i
            # Create a row of symbols with the specified width
            row = spaces + symbol * width
            result.append(row)
            
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol to use for drawing the triangle.
            
        Returns:
            str: A multi-line string representation of the triangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, width, height)
        
        # Calculate the step size for increasing width
        if height <= 1:
            step = 0
        else:
            step = (width - 1) / (height - 1) if height > 1 else 0
            
        result = []
        for i in range(height):
            # Calculate the number of symbols for this row
            symbols_count = 1 + int(i * step)
            row = symbol * symbols_count
            result.append(row)
            
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing the pyramid.
            
        Returns:
            str: A multi-line string representation of the pyramid.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, height)
        
        result = []
        for i in range(height):
            # Calculate spaces and symbols for each row
            spaces = ' ' * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            row = spaces + symbols
            result.append(row)
            
        return '\n'.join(result)


def main():
    """
    Main function to demonstrate the ASCII Art generator capabilities.
    """
    art = AsciiArt()
    
    try:
        print("\nSquare (4x4):")
        print(art.draw_square(4, "#"))
        
        print("\nRectangle (6x3):")
        print(art.draw_rectangle(6, 3, "*"))
        
        print("\nParallelogram (5x3):")
        print(art.draw_parallelogram(5, 3, "+"))
        
        print("\nTriangle (5x5):")
        print(art.draw_triangle(5, 5, ">"))
        
        print("\nPyramid (height 5):")
        print(art.draw_pyramid(5, "^"))
        
        # Uncomment below lines to test validation errors
        # print(art.draw_square(4, "##"))  # Multi-character symbol
        # print(art.draw_rectangle(5, -2, "*"))  # Negative dimension
        # print(art.draw_parallelogram(3, 4, " "))  # Whitespace symbol
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
