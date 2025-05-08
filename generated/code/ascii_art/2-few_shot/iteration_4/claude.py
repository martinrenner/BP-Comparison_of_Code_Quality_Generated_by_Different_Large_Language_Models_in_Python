class AsciiArt:
    """
    A class for generating various ASCII art shapes.
    
    This class provides methods to create different geometric shapes using ASCII characters.
    Each method validates the input parameters and returns a string representing the shape.
    """
    
    @staticmethod
    def _validate_input(symbol: str, *dimensions: int) -> None:
        """
        Validates the input parameters for all drawing functions.
        
        Args:
            symbol (str): The character to use for drawing the shape.
            *dimensions (int): One or more dimensions for the shape (width, height, etc.).
            
        Raises:
            ValueError: If the symbol is not exactly one character, is whitespace,
                       or if any dimension is negative or zero.
        """
        # Validate symbol
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
            
        # Validate dimensions
        for i, dimension in enumerate(dimensions):
            if dimension <= 0:
                dimension_name = ["width", "height"][i] if i < 2 else f"dimension {i+1}"
                raise ValueError(f"{dimension_name.capitalize()} must be positive")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The character to fill the square with.
            
        Returns:
            str: A multi-line string representing a square.
            
        Raises:
            ValueError: If the symbol is invalid or the width is not positive.
        """
        self._validate_input(symbol, width)
        
        # Create a square by repeating the symbol 'width' times for 'width' rows
        row = symbol * width
        return '\n'.join([row] * width)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to fill the rectangle with.
            
        Returns:
            str: A multi-line string representing a rectangle.
            
        Raises:
            ValueError: If the symbol is invalid or any dimension is not positive.
        """
        self._validate_input(symbol, width, height)
        
        # Create a rectangle by repeating the symbol 'width' times for 'height' rows
        row = symbol * width
        return '\n'.join([row] * height)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, 
        starting from the top-left corner with each row shifted by one space.
        
        Args:
            width (int): The width of the parallelogram's base.
            height (int): The height of the parallelogram.
            symbol (str): The character to fill the parallelogram with.
            
        Returns:
            str: A multi-line string representing a parallelogram.
            
        Raises:
            ValueError: If the symbol is invalid or any dimension is not positive.
        """
        self._validate_input(symbol, width, height)
        
        # Create rows with increasing indentation
        rows = []
        for i in range(height):
            rows.append(' ' * i + symbol * width)
        
        return '\n'.join(rows)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The width of the triangle's base.
            height (int): The height of the triangle.
            symbol (str): The character to fill the triangle with.
            
        Returns:
            str: A multi-line string representing a right-angled triangle.
            
        Raises:
            ValueError: If the symbol is invalid or any dimension is not positive.
        """
        self._validate_input(symbol, width, height)
        
        rows = []
        # Calculate the width increment for each row to form a right-angled triangle
        width_increment = width / height
        
        for i in range(height):
            # Calculate the width of the current row
            current_width = int((i + 1) * width_increment)
            rows.append(symbol * current_width)
        
        return '\n'.join(rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to fill the pyramid with.
            
        Returns:
            str: A multi-line string representing a symmetrical pyramid.
            
        Raises:
            ValueError: If the symbol is invalid or height is not positive.
        """
        self._validate_input(symbol, height)
        
        rows = []
        for i in range(height):
            # For each row, calculate the number of symbols and spaces
            symbols = 2 * i + 1
            spaces = height - i - 1
            
            rows.append(' ' * spaces + symbol * symbols)
        
        return '\n'.join(rows)


def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    ascii_art = AsciiArt()
    
    print("ASCII Art Generator\n")
    
    while True:
        print("\nChoose a shape to draw:")
        print("1. Square")
        print("2. Rectangle")
        print("3. Parallelogram")
        print("4. Triangle (Right-angled)")
        print("5. Pyramid")
        print("0. Exit")
        
        try:
            choice = int(input("\nEnter your choice (0-5): "))
            
            if choice == 0:
                print("Thank you for using ASCII Art Generator!")
                break
                
            if choice < 1 or choice > 5:
                print("Invalid choice! Please enter a number between 0 and 5.")
                continue
                
            symbol = input("Enter a symbol to draw with (single character): ")
                
            if choice == 1:  # Square
                width = int(input("Enter width: "))
                result = ascii_art.draw_square(width, symbol)
            elif choice == 2:  # Rectangle
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = ascii_art.draw_rectangle(width, height, symbol)
            elif choice == 3:  # Parallelogram
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = ascii_art.draw_parallelogram(width, height, symbol)
            elif choice == 4:  # Triangle
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = ascii_art.draw_triangle(width, height, symbol)
            elif choice == 5:  # Pyramid
                height = int(input("Enter height: "))
                result = ascii_art.draw_pyramid(height, symbol)
            
            print("\nYour ASCII art:")
            print(result)
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
