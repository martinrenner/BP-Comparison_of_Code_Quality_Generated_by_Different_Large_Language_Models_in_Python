class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various ASCII art shapes
    such as squares, rectangles, triangles, parallelograms, and pyramids.
    Each shape is filled with a user-specified symbol.
    """
    
    @staticmethod
    def _validate_input(width: int, height: int, symbol: str) -> None:
        """
        Validates the input parameters for all drawing functions.
        
        Args:
            width (int): The width of the shape.
            height (int): The height of the shape.
            symbol (str): The character to fill the shape with.
            
        Raises:
            ValueError: If the symbol is not a single character or is a whitespace.
            ValueError: If the width or height is negative.
        """
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        
        if width < 1 or height < 1:
            raise ValueError("Width and height must be positive integers.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The character to fill the square with.
            
        Returns:
            str: A multi-line string representing a square.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(width, width, symbol)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        
        # Join multiple rows to create the square
        return "\n".join([row for _ in range(width)])
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to fill the rectangle with.
            
        Returns:
            str: A multi-line string representing a rectangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(width, height, symbol)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        
        # Join multiple rows to create the rectangle
        return "\n".join([row for _ in range(height)])
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        Each row is shifted one space to the right compared to the row above it.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to fill the parallelogram with.
            
        Returns:
            str: A multi-line string representing a parallelogram.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(width, height, symbol)
        
        result = []
        for i in range(height):
            # Add spaces for the diagonal shift, then add the symbols
            row = " " * i + symbol * width
            result.append(row)
            
        return "\n".join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The maximum width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The character to fill the triangle with.
            
        Returns:
            str: A multi-line string representing a right-angled triangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(width, height, symbol)
        
        result = []
        # Calculate the number of symbols per row
        symbols_per_row = [int(i * (width / height) + 0.5) for i in range(1, height + 1)]
        
        for num_symbols in symbols_per_row:
            row = symbol * num_symbols
            result.append(row)
            
        return "\n".join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        The pyramid has a single symbol at the top and grows symmetrically
        in both directions. The width of the base is (2 * height - 1).
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to fill the pyramid with.
            
        Returns:
            str: A multi-line string representing a pyramid.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(height, height, symbol)
        
        result = []
        for i in range(1, height + 1):
            # Calculate spaces needed for centering and symbols for current row
            spaces = " " * (height - i)
            symbols = symbol * (2 * i - 1)
            
            # Combine spaces and symbols for the current row
            row = spaces + symbols
            result.append(row)
            
        return "\n".join(result)


def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    ascii_art = AsciiArt()
    
    try:
        print("Square (4x4 with '*'):")
        print(ascii_art.draw_square(4, "*"))
        print("\nRectangle (6x3 with '#'):")
        print(ascii_art.draw_rectangle(6, 3, "#"))
        print("\nParallelogram (5x3 with '@'):")
        print(ascii_art.draw_parallelogram(5, 3, "@"))
        print("\nTriangle (5x5 with '+'):")
        print(ascii_art.draw_triangle(5, 5, "+"))
        print("\nPyramid (4 high with '$'):")
        print(ascii_art.draw_pyramid(4, "$"))
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
