class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various ASCII art shapes
    filled with a user-specified symbol.
    """
    
    @staticmethod
    def _validate_input(symbol: str, *dimensions) -> None:
        """
        Validates input parameters for all drawing functions.
        
        Args:
            symbol (str): The symbol to use for drawing.
            *dimensions: Variable number of dimension parameters (width, height).
            
        Raises:
            ValueError: If symbol is not a single character or is whitespace.
            ValueError: If any dimension is negative.
        """
        # Validate symbol
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
            
        # Validate dimensions
        for i, dimension in enumerate(dimensions):
            if dimension < 1:
                dim_name = "width" if i == 0 else "height"
                raise ValueError(f"{dim_name.capitalize()} must be a positive integer.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The symbol to fill the square with.
            
        Returns:
            str: A multi-line string representing a square.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, width)
        
        # Create a square by repeating the symbol
        row = symbol * width
        return '\n'.join([row] * width)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to fill the rectangle with.
            
        Returns:
            str: A multi-line string representing a rectangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, width, height)
        
        # Create a rectangle by repeating the symbol
        row = symbol * width
        return '\n'.join([row] * height)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, with each row
        shifted one space to the right.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to fill the parallelogram with.
            
        Returns:
            str: A multi-line string representing a parallelogram.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, width, height)
        
        result = []
        row = symbol * width
        
        for i in range(height):
            # Add leading spaces according to the current row
            result.append(' ' * i + row)
            
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The maximum width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol to fill the triangle with.
            
        Returns:
            str: A multi-line string representing a right-angled triangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, width, height)
        
        result = []
        # Calculate width increments per row
        width_increment = width / height
        
        for i in range(height):
            # Calculate the number of symbols for the current row
            symbols_count = round((i + 1) * width_increment)
            result.append(symbol * symbols_count)
            
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to fill the pyramid with.
            
        Returns:
            str: A multi-line string representing a pyramid.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, height)
        
        result = []
        # The width of the pyramid at the base is (2 * height - 1)
        width = 2 * height - 1
        
        for i in range(height):
            # Calculate the number of symbols for the current row
            symbols_count = 2 * i + 1
            # Calculate padding to center the symbols
            padding = (width - symbols_count) // 2
            
            line = ' ' * padding + symbol * symbols_count
            result.append(line)
            
        return '\n'.join(result)


def main():
    """Demo function to showcase the ASCII Art generator."""
    art = AsciiArt()
    
    print("\n=== ASCII Art Generator ===\n")
    
    print("Square (4x4):")
    print(art.draw_square(4, '*'))
    
    print("\nRectangle (6x3):")
    print(art.draw_rectangle(6, 3, '#'))
    
    print("\nParallelogram (5x3):")
    print(art.draw_parallelogram(5, 3, '@'))
    
    print("\nTriangle (5x5):")
    print(art.draw_triangle(5, 5, '+'))
    
    print("\nPyramid (height 4):")
    print(art.draw_pyramid(4, '^'))
    
    print("\nCustom shape:")
    try:
        symbol = input("Enter a single character symbol: ")
        shape_type = input("Choose shape (square, rectangle, parallelogram, triangle, pyramid): ").lower()
        
        if shape_type == "square":
            width = int(input("Enter width: "))
            print(art.draw_square(width, symbol))
        elif shape_type == "rectangle":
            width = int(input("Enter width: "))
            height = int(input("Enter height: "))
            print(art.draw_rectangle(width, height, symbol))
        elif shape_type == "parallelogram":
            width = int(input("Enter width: "))
            height = int(input("Enter height: "))
            print(art.draw_parallelogram(width, height, symbol))
        elif shape_type == "triangle":
            width = int(input("Enter width: "))
            height = int(input("Enter height: "))
            print(art.draw_triangle(width, height, symbol))
        elif shape_type == "pyramid":
            height = int(input("Enter height: "))
            print(art.draw_pyramid(height, symbol))
        else:
            print("Invalid shape type.")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
