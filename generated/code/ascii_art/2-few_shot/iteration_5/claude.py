class AsciiArt:
    """
    A class for generating 2D ASCII art shapes.
    
    This class provides functionality to draw various ASCII art shapes
    like squares, rectangles, parallelograms, triangles, and pyramids
    using a specified symbol.
    """
    
    @staticmethod
    def _validate_input(width: int, height: int, symbol: str) -> None:
        """
        Validates the input parameters for ASCII art generation.
        
        Args:
            width (int): The width of the shape.
            height (int): The height of the shape.
            symbol (str): The symbol to use for drawing.
            
        Raises:
            ValueError: If width or height is negative.
            ValueError: If symbol is not exactly one character.
            ValueError: If symbol is a whitespace character.
        """
        if width < 1:
            raise ValueError("Width must be a positive integer")
        
        if height < 1:
            raise ValueError("Height must be a positive integer")
            
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
            
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square ASCII art shape.
        
        Args:
            width (int): The width (and height) of the square.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If inputs are invalid (see _validate_input).
        """
        self._validate_input(width, width, symbol)
        
        row = symbol * width
        result = [row for _ in range(width)]
        return '\n'.join(result)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle ASCII art shape.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If inputs are invalid (see _validate_input).
        """
        self._validate_input(width, height, symbol)
        
        row = symbol * width
        result = [row for _ in range(height)]
        return '\n'.join(result)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram ASCII art shape.
        
        The parallelogram grows diagonally to the right, with each row 
        shifted by one space to the right from the row above it.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If inputs are invalid (see _validate_input).
        """
        self._validate_input(width, height, symbol)
        
        result = []
        for i in range(height):
            spaces = ' ' * i
            row = spaces + symbol * width
            result.append(row)
        
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle ASCII art shape.
        
        The triangle grows diagonally to the right, starting from 
        the top-left corner.
        
        Args:
            width (int): The base width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the triangle.
            
        Raises:
            ValueError: If inputs are invalid (see _validate_input).
            ValueError: If width is less than height (cannot form a right triangle).
        """
        self._validate_input(width, height, symbol)
        
        if width < height:
            raise ValueError("Width must be greater than or equal to height for a right triangle")
        
        result = []
        for i in range(height):
            # Calculate how many symbols to draw in this row
            # This ensures the triangle fills out to the specified width by the last row
            symbols_in_row = max(1, round((i + 1) * width / height))
            row = symbol * symbols_in_row
            result.append(row)
        
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid ASCII art shape.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to use for drawing.
            
        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If inputs are invalid (see _validate_input).
        """
        self._validate_input(height, height, symbol)
        
        result = []
        width = 2 * height - 1  # Width of the base of the pyramid
        
        for i in range(height):
            # Number of symbols in current row
            symbols_count = 2 * i + 1
            # Number of spaces on each side
            padding = (width - symbols_count) // 2
            
            row = ' ' * padding + symbol * symbols_count
            result.append(row)
        
        return '\n'.join(result)


def main():
    """
    Main function to demonstrate the AsciiArt class functionality.
    """
    ascii_art = AsciiArt()
    
    print("ASCII Art Generator\n")
    print("Available shapes:")
    print("1. Square")
    print("2. Rectangle")
    print("3. Parallelogram")
    print("4. Right-angled Triangle")
    print("5. Pyramid")
    print("6. Exit\n")
    
    while True:
        try:
            choice = int(input("Enter your choice (1-6): "))
            
            if choice == 6:
                print("Thank you for using ASCII Art Generator!")
                break
                
            symbol = input("Enter a symbol (single character): ")
            
            if choice == 1:
                width = int(input("Enter width: "))
                print("\nResult:")
                print(ascii_art.draw_square(width, symbol))
                
            elif choice == 2:
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                print("\nResult:")
                print(ascii_art.draw_rectangle(width, height, symbol))
                
            elif choice == 3:
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                print("\nResult:")
                print(ascii_art.draw_parallelogram(width, height, symbol))
                
            elif choice == 4:
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                print("\nResult:")
                print(ascii_art.draw_triangle(width, height, symbol))
                
            elif choice == 5:
                height = int(input("Enter height: "))
                print("\nResult:")
                print(ascii_art.draw_pyramid(height, symbol))
                
            else:
                print("Invalid choice! Please enter a number between 1 and 6.")
                
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        print()  # Add blank line for readability


if __name__ == "__main__":
    main()
