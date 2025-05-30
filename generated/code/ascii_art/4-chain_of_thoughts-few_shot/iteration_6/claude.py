class AsciiArt:
    """
    A class that provides functionality to create various ASCII art shapes.
    
    This class implements methods to draw squares, rectangles, parallelograms,
    right-angled triangles, and pyramids using ASCII characters.
    """
    
    @staticmethod
    def _validate_input(width: int, height: int, symbol: str) -> None:
        """
        Validates the input parameters for ASCII art generation.
        
        Args:
            width (int): The width of the shape.
            height (int): The height of the shape.
            symbol (str): The character to use for drawing.
            
        Raises:
            ValueError: If width or height is negative or zero.
            ValueError: If symbol is empty, whitespace, or more than one character.
        """
        # Validate width and height
        if width <= 0:
            raise ValueError("Width must be a positive integer")
        if height <= 0:
            raise ValueError("Height must be a positive integer")
        
        # Validate symbol
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the ASCII art square.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(width, width, symbol)
        
        # Create the square by repeating the symbol
        row = symbol * width
        return '\n'.join([row] * width)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the ASCII art rectangle.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(width, height, symbol)
        
        # Create the rectangle by repeating the symbol
        row = symbol * width
        return '\n'.join([row] * height)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, with each row
        shifted by one space relative to the previous row.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the ASCII art parallelogram.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(width, height, symbol)
        
        result = []
        for i in range(height):
            # Add spaces for the shift effect, then symbols for the width
            result.append(' ' * i + symbol * width)
        
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the 
        top-left corner.
        
        Args:
            width (int): The maximum width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the ASCII art triangle.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(width, height, symbol)
        
        result = []
        # Calculate the width increment per row to reach the target width by the end
        width_increment = max(1, width // height)
        
        for i in range(height):
            # Calculate current width, capped at maximum width
            current_width = min(width, (i + 1) * width_increment)
            result.append(symbol * current_width)
        
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing.
            
        Returns:
            str: A multi-line string representing the ASCII art pyramid.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(height, height, symbol)
        
        result = []
        for i in range(height):
            # Calculate spaces and symbols for each row to create a centered pyramid
            spaces = ' ' * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            result.append(spaces + symbols)
        
        return '\n'.join(result)


def main():
    """
    Main function to demonstrate the functionality of the AsciiArt class.
    """
    art = AsciiArt()
    
    print("\nASCII Art Generator")
    print("==================\n")
    
    try:
        # Demonstrate each shape with example parameters
        print("Square (4x4, using '#'):")
        print(art.draw_square(4, '#'))
        print("\nRectangle (6x3, using '*'):")
        print(art.draw_rectangle(6, 3, '*'))
        print("\nParallelogram (5x3, using '@'):")
        print(art.draw_parallelogram(5, 3, '@'))
        print("\nTriangle (5x5, using '+'):")
        print(art.draw_triangle(5, 5, '+'))
        print("\nPyramid (5 high, using '^'):")
        print(art.draw_pyramid(5, '^'))
        
        # Interactive mode
        print("\nEnter your own shapes (press Ctrl+C to exit):")
        while True:
            print("\nChoose a shape: ")
            print("1. Square")
            print("2. Rectangle")
            print("3. Parallelogram")
            print("4. Triangle")
            print("5. Pyramid")
            choice = input("Enter choice (1-5): ")
            
            if choice == '1':
                width = int(input("Enter width: "))
                symbol = input("Enter symbol: ")
                print(art.draw_square(width, symbol))
            elif choice == '2':
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                symbol = input("Enter symbol: ")
                print(art.draw_rectangle(width, height, symbol))
            elif choice == '3':
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                symbol = input("Enter symbol: ")
                print(art.draw_parallelogram(width, height, symbol))
            elif choice == '4':
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                symbol = input("Enter symbol: ")
                print(art.draw_triangle(width, height, symbol))
            elif choice == '5':
                height = int(input("Enter height: "))
                symbol = input("Enter symbol: ")
                print(art.draw_pyramid(height, symbol))
            else:
                print("Invalid choice, please try again.")
                
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting ASCII Art Generator. Goodbye!")


if __name__ == "__main__":
    main()
