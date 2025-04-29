"""
ASCII Art Generator

This module provides functionality to create ASCII art shapes including squares,
rectangles, parallelograms, triangles, and pyramids.
"""

class AsciiArt:
    """
    A class for generating ASCII art shapes.
    
    This class provides methods to draw various ASCII art shapes
    using a specified symbol character.
    """
    
    @staticmethod
    def _validate_inputs(symbol: str, *dimensions: int) -> None:
        """
        Validates the input parameters for all drawing methods.
        
        Args:
            symbol: The character to use for drawing the shape.
            *dimensions: Variable length arguments representing width, height, etc.
            
        Raises:
            ValueError: If symbol is not a single character or is whitespace.
            ValueError: If any dimension is negative or zero.
        """
        # Validate symbol
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        
        # Validate dimensions
        for dimension in dimensions:
            if not isinstance(dimension, int):
                raise TypeError(f"Dimension must be an integer, got {type(dimension).__name__}.")
            if dimension <= 0:
                raise ValueError(f"Dimension must be positive, got {dimension}.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square using the specified symbol.
        
        Args:
            width: The width and height of the square.
            symbol: The character to use for drawing the square.
            
        Returns:
            A multi-line string representing the square.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, width)
        
        # Create a square by repeating the symbol 'width' times for 'width' rows
        square_rows = [symbol * width for _ in range(width)]
        return '\n'.join(square_rows)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle using the specified symbol.
        
        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.
            
        Returns:
            A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, width, height)
        
        # Create a rectangle by repeating the symbol 'width' times for 'height' rows
        rectangle_rows = [symbol * width for _ in range(height)]
        return '\n'.join(rectangle_rows)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram using the specified symbol.
        
        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to use for drawing the parallelogram.
            
        Returns:
            A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, width, height)
        
        # Each row starts with increasing spaces and contains 'width' symbols
        parallelogram_rows = [' ' * i + symbol * width for i in range(height)]
        return '\n'.join(parallelogram_rows)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle using the specified symbol.
        
        Args:
            width: The maximum width of the triangle.
            height: The height of the triangle.
            symbol: The character to use for drawing the triangle.
            
        Returns:
            A multi-line string representing the triangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, width, height)
        
        # Calculate the width increment per row
        if height <= 1:
            return symbol * width
            
        width_increment = width / height
        
        # Create the triangle rows
        triangle_rows = []
        for i in range(height):
            # Calculate how many symbols to draw in this row
            # Use integer division to avoid partial symbols
            symbols_in_row = int((i + 1) * width_increment + 0.5)
            # Ensure we don't exceed the maximum width
            symbols_in_row = min(symbols_in_row, width)
            triangle_rows.append(symbol * symbols_in_row)
        
        return '\n'.join(triangle_rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid using the specified symbol.
        
        Args:
            height: The height of the pyramid.
            symbol: The character to use for drawing the pyramid.
            
        Returns:
            A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(symbol, height)
        
        # The width of the pyramid at the base is 2*height - 1
        width = 2 * height - 1
        
        pyramid_rows = []
        for i in range(height):
            # Calculate the number of symbols in this row
            symbols_count = 2 * i + 1
            # Calculate the padding needed for centering
            padding = (width - symbols_count) // 2
            # Build the row
            row = ' ' * padding + symbol * symbols_count
            pyramid_rows.append(row)
        
        return '\n'.join(pyramid_rows)


def main():
    """
    Main function to demonstrate the AsciiArt class functionality.
    """
    ascii_art = AsciiArt()
    
    print("ASCII Art Generator")
    print("------------------")
    
    while True:
        print("\nAvailable shapes:")
        print("1. Square")
        print("2. Rectangle")
        print("3. Parallelogram")
        print("4. Triangle (right-angled)")
        print("5. Pyramid")
        print("0. Exit")
        
        try:
            choice = int(input("\nEnter your choice (0-5): "))
            
            if choice == 0:
                print("Exiting the program. Goodbye!")
                break
                
            if choice not in range(1, 6):
                print("Invalid choice. Please try again.")
                continue
                
            symbol = input("Enter a single character to draw with: ")
            
            if choice == 1:
                width = int(input("Enter width: "))
                result = ascii_art.draw_square(width, symbol)
            elif choice == 2:
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = ascii_art.draw_rectangle(width, height, symbol)
            elif choice == 3:
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = ascii_art.draw_parallelogram(width, height, symbol)
            elif choice == 4:
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                result = ascii_art.draw_triangle(width, height, symbol)
            elif choice == 5:
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
