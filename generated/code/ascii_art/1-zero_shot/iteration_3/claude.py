class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to draw various shapes using ASCII characters,
    including squares, rectangles, parallelograms, triangles, and pyramids.
    """
    
    @staticmethod
    def _validate_input(symbol: str, *dimensions: int) -> None:
        """
        Validates the input parameters for all drawing functions.
        
        Args:
            symbol: The character to use for drawing
            *dimensions: One or more dimensions (width, height) for the shape
            
        Raises:
            ValueError: If the symbol is not a single character or is whitespace
            ValueError: If any dimension is negative or zero
        """
        # Validate symbol
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
            
        # Validate dimensions
        for dimension in dimensions:
            if dimension <= 0:
                raise ValueError("Dimensions must be positive integers")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width: The width and height of the square
            symbol: The character to fill the square with
            
        Returns:
            A string representation of the square
            
        Raises:
            ValueError: If inputs are invalid
        """
        self._validate_input(symbol, width)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        
        # Repeat the row for each line of the square
        return '\n'.join([row] * width)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width: The width of the rectangle
            height: The height of the rectangle
            symbol: The character to fill the rectangle with
            
        Returns:
            A string representation of the rectangle
            
        Raises:
            ValueError: If inputs are invalid
        """
        self._validate_input(symbol, width, height)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        
        # Repeat the row for each line of the rectangle
        return '\n'.join([row] * height)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, with each row
        shifted by one space to create the slant effect.
        
        Args:
            width: The width of the parallelogram
            height: The height of the parallelogram
            symbol: The character to fill the parallelogram with
            
        Returns:
            A string representation of the parallelogram
            
        Raises:
            ValueError: If inputs are invalid
        """
        self._validate_input(symbol, width, height)
        
        result = []
        for i in range(height):
            # Add i spaces as indentation, then add a row of symbols
            result.append(' ' * i + symbol * width)
            
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        
        The triangle grows from left to right, starting with one symbol
        in the top-left corner and expanding as it goes down.
        
        Args:
            width: The maximum width of the triangle
            height: The height of the triangle
            symbol: The character to fill the triangle with
            
        Returns:
            A string representation of the right-angled triangle
            
        Raises:
            ValueError: If inputs are invalid
        """
        self._validate_input(symbol, width, height)
        
        # Calculate the number of symbols per row
        symbols_per_row = []
        for i in range(height):
            # Use linear interpolation to determine symbols in each row
            symbols = max(1, round(width * (i + 1) / height))
            symbols_per_row.append(symbols)
        
        # Build the triangle
        result = []
        for num_symbols in symbols_per_row:
            result.append(symbol * num_symbols)
            
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered, with one symbol at the top and
        increasing width as it goes down.
        
        Args:
            height: The height of the pyramid
            symbol: The character to fill the pyramid with
            
        Returns:
            A string representation of the pyramid
            
        Raises:
            ValueError: If inputs are invalid
        """
        self._validate_input(symbol, height)
        
        result = []
        for i in range(height):
            # Calculate number of symbols for this row (odd numbers: 1, 3, 5, ...)
            num_symbols = 2 * i + 1
            
            # Calculate padding to center the row
            padding = height - i - 1
            
            # Create the row with proper padding and symbols
            row = ' ' * padding + symbol * num_symbols
            result.append(row)
            
        return '\n'.join(result)


def main():
    """
    Main function to demonstrate the ASCII art generator.
    """
    ascii_art = AsciiArt()
    
    print("ASCII Art Generator")
    print("===================")
    
    while True:
        print("\nSelect a shape to draw:")
        print("1. Square")
        print("2. Rectangle")
        print("3. Parallelogram")
        print("4. Triangle")
        print("5. Pyramid")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-5): ")
        
        if choice == '0':
            print("Goodbye!")
            break
            
        # Get the symbol to use
        symbol = input("Enter the symbol to use (single character): ")
        
        try:
            if choice == '1':
                width = int(input("Enter width: "))
                result = ascii_art.draw_square(width, symbol)
                print("\nResult:\n")
                print(result)
                
            elif choice == '2':
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = ascii_art.draw_rectangle(width, height, symbol)
                print("\nResult:\n")
                print(result)
                
            elif choice == '3':
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = ascii_art.draw_parallelogram(width, height, symbol)
                print("\nResult:\n")
                print(result)
                
            elif choice == '4':
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = ascii_art.draw_triangle(width, height, symbol)
                print("\nResult:\n")
                print(result)
                
            elif choice == '5':
                height = int(input("Enter height: "))
                result = ascii_art.draw_pyramid(height, symbol)
                print("\nResult:\n")
                print(result)
                
            else:
                print("Invalid choice. Please try again.")
                
        except ValueError as e:
            print(f"Error: {e}")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
