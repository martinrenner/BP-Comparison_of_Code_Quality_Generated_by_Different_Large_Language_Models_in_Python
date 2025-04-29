class AsciiArt:
    """
    A class for creating 2D ASCII art shapes.
    
    This class provides methods to draw various ASCII art shapes including squares,
    rectangles, parallelograms, triangles, and pyramids using specified symbols.
    """

    @staticmethod
    def _validate_input(width=None, height=None, symbol=None):
        """
        Validates the input parameters for drawing ASCII shapes.
        
        Args:
            width (int, optional): Width of the shape.
            height (int, optional): Height of the shape.
            symbol (str, optional): Symbol to use for drawing.
            
        Raises:
            ValueError: If inputs don't meet requirements (negative dimensions,
                      multi-character or whitespace symbol).
        """
        # Validate dimensions
        if width is not None and width <= 0:
            raise ValueError("Width must be a positive integer.")
        if height is not None and height <= 0:
            raise ValueError("Height must be a positive integer.")
        
        # Validate symbol
        if symbol is not None:
            if len(symbol) != 1:
                raise ValueError("Symbol must be a single character.")
            if symbol.isspace():
                raise ValueError("Symbol cannot be a whitespace character.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The symbol to use for drawing (single character).
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If width is not positive or symbol is invalid.
        """
        self._validate_input(width=width, symbol=symbol)
        
        # Create a square by drawing 'width' rows, each with 'width' symbols
        return '\n'.join([symbol * width] * width)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing (single character).
            
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If width/height is not positive or symbol is invalid.
        """
        self._validate_input(width=width, height=height, symbol=symbol)
        
        # Create a rectangle by drawing 'height' rows, each with 'width' symbols
        return '\n'.join([symbol * width] * height)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, with each row shifted
        by one space compared to the row above it.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing (single character).
            
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If width/height is not positive or symbol is invalid.
        """
        self._validate_input(width=width, height=height, symbol=symbol)
        
        # Create a parallelogram with each row shifted by one space
        result = []
        for i in range(height):
            result.append(' ' * i + symbol * width)
        
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The base width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol to use for drawing (single character).
            
        Returns:
            str: A multi-line string representing the right-angled triangle.
            
        Raises:
            ValueError: If width/height is not positive or symbol is invalid.
        """
        self._validate_input(width=width, height=height, symbol=symbol)
        
        result = []
        for i in range(height):
            # Calculate how many symbols to draw in this row based on height and width
            symbols_in_row = max(1, int(width * ((i + 1) / height)))
            result.append(symbol * symbols_in_row)
        
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing (single character).
            
        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_input(height=height, symbol=symbol)
        
        result = []
        for i in range(height):
            # Calculate spaces and symbols for current row
            spaces = height - i - 1
            symbols = 2 * i + 1
            result.append(' ' * spaces + symbol * symbols)
        
        return '\n'.join(result)


def main():
    """
    Main function to demonstrate the ASCII art functionality.
    """
    ascii_art = AsciiArt()
    
    try:
        print("\nASCII Art Generator\n")
        print("1. Square")
        print("2. Rectangle")
        print("3. Parallelogram")
        print("4. Triangle")
        print("5. Pyramid")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-5): ")
        
        if choice == '0':
            print("Exiting the program. Goodbye!")
            return
            
        symbol = input("Enter a symbol to use (single character): ")
        
        if choice == '1':
            width = int(input("Enter width: "))
            print("\nSquare:")
            print(ascii_art.draw_square(width, symbol))
            
        elif choice == '2':
            width = int(input("Enter width: "))
            height = int(input("Enter height: "))
            print("\nRectangle:")
            print(ascii_art.draw_rectangle(width, height, symbol))
            
        elif choice == '3':
            width = int(input("Enter width: "))
            height = int(input("Enter height: "))
            print("\nParallelogram:")
            print(ascii_art.draw_parallelogram(width, height, symbol))
            
        elif choice == '4':
            width = int(input("Enter width: "))
            height = int(input("Enter height: "))
            print("\nTriangle:")
            print(ascii_art.draw_triangle(width, height, symbol))
            
        elif choice == '5':
            height = int(input("Enter height: "))
            print("\nPyramid:")
            print(ascii_art.draw_pyramid(height, symbol))
            
        else:
            print("Invalid choice. Please select a number between 0 and 5.")
            
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
