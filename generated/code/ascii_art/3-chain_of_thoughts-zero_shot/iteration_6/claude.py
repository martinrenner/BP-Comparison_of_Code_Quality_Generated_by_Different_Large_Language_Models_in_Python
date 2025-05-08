class AsciiArt:
    """
    A class to generate various ASCII art shapes.
    
    This class provides methods to create common geometric shapes using ASCII characters.
    All methods validate inputs and return multi-line strings representing the requested shape.
    """
    
    @staticmethod
    def _validate_input(width=None, height=None, symbol=None):
        """
        Validates the input parameters for ASCII art generation.
        
        Args:
            width (int, optional): Width of the shape
            height (int, optional): Height of the shape
            symbol (str, optional): Character to use for drawing
            
        Raises:
            ValueError: If inputs don't meet requirements
            TypeError: If inputs are of incorrect type
        """
        # Validate symbol
        if symbol is not None:
            if not isinstance(symbol, str):
                raise TypeError("Symbol must be a string")
            if len(symbol) != 1:
                raise ValueError("Symbol must be exactly one character")
            if symbol.isspace():
                raise ValueError("Symbol cannot be whitespace")
                
        # Validate dimensions
        for name, value in [('width', width), ('height', height)]:
            if value is not None:
                if not isinstance(value, int):
                    raise TypeError(f"{name.capitalize()} must be an integer")
                if value <= 0:
                    raise ValueError(f"{name.capitalize()} must be a positive integer")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): Width and height of the square
            symbol (str): Character to use for drawing
            
        Returns:
            str: Multi-line string representing a square
            
        Raises:
            ValueError: If width is negative or symbol is invalid
            TypeError: If inputs are of incorrect type
        """
        self._validate_input(width=width, symbol=symbol)
        
        # Create a square by repeating the symbol
        row = symbol * width
        square = '\n'.join([row for _ in range(width)])
        return square
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width (int): Width of the rectangle
            height (int): Height of the rectangle
            symbol (str): Character to use for drawing
            
        Returns:
            str: Multi-line string representing a rectangle
            
        Raises:
            ValueError: If dimensions are negative or symbol is invalid
            TypeError: If inputs are of incorrect type
        """
        self._validate_input(width=width, height=height, symbol=symbol)
        
        # Create a rectangle by repeating the symbol
        row = symbol * width
        rectangle = '\n'.join([row for _ in range(height)])
        return rectangle
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): Width of the parallelogram
            height (int): Height of the parallelogram
            symbol (str): Character to use for drawing
            
        Returns:
            str: Multi-line string representing a parallelogram
            
        Raises:
            ValueError: If dimensions are negative or symbol is invalid
            TypeError: If inputs are of incorrect type
        """
        self._validate_input(width=width, height=height, symbol=symbol)
        
        # Each row is shifted by one space to the right
        rows = []
        for i in range(height):
            rows.append(' ' * i + symbol * width)
        
        return '\n'.join(rows)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): Width of the triangle base
            height (int): Height of the triangle
            symbol (str): Character to use for drawing
            
        Returns:
            str: Multi-line string representing a right-angled triangle
            
        Raises:
            ValueError: If dimensions are negative or symbol is invalid
            TypeError: If inputs are of incorrect type
        """
        self._validate_input(width=width, height=height, symbol=symbol)
        
        # Ensure the triangle is well-formed
        if width < height:
            raise ValueError("Width must be greater than or equal to height for a proper right triangle")
        
        # Calculate width growth per row
        width_per_row = width / height if height > 1 else width
        
        rows = []
        for i in range(height):
            # Calculate the width for this row, ensuring proper growth
            row_width = max(1, int((i + 1) * width_per_row))
            rows.append(symbol * row_width)
        
        return '\n'.join(rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        Args:
            height (int): Height of the pyramid
            symbol (str): Character to use for drawing
            
        Returns:
            str: Multi-line string representing a pyramid
            
        Raises:
            ValueError: If height is negative or symbol is invalid
            TypeError: If inputs are of incorrect type
        """
        self._validate_input(height=height, symbol=symbol)
        
        rows = []
        for i in range(height):
            # Calculate spaces and symbols
            spaces = ' ' * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            rows.append(spaces + symbols)
        
        return '\n'.join(rows)


def main():
    """
    Main function to demonstrate the ASCII Art generator.
    """
    ascii_art = AsciiArt()
    
    # Example usage
    print("\nSquare (5x5):")
    print(ascii_art.draw_square(5, '#'))
    
    print("\nRectangle (8x3):")
    print(ascii_art.draw_rectangle(8, 3, '*'))
    
    print("\nParallelogram (6x4):")
    print(ascii_art.draw_parallelogram(6, 4, '@'))
    
    print("\nTriangle (6x4):")
    print(ascii_art.draw_triangle(6, 4, '+'))
    
    print("\nPyramid (5):")
    print(ascii_art.draw_pyramid(5, '^'))
    
    # Interactive mode
    try:
        print("\n=== ASCII Art Generator ===")
        print("1. Square")
        print("2. Rectangle")
        print("3. Parallelogram")
        print("4. Triangle")
        print("5. Pyramid")
        
        choice = int(input("\nSelect shape (1-5): "))
        symbol = input("Enter symbol (single character): ")
        
        if choice == 1:
            width = int(input("Enter width: "))
            print(ascii_art.draw_square(width, symbol))
        elif choice == 2:
            width = int(input("Enter width: "))
            height = int(input("Enter height: "))
            print(ascii_art.draw_rectangle(width, height, symbol))
        elif choice == 3:
            width = int(input("Enter width: "))
            height = int(input("Enter height: "))
            print(ascii_art.draw_parallelogram(width, height, symbol))
        elif choice == 4:
            width = int(input("Enter width: "))
            height = int(input("Enter height: "))
            print(ascii_art.draw_triangle(width, height, symbol))
        elif choice == 5:
            height = int(input("Enter height: "))
            print(ascii_art.draw_pyramid(height, symbol))
        else:
            print("Invalid choice!")
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
