class AsciiArt:
    """A class for generating ASCII art shapes.
    
    This class provides methods to create various ASCII art shapes
    such as squares, rectangles, parallelograms, triangles, and pyramids.
    Each shape is filled with a user-specified symbol.
    """
    
    @staticmethod
    def _validate_input(width: int, height: int, symbol: str) -> None:
        """Validate input parameters for all drawing functions.
        
        Args:
            width: The width of the shape.
            height: The height of the shape.
            symbol: The character to fill the shape with.
            
        Raises:
            ValueError: If width or height is not positive, or if symbol is not a single character.
            TypeError: If width, height are not integers or if symbol is not a string.
        """
        # Type validation
        if not isinstance(width, int):
            raise TypeError("Width must be an integer.")
        if not isinstance(height, int):
            raise TypeError("Height must be an integer.")
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
            
        # Value validation
        if width <= 0:
            raise ValueError("Width must be a positive integer.")
        if height <= 0:
            raise ValueError("Height must be a positive integer.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """Draw a square filled with the specified symbol.
        
        Args:
            width: The width and height of the square.
            symbol: The character to fill the square with.
            
        Returns:
            A string representation of the square.
            
        Raises:
            ValueError: If width is not positive, or if symbol is not a single character.
            TypeError: If width is not an integer or if symbol is not a string.
        """
        self._validate_input(width, width, symbol)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        
        # Repeat the row for the height (same as width for a square)
        return '\n'.join([row] * width)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Draw a rectangle filled with the specified symbol.
        
        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to fill the rectangle with.
            
        Returns:
            A string representation of the rectangle.
            
        Raises:
            ValueError: If width or height is not positive, or if symbol is not a single character.
            TypeError: If width, height are not integers or if symbol is not a string.
        """
        self._validate_input(width, height, symbol)
        
        # Create a row of symbols with the specified width
        row = symbol * width
        
        # Repeat the row for the specified height
        return '\n'.join([row] * height)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """Draw a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, with each row
        shifted one space to the right from the previous row.
        
        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to fill the parallelogram with.
            
        Returns:
            A string representation of the parallelogram.
            
        Raises:
            ValueError: If width or height is not positive, or if symbol is not a single character.
            TypeError: If width, height are not integers or if symbol is not a string.
        """
        self._validate_input(width, height, symbol)
        
        result = []
        row = symbol * width
        
        for i in range(height):
            # Add spaces at the beginning of each row (proportional to the row number)
            result.append(' ' * i + row)
        
        return '\n'.join(result)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """Draw a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        Each row has one more symbol than the previous row.
        
        Args:
            width: The maximum width of the triangle (may not be fully used if height is smaller).
            height: The height of the triangle.
            symbol: The character to fill the triangle with.
            
        Returns:
            A string representation of the triangle.
            
        Raises:
            ValueError: If width or height is not positive, or if symbol is not a single character.
            TypeError: If width, height are not integers or if symbol is not a string.
        """
        self._validate_input(width, height, symbol)
        
        result = []
        # Calculate the actual width for each row (limited by either width or current row)
        for i in range(1, height + 1):
            actual_width = min(i, width)
            result.append(symbol * actual_width)
        
        return '\n'.join(result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """Draw a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered, with the width increasing by 2 for each row.
        
        Args:
            height: The height of the pyramid.
            symbol: The character to fill the pyramid with.
            
        Returns:
            A string representation of the pyramid.
            
        Raises:
            ValueError: If height is not positive, or if symbol is not a single character.
            TypeError: If height is not an integer or if symbol is not a string.
        """
        # Using a dummy width value for validation since width is determined by height
        self._validate_input(1, height, symbol)
        
        result = []
        max_width = 2 * height - 1  # Maximum width at the base of the pyramid
        
        for i in range(height):
            # Calculate number of symbols for current row
            symbols_count = 2 * i + 1
            # Calculate padding needed to center the symbols
            padding = (max_width - symbols_count) // 2
            
            # Construct the row with padding and symbols
            row = ' ' * padding + symbol * symbols_count
            result.append(row)
        
        return '\n'.join(result)


def main():
    """Main function to demonstrate the AsciiArt class functionality."""
    ascii_art = AsciiArt()
    
    print("ASCII Art Generator")
    print("===================")
    
    try:
        while True:
            print("\nChoose a shape to draw:")
            print("1. Square")
            print("2. Rectangle")
            print("3. Parallelogram")
            print("4. Triangle (Right-angled)")
            print("5. Pyramid")
            print("0. Exit")
            
            choice = input("\nEnter your choice (0-5): ")
            
            if choice == '0':
                print("Exiting program. Goodbye!")
                break
            
            # Get the symbol from user
            symbol = input("Enter a single character to draw with: ")
            
            if choice == '1':  # Square
                width = int(input("Enter width: "))
                print("\nYour square:")
                print(ascii_art.draw_square(width, symbol))
                
            elif choice == '2':  # Rectangle
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                print("\nYour rectangle:")
                print(ascii_art.draw_rectangle(width, height, symbol))
                
            elif choice == '3':  # Parallelogram
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                print("\nYour parallelogram:")
                print(ascii_art.draw_parallelogram(width, height, symbol))
                
            elif choice == '4':  # Triangle
                width = int(input("Enter max width: "))
                height = int(input("Enter height: "))
                print("\nYour triangle:")
                print(ascii_art.draw_triangle(width, height, symbol))
                
            elif choice == '5':  # Pyramid
                height = int(input("Enter height: "))
                print("\nYour pyramid:")
                print(ascii_art.draw_pyramid(height, symbol))
                
            else:
                print("Invalid choice. Please try again.")
                
    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
