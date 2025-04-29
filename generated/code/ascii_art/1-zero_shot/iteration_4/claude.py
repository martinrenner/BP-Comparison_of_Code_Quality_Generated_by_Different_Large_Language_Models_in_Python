class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to create various geometric shapes using ASCII characters.
    All methods validate inputs and return a formatted multi-line string.
    """
    
    @staticmethod
    def _validate_input(width: int, height: int, symbol: str) -> None:
        """
        Validates the input parameters for all drawing methods.
        
        Args:
            width: Width of the shape (must be positive)
            height: Height of the shape (must be positive)
            symbol: Character to use for drawing (must be exactly one non-whitespace character)
            
        Raises:
            ValueError: If any of the validations fail
        """
        # Check dimensions
        if width <= 0:
            raise ValueError(f"Width must be positive, got {width}")
        if height <= 0:
            raise ValueError(f"Height must be positive, got {height}")
        
        # Check symbol
        if len(symbol) != 1:
            raise ValueError(f"Symbol must be exactly one character, got '{symbol}' (length: {len(symbol)})")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square with the specified width and symbol.
        
        Args:
            width: Width of the square (equal to height)
            symbol: Character to use for drawing
            
        Returns:
            A multi-line string representing the square
        
        Raises:
            ValueError: If inputs are invalid
        """
        self._validate_input(width, width, symbol)
        
        # For a square, width = height
        lines = []
        for _ in range(width):
            lines.append(symbol * width)
        
        return "\n".join(lines)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle with the specified width, height and symbol.
        
        Args:
            width: Width of the rectangle
            height: Height of the rectangle
            symbol: Character to use for drawing
            
        Returns:
            A multi-line string representing the rectangle
        
        Raises:
            ValueError: If inputs are invalid
        """
        self._validate_input(width, height, symbol)
        
        lines = []
        for _ in range(height):
            lines.append(symbol * width)
        
        return "\n".join(lines)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified width, height and symbol.
        
        The parallelogram grows diagonally to the right, with each row shifted
        by one space to create the diagonal effect.
        
        Args:
            width: Width of the parallelogram
            height: Height of the parallelogram
            symbol: Character to use for drawing
            
        Returns:
            A multi-line string representing the parallelogram
        
        Raises:
            ValueError: If inputs are invalid
        """
        self._validate_input(width, height, symbol)
        
        lines = []
        for i in range(height):
            # Add i spaces before the symbols to create the parallelogram effect
            lines.append(" " * i + symbol * width)
        
        return "\n".join(lines)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with the specified width, height and symbol.
        
        The triangle grows diagonally to the right from the top-left corner.
        
        Args:
            width: Maximum width of the triangle
            height: Height of the triangle
            symbol: Character to use for drawing
            
        Returns:
            A multi-line string representing the triangle
        
        Raises:
            ValueError: If inputs are invalid
        """
        self._validate_input(width, height, symbol)
        
        lines = []
        # Calculate how many symbols to add per row to maintain proportions
        symbols_per_row = max(1, width // height)
        
        for i in range(height):
            # Ensure we don't exceed the specified width
            num_symbols = min((i + 1) * symbols_per_row, width)
            lines.append(symbol * num_symbols)
        
        return "\n".join(lines)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the specified height and symbol.
        
        Args:
            height: Height of the pyramid
            symbol: Character to use for drawing
            
        Returns:
            A multi-line string representing the pyramid
        
        Raises:
            ValueError: If inputs are invalid
        """
        # For a pyramid, width is derived from height
        width = height * 2 - 1
        self._validate_input(width, height, symbol)
        
        lines = []
        for i in range(height):
            # Calculate the number of symbols for this row
            num_symbols = 2 * i + 1
            # Calculate spaces needed before symbols for centering
            spaces = (width - num_symbols) // 2
            lines.append(" " * spaces + symbol * num_symbols)
        
        return "\n".join(lines)


def main():
    """
    Main function to demonstrate the ASCII art generator.
    """
    ascii_art = AsciiArt()
    
    print("Welcome to the ASCII Art Generator!")
    print("===================================")
    
    while True:
        print("\nSelect a shape to draw:")
        print("1. Square")
        print("2. Rectangle")
        print("3. Parallelogram")
        print("4. Right-angled Triangle")
        print("5. Pyramid")
        print("0. Exit")
        
        try:
            choice = int(input("\nEnter your choice (0-5): "))
            
            if choice == 0:
                print("Thank you for using ASCII Art Generator. Goodbye!")
                break
            
            if choice not in range(1, 6):
                print("Invalid choice! Please enter a number between 0 and 5.")
                continue
            
            symbol = input("Enter a single character to use for drawing: ")
            
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
                width = int(input("Enter max width: "))
                height = int(input("Enter height: "))
                result = ascii_art.draw_triangle(width, height, symbol)
            
            elif choice == 5:  # Pyramid
                height = int(input("Enter height: "))
                result = ascii_art.draw_pyramid(height, symbol)
            
            print("\nHere's your ASCII art:")
            print("----------------------")
            print(result)
            print("----------------------")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
