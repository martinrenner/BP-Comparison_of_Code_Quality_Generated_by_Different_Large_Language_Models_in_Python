class AsciiArt:
    """
    A class for creating various ASCII art shapes.
    
    This class provides methods to generate different ASCII art shapes
    such as squares, rectangles, parallelograms, triangles, and pyramids.
    All methods validate input parameters and return properly formatted strings.
    """
    
    @staticmethod
    def _validate_input(width, height, symbol):
        """
        Validates input parameters for all shape-drawing methods.
        
        Args:
            width (int): Width of the shape.
            height (int): Height of the shape.
            symbol (str): Symbol to use for drawing the shape.
            
        Raises:
            ValueError: If width or height is negative or zero.
            TypeError: If width or height is not an integer.
            ValueError: If symbol is empty, whitespace, or more than one character.
        """
        # Validate width and height
        if not isinstance(width, int):
            raise TypeError("Width must be an integer")
        if not isinstance(height, int):
            raise TypeError("Height must be an integer")
        if width <= 0:
            raise ValueError("Width must be a positive integer")
        if height <= 0:
            raise ValueError("Height must be a positive integer")
        
        # Validate symbol
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string")
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character")
    
    def draw_square(self, width, symbol):
        """
        Draws a square using the specified symbol.
        
        Args:
            width (int): Width and height of the square.
            symbol (str): Symbol to use for drawing the square.
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError, TypeError: If inputs are invalid.
        """
        self._validate_input(width, width, symbol)
        
        # Create the square as a list of rows
        square = [symbol * width for _ in range(width)]
        
        # Join the rows with newlines
        return '\n'.join(square)
    
    def draw_rectangle(self, width, height, symbol):
        """
        Draws a rectangle using the specified symbol.
        
        Args:
            width (int): Width of the rectangle.
            height (int): Height of the rectangle.
            symbol (str): Symbol to use for drawing the rectangle.
            
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError, TypeError: If inputs are invalid.
        """
        self._validate_input(width, height, symbol)
        
        # Create the rectangle as a list of rows
        rectangle = [symbol * width for _ in range(height)]
        
        # Join the rows with newlines
        return '\n'.join(rectangle)
    
    def draw_parallelogram(self, width, height, symbol):
        """
        Draws a parallelogram using the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        Each row is shifted by one space to the right compared to the previous row.
        
        Args:
            width (int): Width of the parallelogram.
            height (int): Height of the parallelogram.
            symbol (str): Symbol to use for drawing the parallelogram.
            
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError, TypeError: If inputs are invalid.
        """
        self._validate_input(width, height, symbol)
        
        # Create the parallelogram as a list of rows
        parallelogram = [' ' * i + symbol * width for i in range(height)]
        
        # Join the rows with newlines
        return '\n'.join(parallelogram)
    
    def draw_triangle(self, width, height, symbol):
        """
        Draws a right-angled triangle using the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): Maximum width of the triangle.
            height (int): Height of the triangle.
            symbol (str): Symbol to use for drawing the triangle.
            
        Returns:
            str: A multi-line string representing the triangle.
            
        Raises:
            ValueError, TypeError: If inputs are invalid.
        """
        self._validate_input(width, height, symbol)
        
        # Calculate the increment per row
        if height == 1:
            increment = width
        else:
            increment = max(1, width // height)
        
        # Create the triangle as a list of rows
        triangle = []
        for i in range(height):
            # Calculate the number of symbols for this row, ensuring we don't exceed width
            num_symbols = min(width, (i + 1) * increment)
            triangle.append(symbol * num_symbols)
        
        # Join the rows with newlines
        return '\n'.join(triangle)
    
    def draw_pyramid(self, height, symbol):
        """
        Draws a symmetrical pyramid using the specified symbol.
        
        The pyramid is centered and grows from top to bottom.
        
        Args:
            height (int): Height of the pyramid.
            symbol (str): Symbol to use for drawing the pyramid.
            
        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError, TypeError: If inputs are invalid.
        """
        # For the pyramid, width = 2 * height - 1
        width = 2 * height - 1
        self._validate_input(width, height, symbol)
        
        pyramid = []
        for i in range(height):
            # Calculate the number of symbols for this row (2*i + 1)
            num_symbols = 2 * i + 1
            # Calculate the padding needed to center the symbols
            padding = (width - num_symbols) // 2
            # Add the row to our pyramid
            pyramid.append(' ' * padding + symbol * num_symbols)
        
        # Join the rows with newlines
        return '\n'.join(pyramid)


def main():
    """
    Main function to demonstrate the AsciiArt class.
    """
    ascii_art = AsciiArt()
    
    print("ASCII Art Generator")
    print("===================")
    
    while True:
        print("\nChoose a shape to draw:")
        print("1. Square")
        print("2. Rectangle")
        print("3. Parallelogram")
        print("4. Triangle (right-angled)")
        print("5. Pyramid")
        print("0. Exit")
        
        try:
            choice = int(input("Enter your choice (0-5): "))
            
            if choice == 0:
                print("Exiting. Goodbye!")
                break
            
            symbol = input("Enter a symbol to use (single character): ")
            
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
                print("Invalid choice. Please try again.")
        
        except ValueError as e:
            print(f"Error: {e}")
        except TypeError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
