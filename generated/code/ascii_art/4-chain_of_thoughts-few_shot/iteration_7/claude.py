class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods for drawing various ASCII shapes including
    squares, rectangles, parallelograms, triangles, and pyramids with a specified symbol.
    """
    
    @staticmethod
    def _validate_inputs(symbol: str, *dimensions: int) -> None:
        """
        Validates input parameters for the drawing functions.
        
        Args:
            symbol (str): The character to use for drawing the shape.
            *dimensions (int): Width, height or other dimensions of the shape.
            
        Raises:
            ValueError: If symbol is not exactly one character or is whitespace.
            ValueError: If any dimension is negative or zero.
        """
        # Validate symbol
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        
        # Validate dimensions
        for dimension in dimensions:
            if dimension <= 0:
                raise ValueError("Dimensions must be positive integers.")

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square with the specified width using the given symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The character to use for drawing the square.
            
        Returns:
            str: A multi-line string representing the ASCII square.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, width)
        
        # Create the square by repeating the symbol
        row = symbol * width
        square = '\n'.join([row for _ in range(width)])
        
        return square

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle with the specified width and height using the given symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use for drawing the rectangle.
            
        Returns:
            str: A multi-line string representing the ASCII rectangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, width, height)
        
        # Create the rectangle by repeating the symbol
        row = symbol * width
        rectangle = '\n'.join([row for _ in range(height)])
        
        return rectangle

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified width and height using the given symbol.
        The parallelogram grows diagonally to the right, with each row shifted by one space.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use for drawing the parallelogram.
            
        Returns:
            str: A multi-line string representing the ASCII parallelogram.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, width, height)
        
        # Create the parallelogram with proper spacing
        parallelogram_rows = []
        for i in range(height):
            # Add i spaces at the beginning of each row
            row = " " * i + symbol * width
            parallelogram_rows.append(row)
        
        return '\n'.join(parallelogram_rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle with the specified width and height using the given symbol.
        The triangle grows diagonally to the right from the top-left corner.
        
        Args:
            width (int): The maximum width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The character to use for drawing the triangle.
            
        Returns:
            str: A multi-line string representing the ASCII right-angled triangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, width, height)
        
        triangle_rows = []
        # Calculate width increment per row
        if height <= 1:
            width_per_row = width
        else:
            width_per_row = width / (height - 1)
        
        for i in range(height):
            # Calculate the width for the current row, ensuring it's an integer
            current_width = min(width, int(i * width_per_row) + 1)
            row = symbol * current_width
            triangle_rows.append(row)
        
        return '\n'.join(triangle_rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the specified height using the given symbol.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use for drawing the pyramid.
            
        Returns:
            str: A multi-line string representing the ASCII pyramid.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, height)
        
        pyramid_rows = []
        for i in range(height):
            # Calculate spaces and symbols for current row
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            row = spaces + symbols
            pyramid_rows.append(row)
        
        return '\n'.join(pyramid_rows)


def main():
    """
    Main function to demonstrate the AsciiArt class functionality.
    Allows the user to choose shapes and parameters via a simple console interface.
    """
    ascii_art = AsciiArt()
    
    print("Welcome to ASCII Art Generator!")
    print("==============================")
    
    while True:
        print("\nChoose a shape to draw:")
        print("1. Square")
        print("2. Rectangle")
        print("3. Parallelogram")
        print("4. Triangle (Right-angled)")
        print("5. Pyramid")
        print("0. Exit")
        
        try:
            choice = int(input("Enter your choice (0-5): "))
            
            if choice == 0:
                print("Thank you for using ASCII Art Generator. Goodbye!")
                break
                
            # Get the symbol from user
            symbol = input("Enter a single character to use for drawing: ")
            
            if choice == 1:
                width = int(input("Enter the width of the square: "))
                result = ascii_art.draw_square(width, symbol)
                
            elif choice == 2:
                width = int(input("Enter the width of the rectangle: "))
                height = int(input("Enter the height of the rectangle: "))
                result = ascii_art.draw_rectangle(width, height, symbol)
                
            elif choice == 3:
                width = int(input("Enter the width of the parallelogram: "))
                height = int(input("Enter the height of the parallelogram: "))
                result = ascii_art.draw_parallelogram(width, height, symbol)
                
            elif choice == 4:
                width = int(input("Enter the width of the triangle: "))
                height = int(input("Enter the height of the triangle: "))
                result = ascii_art.draw_triangle(width, height, symbol)
                
            elif choice == 5:
                height = int(input("Enter the height of the pyramid: "))
                result = ascii_art.draw_pyramid(height, symbol)
                
            else:
                print("Invalid choice. Please try again.")
                continue
                
            print("\nYour ASCII Art:")
            print(result)
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
