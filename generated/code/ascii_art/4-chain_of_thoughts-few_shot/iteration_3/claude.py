class AsciiArt:
    """
    A class for creating ASCII art shapes.
    
    This class provides methods to draw various ASCII shapes using a specified
    symbol. All shapes are returned as multi-line strings.
    """
    
    @staticmethod
    def _validate_input(symbol: str, *dimensions) -> None:
        """
        Validates input parameters for drawing functions.
        
        Args:
            symbol (str): The character to use for drawing.
            *dimensions: Variable number of dimension arguments (width, height, etc.)
            
        Raises:
            ValueError: If symbol is not exactly one character or is whitespace.
            ValueError: If any dimension is negative.
        """
        # Validate the symbol
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
            
        # Validate dimensions
        for dimension in dimensions:
            if not isinstance(dimension, int):
                raise TypeError(f"Dimensions must be integers, got {type(dimension).__name__}.")
            if dimension <= 0:
                raise ValueError(f"Dimensions must be positive, got {dimension}.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The character to use for drawing the square.
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(symbol, width)
        
        # Create a row of symbols
        row = symbol * width
        
        # Join width number of rows to create the square
        return '\n'.join([row] * width)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing the rectangle.
            
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(symbol, width, height)
        
        # Create a row of symbols
        row = symbol * width
        
        # Join height number of rows to create the rectangle
        return '\n'.join([row] * height)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        The parallelogram grows diagonally to the right, with each row 
        shifted by one space.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing the parallelogram.
            
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(symbol, width, height)
        
        result = []
        for i in range(height):
            # Add i spaces before the symbols to create the shift
            result.append(' ' * i + symbol * width)
        
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The base width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The character to use for drawing the triangle.
            
        Returns:
            str: A multi-line string representing the triangle.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(symbol, width, height)
        
        result = []
        # Calculate the increment for each row
        if height <= 1:
            return symbol * width
            
        increment = width / height
        
        for i in range(height):
            # Calculate how many symbols to use for the current row
            # Use ceiling to ensure we don't get 0 symbols for the first row
            symbols_count = int(increment * (i + 1))
            result.append(symbol * symbols_count)
        
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing the pyramid.
            
        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If input validation fails.
        """
        self._validate_input(symbol, height)
        
        result = []
        width = 2 * height - 1  # Maximum width of the pyramid
        
        for i in range(height):
            # Number of symbols in the current row
            symbols_count = 2 * i + 1
            
            # Calculate padding to center the symbols
            padding = (width - symbols_count) // 2
            
            # Add the row with proper padding and symbols
            result.append(' ' * padding + symbol * symbols_count)
        
        return '\n'.join(result)


def main():
    """
    Main function to demonstrate the ASCII art functionality.
    """
    ascii_art = AsciiArt()
    
    try:
        print("\nASCII Art Generator\n" + "=" * 20)
        
        # Demonstrate each shape
        print("\nSquare (4x4, '#'):")
        print(ascii_art.draw_square(4, '#'))
        
        print("\nRectangle (6x3, '*'):")
        print(ascii_art.draw_rectangle(6, 3, '*'))
        
        print("\nParallelogram (5x3, '@'):")
        print(ascii_art.draw_parallelogram(5, 3, '@'))
        
        print("\nTriangle (5x3, '+'):")
        print(ascii_art.draw_triangle(5, 3, '+'))
        
        print("\nPyramid (4, '^'):")
        print(ascii_art.draw_pyramid(4, '^'))
        
        # Interactive mode
        print("\n" + "=" * 20)
        print("Interactive Mode:")
        while True:
            print("\nChoose a shape to draw:")
            print("1. Square")
            print("2. Rectangle")
            print("3. Parallelogram")
            print("4. Triangle")
            print("5. Pyramid")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '6':
                print("Exiting...")
                break
            
            symbol = input("Enter a single character to use: ")
            
            try:
                if choice == '1':
                    width = int(input("Enter width: "))
                    print(ascii_art.draw_square(width, symbol))
                elif choice == '2':
                    width = int(input("Enter width: "))
                    height = int(input("Enter height: "))
                    print(ascii_art.draw_rectangle(width, height, symbol))
                elif choice == '3':
                    width = int(input("Enter width: "))
                    height = int(input("Enter height: "))
                    print(ascii_art.draw_parallelogram(width, height, symbol))
                elif choice == '4':
                    width = int(input("Enter width: "))
                    height = int(input("Enter height: "))
                    print(ascii_art.draw_triangle(width, height, symbol))
                elif choice == '5':
                    height = int(input("Enter height: "))
                    print(ascii_art.draw_pyramid(height, symbol))
                else:
                    print("Invalid choice, please try again.")
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
    
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
