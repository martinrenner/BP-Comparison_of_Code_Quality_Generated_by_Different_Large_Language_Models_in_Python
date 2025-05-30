class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various ASCII art shapes like squares,
    rectangles, triangles, parallelograms, and pyramids using a specified symbol.
    """
    
    @staticmethod
    def _validate_input(width: int = None, height: int = None, symbol: str = None):
        """
        Validate the input parameters for ASCII art generation.
        
        Args:
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.
            symbol (str, optional): The symbol to use for drawing.
            
        Raises:
            ValueError: If any parameter is invalid.
            TypeError: If any parameter has an incorrect type.
        """
        # Validate symbol
        if symbol is not None:
            if not isinstance(symbol, str):
                raise TypeError("Symbol must be a string")
            if len(symbol) != 1:
                raise ValueError("Symbol must be a single character")
            if symbol.isspace():
                raise ValueError("Symbol cannot be a whitespace character")
        
        # Validate width
        if width is not None:
            if not isinstance(width, int):
                raise TypeError("Width must be an integer")
            if width <= 0:
                raise ValueError("Width must be positive")
        
        # Validate height
        if height is not None:
            if not isinstance(height, int):
                raise TypeError("Height must be an integer")
            if height <= 0:
                raise ValueError("Height must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draw a square with the specified width and symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If width is not positive or symbol is invalid.
            TypeError: If parameters have incorrect types.
        """
        self._validate_input(width=width, symbol=symbol)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        
        # Create the square by repeating the row 'width' times
        square = '\n'.join([row for _ in range(width)])
        
        return square
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a rectangle with the specified width, height, and symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If width/height is not positive or symbol is invalid.
            TypeError: If parameters have incorrect types.
        """
        self._validate_input(width=width, height=height, symbol=symbol)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        
        # Create the rectangle by repeating the row 'height' times
        rectangle = '\n'.join([row for _ in range(height)])
        
        return rectangle
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a parallelogram with the specified width, height, and symbol.
        
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If width/height is not positive or symbol is invalid.
            TypeError: If parameters have incorrect types.
        """
        self._validate_input(width=width, height=height, symbol=symbol)
        
        # Create the parallelogram by shifting each row
        rows = []
        for i in range(height):
            # Add spaces for the shift, then add symbols for the width
            rows.append(' ' * i + symbol * width)
        
        return '\n'.join(rows)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draw a right-angled triangle with the specified width, height, and symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The maximum width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the triangle.
            
        Raises:
            ValueError: If width/height is not positive or symbol is invalid.
            TypeError: If parameters have incorrect types.
        """
        self._validate_input(width=width, height=height, symbol=symbol)
        
        # Calculate how many symbols to add per row
        symbols_per_row = max(1, width // height)
        
        rows = []
        for i in range(height):
            # Calculate the number of symbols for this row, but don't exceed width
            num_symbols = min((i + 1) * symbols_per_row, width)
            rows.append(symbol * num_symbols)
        
        return '\n'.join(rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draw a symmetrical pyramid with the specified height and symbol.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If height is not positive or symbol is invalid.
            TypeError: If parameters have incorrect types.
        """
        self._validate_input(height=height, symbol=symbol)
        
        # The width of the base of the pyramid is 2 * height - 1
        base_width = 2 * height - 1
        
        rows = []
        for i in range(height):
            # Calculate number of symbols for this row: 2*i + 1
            symbols_count = 2 * i + 1
            # Calculate padding to center the symbols
            padding = (base_width - symbols_count) // 2
            # Create the row with padding and symbols
            rows.append(' ' * padding + symbol * symbols_count)
        
        return '\n'.join(rows)


def main():
    """
    Main function to demonstrate the ASCII art generator.
    """
    ascii_art = AsciiArt()
    
    # Demonstrate each shape
    print("Square (3x3 with '*'):")
    print(ascii_art.draw_square(3, '*'))
    print("\nRectangle (5x2 with '#'):")
    print(ascii_art.draw_rectangle(5, 2, '#'))
    print("\nParallelogram (4x3 with '@'):")
    print(ascii_art.draw_parallelogram(4, 3, '@'))
    print("\nTriangle (5x3 with '+'):")
    print(ascii_art.draw_triangle(5, 3, '+'))
    print("\nPyramid (height=4 with '^'):")
    print(ascii_art.draw_pyramid(4, '^'))
    
    # Interactive mode
    print("\n===== ASCII Art Generator =====")
    while True:
        print("\nChoose a shape to draw:")
        print("1. Square")
        print("2. Rectangle")
        print("3. Parallelogram")
        print("4. Triangle")
        print("5. Pyramid")
        print("6. Exit")
        
        try:
            choice = int(input("Enter your choice (1-6): "))
            
            if choice == 6:
                print("Goodbye!")
                break
                
            symbol = input("Enter a single character to use: ")
            
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
                width = int(input("Enter max width: "))
                height = int(input("Enter height: "))
                print(ascii_art.draw_triangle(width, height, symbol))
            elif choice == 5:
                height = int(input("Enter height: "))
                print(ascii_art.draw_pyramid(height, symbol))
            else:
                print("Invalid choice! Please enter a number between 1 and 6.")
                
        except ValueError as e:
            print(f"Error: {e}")
        except TypeError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
