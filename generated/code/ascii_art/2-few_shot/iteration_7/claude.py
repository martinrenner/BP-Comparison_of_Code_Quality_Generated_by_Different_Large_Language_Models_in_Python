class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various ASCII art shapes
    filled with a user-specified symbol.
    """
    
    @staticmethod
    def _validate_input(width: int, height: int, symbol: str) -> None:
        """
        Validates the input parameters for all drawing methods.
        
        Args:
            width (int): The width of the shape.
            height (int): The height of the shape.
            symbol (str): The symbol to use for drawing.
            
        Raises:
            ValueError: If width or height is negative.
            ValueError: If symbol is not a single character.
            ValueError: If symbol is a whitespace character.
        """
        if width < 0:
            raise ValueError("Width must be a non-negative integer.")
        if height < 0:
            raise ValueError("Height must be a non-negative integer.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(width, width, symbol)
        
        if width == 0:
            return ""
        
        # Create a row of symbols
        row = symbol * width
        
        # Repeat the row for each line
        return '\n'.join([row for _ in range(width)])
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(width, height, symbol)
        
        if width == 0 or height == 0:
            return ""
        
        # Create a row of symbols
        row = symbol * width
        
        # Repeat the row for each line
        return '\n'.join([row for _ in range(height)])
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        Each row is shifted one space to the right from the previous row.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing.
            
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
            # Add spaces for the shift and then the symbols
            result.append(' ' * i + symbol * width)
        
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The base width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the triangle.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(width, height, symbol)
        
        if width == 0 or height == 0:
            return ""
        
        result = []
        # Calculate how much to increment each row
        if height == 1:
            increment = width
        else:
            increment = max(1, width // height)
        
        current_width = increment
        for i in range(height):
            # Ensure we don't exceed the specified width
            actual_width = min(current_width, width)
            result.append(symbol * actual_width)
            current_width += increment
        
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(height, height, symbol)
        
        if height == 0:
            return ""
        
        result = []
        for i in range(height):
            # Calculate spaces and symbols for each row
            spaces = ' ' * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            result.append(spaces + symbols)
        
        return '\n'.join(result)


def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    ascii_art = AsciiArt()
    
    print("ASCII Art Generator\n")
    
    # Demonstrate square
    print("Square (width=5, symbol='#'):")
    print(ascii_art.draw_square(5, '#'))
    print()
    
    # Demonstrate rectangle
    print("Rectangle (width=8, height=4, symbol='*'):")
    print(ascii_art.draw_rectangle(8, 4, '*'))
    print()
    
    # Demonstrate parallelogram
    print("Parallelogram (width=6, height=4, symbol='+'):")
    print(ascii_art.draw_parallelogram(6, 4, '+'))
    print()
    
    # Demonstrate triangle
    print("Triangle (width=6, height=4, symbol='@'):")
    print(ascii_art.draw_triangle(6, 4, '@'))
    print()
    
    # Demonstrate pyramid
    print("Pyramid (height=5, symbol='^'):")
    print(ascii_art.draw_pyramid(5, '^'))


if __name__ == "__main__":
    main()
