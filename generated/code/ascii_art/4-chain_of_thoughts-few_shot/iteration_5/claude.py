class AsciiArt:
    """
    A class for generating various ASCII art shapes.
    
    This class provides methods to create different geometric shapes
    using ASCII characters. Each shape is completely filled with the
    specified symbol.
    """
    
    @staticmethod
    def _validate_input(symbol: str, *dimensions: int) -> None:
        """
        Validates input parameters for all drawing methods.
        
        Args:
            symbol (str): The character to use for drawing the shape.
            *dimensions (int): One or more integers representing dimensions.
            
        Raises:
            ValueError: If the symbol is not exactly one character or is whitespace.
            ValueError: If any dimension is negative or zero.
        """
        # Validate symbol
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace")
            
        # Validate dimensions
        for dimension in dimensions:
            if dimension <= 0:
                raise ValueError("Dimensions must be positive integers")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The character to use for drawing the square.
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If inputs are invalid (see _validate_input).
        """
        self._validate_input(symbol, width)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        
        # Repeat the row for each line to create the square
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
            ValueError: If inputs are invalid (see _validate_input).
        """
        self._validate_input(symbol, width, height)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        
        # Repeat the row for each line to create the rectangle
        return '\n'.join([row] * height)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        The parallelogram grows diagonally to the right, with each row
        shifted by one space from the previous row.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing the parallelogram.
            
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If inputs are invalid (see _validate_input).
        """
        self._validate_input(symbol, width, height)
        
        result = []
        row = symbol * width
        
        for i in range(height):
            # Add increasing number of spaces before each row
            result.append(' ' * i + row)
            
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The maximum width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The character to use for drawing the triangle.
            
        Returns:
            str: A multi-line string representing the triangle.
            
        Raises:
            ValueError: If inputs are invalid (see _validate_input).
        """
        self._validate_input(symbol, width, height)
        
        result = []
        
        # Calculate step size for width increase in each row
        if height <= 1:
            step = 0  # Edge case
        else:
            step = (width - 1) / (height - 1) if height > 1 else 0
            
        for i in range(height):
            # Calculate the width for the current row
            current_width = max(1, round(1 + i * step))
            result.append(symbol * current_width)
            
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
            ValueError: If inputs are invalid (see _validate_input).
        """
        self._validate_input(symbol, height)
        
        result = []
        
        for i in range(height):
            # Calculate number of symbols and spaces for this row
            num_symbols = 2 * i + 1
            num_spaces = height - i - 1
            
            # Create the row with proper spacing and symbols
            row = ' ' * num_spaces + symbol * num_symbols
            result.append(row)
            
        return '\n'.join(result)


def main():
    """
    Main function to demonstrate the AsciiArt class functionality.
    Allows users to create different ASCII art shapes interactively.
    """
    ascii_art = AsciiArt()
    
    print("ASCII Art Generator")
    print("===================")
    
    while True:
        print("\nAvailable shapes:")
        print("1. Square")
        print("2. Rectangle")
        print("3. Parallelogram")
        print("4. Triangle (right-angled)")
        print("5. Pyramid")
        print("0. Exit")
        
        choice = input("\nSelect a shape (0-5): ")
        
        if choice == '0':
            print("Goodbye!")
            break
            
        try:
            symbol = input("Enter a symbol (one character): ")
            
            if choice == '1':
                width = int(input("Enter width: "))
                result = ascii_art.draw_square(width, symbol)
            elif choice == '2':
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = ascii_art.draw_rectangle(width, height, symbol)
            elif choice == '3':
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = ascii_art.draw_parallelogram(width, height, symbol)
            elif choice == '4':
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = ascii_art.draw_triangle(width, height, symbol)
            elif choice == '5':
                height = int(input("Enter height: "))
                result = ascii_art.draw_pyramid(height, symbol)
            else:
                print("Invalid choice. Please select a number between 0 and 5.")
                continue
                
            print("\nResult:")
            print(result)
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
