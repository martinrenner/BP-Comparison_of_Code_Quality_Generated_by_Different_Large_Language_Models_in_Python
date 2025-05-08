class AsciiArt:
    """
    A class for creating ASCII art shapes.
    
    This class provides methods to draw various ASCII art shapes such as squares,
    rectangles, parallelograms, triangles, and pyramids using a specified symbol.
    """
    
    @staticmethod
    def _validate_input(width: int, height: int, symbol: str) -> None:
        """
        Validates the input parameters for ASCII art generation.
        
        Args:
            width: The width of the shape.
            height: The height of the shape.
            symbol: The character to use for drawing the shape.
            
        Raises:
            ValueError: If width or height is negative, or if symbol is not a single character.
            TypeError: If width or height is not an integer, or if symbol is not a string.
        """
        # Validate types
        if not isinstance(width, int):
            raise TypeError("Width must be an integer.")
        if not isinstance(height, int):
            raise TypeError("Height must be an integer.")
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        
        # Validate values
        if width < 1:
            raise ValueError("Width must be a positive integer.")
        if height < 1:
            raise ValueError("Height must be a positive integer.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square with the specified width using the given symbol.
        
        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing.
            
        Returns:
            A multi-line string representation of the square.
            
        Raises:
            ValueError: If width is negative or symbol is not a single character.
            TypeError: If width is not an integer or symbol is not a string.
        """
        self._validate_input(width, width, symbol)
        return self.draw_rectangle(width, width, symbol)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle with the specified dimensions using the given symbol.
        
        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.
            
        Returns:
            A multi-line string representation of the rectangle.
            
        Raises:
            ValueError: If width or height is negative, or if symbol is not a single character.
            TypeError: If width or height is not an integer, or if symbol is not a string.
        """
        self._validate_input(width, height, symbol)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        
        # Create the rectangle by repeating the row for the specified height
        return '\n'.join([row for _ in range(height)])
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified dimensions using the given symbol.
        
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        Each row is shifted by one space to the right.
        
        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.
            
        Returns:
            A multi-line string representation of the parallelogram.
            
        Raises:
            ValueError: If width or height is negative, or if symbol is not a single character.
            TypeError: If width or height is not an integer, or if symbol is not a string.
        """
        self._validate_input(width, height, symbol)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        
        # Create the parallelogram by shifting each row to the right
        return '\n'.join([' ' * i + row for i in range(height)])
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with the specified dimensions using the given symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width: The base width of the triangle.
            height: The height of the triangle.
            symbol: The character to use for drawing.
            
        Returns:
            A multi-line string representation of the triangle.
            
        Raises:
            ValueError: If width or height is negative, or if symbol is not a single character.
            TypeError: If width or height is not an integer, or if symbol is not a string.
        """
        self._validate_input(width, height, symbol)
        
        result = []
        # Calculate the increment of symbols per row
        increment = width / height
        
        for i in range(height):
            # Calculate the number of symbols to draw in this row
            symbols_count = int((i + 1) * increment)
            # Ensure we never exceed the width
            symbols_count = min(symbols_count, width)
            result.append(symbol * symbols_count)
        
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the specified height using the given symbol.
        
        Args:
            height: The height of the pyramid.
            symbol: The character to use for drawing.
            
        Returns:
            A multi-line string representation of the pyramid.
            
        Raises:
            ValueError: If height is negative, or if symbol is not a single character.
            TypeError: If height is not an integer, or if symbol is not a string.
        """
        self._validate_input(height * 2 - 1, height, symbol)
        
        result = []
        for i in range(height):
            # Calculate padding and symbols for each row
            symbols_count = 2 * i + 1
            padding = height - i - 1
            
            # Construct the row with proper padding and symbols
            row = ' ' * padding + symbol * symbols_count
            result.append(row)
        
        return '\n'.join(result)


def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    art = AsciiArt()
    
    try:
        # Example usage of each function
        print("Square (4x4 with '*'):")
        print(art.draw_square(4, '*'))
        
        print("\nRectangle (6x3 with '#'):")
        print(art.draw_rectangle(6, 3, '#'))
        
        print("\nParallelogram (5x3 with '@'):")
        print(art.draw_parallelogram(5, 3, '@'))
        
        print("\nTriangle (5x5 with '+'):")
        print(art.draw_triangle(5, 5, '+'))
        
        print("\nPyramid (4 height with '$'):")
        print(art.draw_pyramid(4, '$'))
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
