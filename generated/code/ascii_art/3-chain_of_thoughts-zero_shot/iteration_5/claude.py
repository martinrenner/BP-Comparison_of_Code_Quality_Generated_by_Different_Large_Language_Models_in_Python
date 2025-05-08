class AsciiArt:
    """
    A class to generate various ASCII art shapes.
    
    This class provides methods to draw different shapes using ASCII characters,
    including squares, rectangles, parallelograms, triangles, and pyramids.
    """
    
    def __init__(self):
        """Initialize the AsciiArt class."""
        pass
    
    def _validate_input(self, symbol: str, *dimensions: int) -> None:
        """
        Validate the input parameters for all drawing functions.
        
        Args:
            symbol (str): The character to use for drawing.
            *dimensions (int): The dimensions (width, height) of the shape.
            
        Raises:
            ValueError: If symbol is not exactly one character or if it's whitespace.
            ValueError: If any dimension is negative or zero.
        """
        # Validate symbol
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
        
        # Validate dimensions
        for dimension in dimensions:
            if dimension <= 0:
                raise ValueError("Dimensions must be positive integers")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, width)
        
        # Create each line of the square with the symbol repeated 'width' times
        square_line = symbol * width
        # Join 'width' number of lines to form a square
        return '\n'.join([square_line for _ in range(width)])
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, width, height)
        
        # Create each line of the rectangle with the symbol repeated 'width' times
        rectangle_line = symbol * width
        # Join 'height' number of lines to form a rectangle
        return '\n'.join([rectangle_line for _ in range(height)])
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, with each row shifted
        by one space to the right.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, width, height)
        
        result = []
        for i in range(height):
            # Add 'i' spaces before each line, then 'width' symbols
            result.append(' ' * i + symbol * width)
            
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top.
        
        Args:
            width (int): The base width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the triangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, width, height)
        
        result = []
        # Calculate how much the width grows with each row
        width_step = width / height if height > 0 else 0
        
        for i in range(height):
            # Calculate current width, rounding to ensure integer number of symbols
            current_width = round((i + 1) * width_step)
            result.append(symbol * current_width)
            
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered and grows wider toward the bottom.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(symbol, height)
        
        result = []
        for i in range(height):
            # Calculate spaces and symbols for each row to create a symmetric pyramid
            # The width of symbols at each row is 2*i + 1 to create an odd number
            # of symbols that increases by 2 with each row
            spaces = ' ' * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            result.append(spaces + symbols)
            
        return '\n'.join(result)


# Example usage and demo function
def demo():
    """
    Demonstrate the AsciiArt class by drawing various shapes.
    """
    art = AsciiArt()
    
    print("ASCII Art Examples\n")
    
    print("Square (4x4, using '#'):")
    print(art.draw_square(4, "#"))
    print()
    
    print("Rectangle (6x3, using '*'):")
    print(art.draw_rectangle(6, 3, "*"))
    print()
    
    print("Parallelogram (5x3, using '@'):")
    print(art.draw_parallelogram(5, 3, "@"))
    print()
    
    print("Triangle (5x3, using '$'):")
    print(art.draw_triangle(5, 3, "$"))
    print()
    
    print("Pyramid (5 height, using '^'):")
    print(art.draw_pyramid(5, "^"))
    print()
    
    # Testing error handling
    try:
        art.draw_square(-1, "#")
    except ValueError as e:
        print(f"Error caught: {e}")
    
    try:
        art.draw_rectangle(5, 3, "  ")
    except ValueError as e:
        print(f"Error caught: {e}")


if __name__ == "__main__":
    try:
        demo()
        
        # Interactive mode
        print("\nInteractive Mode:")
        ascii_art = AsciiArt()
        
        while True:
            print("\nChoose a shape to draw:")
            print("1. Square")
            print("2. Rectangle")
            print("3. Parallelogram")
            print("4. Triangle")
            print("5. Pyramid")
            print("6. Exit")
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == '6':
                print("Exiting program...")
                break
            
            try:
                symbol = input("Enter a single character to draw with: ")
                
                if choice == '1':
                    width = int(input("Enter width: "))
                    print("\nResult:")
                    print(ascii_art.draw_square(width, symbol))
                    
                elif choice == '2':
                    width = int(input("Enter width: "))
                    height = int(input("Enter height: "))
                    print("\nResult:")
                    print(ascii_art.draw_rectangle(width, height, symbol))
                    
                elif choice == '3':
                    width = int(input("Enter width: "))
                    height = int(input("Enter height: "))
                    print("\nResult:")
                    print(ascii_art.draw_parallelogram(width, height, symbol))
                    
                elif choice == '4':
                    width = int(input("Enter width: "))
                    height = int(input("Enter height: "))
                    print("\nResult:")
                    print(ascii_art.draw_triangle(width, height, symbol))
                    
                elif choice == '5':
                    height = int(input("Enter height: "))
                    print("\nResult:")
                    print(ascii_art.draw_pyramid(height, symbol))
                    
                else:
                    print("Invalid choice. Please enter a number between 1 and 6.")
                    
            except ValueError as e:
                print(f"Error: {e}")
                
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
