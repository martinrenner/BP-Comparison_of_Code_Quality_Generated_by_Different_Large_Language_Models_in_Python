class AsciiArt:
    """
    A class for drawing ASCII art shapes.
    
    This class provides methods to draw various ASCII art shapes including
    squares, rectangles, parallelograms, right-angled triangles, and pyramids.
    """
    
    @staticmethod
    def _validate_input(width: int, height: int, symbol: str) -> None:
        """
        Validates input parameters for the drawing functions.
        
        Args:
            width (int): The width of the shape.
            height (int): The height of the shape.
            symbol (str): The symbol used to draw the shape.
            
        Raises:
            ValueError: If symbol is not a single character or is whitespace.
            ValueError: If width or height is negative.
        """
        # Validate symbol
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace")
        
        # Validate dimensions
        if width < 0:
            raise ValueError("Width cannot be negative")
        if height < 0:
            raise ValueError("Height cannot be negative")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square filled with the specified symbol.
        
        Args:
            width (int): The width and height of the square.
            symbol (str): The symbol used to draw the square.
            
        Returns:
            str: A multi-line string representing the square.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(width, width, symbol)
        if width == 0:
            return ""
        
        # Create a row of symbols with the specified width
        row = symbol * width
        # Create width number of rows
        return '\n'.join([row] * width)
    
    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle filled with the specified symbol.
        
        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol used to draw the rectangle.
            
        Returns:
            str: A multi-line string representing the rectangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(width, height, symbol)
        if width == 0 or height == 0:
            return ""
        
        # Create a row of symbols with the specified width
        row = symbol * width
        # Create height number of rows
        return '\n'.join([row] * height)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram filled with the specified symbol.
        
        The parallelogram grows diagonally to the right, starting from the top-left corner.
        Each row is shifted by one space to create the diagonal effect.
        
        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol used to draw the parallelogram.
            
        Returns:
            str: A multi-line string representing the parallelogram.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(width, height, symbol)
        if width == 0 or height == 0:
            return ""
        
        # Create rows with increasing indentation
        rows = []
        for i in range(height):
            # Add spaces for indentation and then symbols for the row
            rows.append(' ' * i + symbol * width)
        
        return '\n'.join(rows)
    
    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle filled with the specified symbol.
        
        The triangle grows diagonally to the right, starting from the top-left corner.
        
        Args:
            width (int): The width of the triangle.
            height (int): The height of the triangle.
            symbol (str): The symbol used to draw the triangle.
            
        Returns:
            str: A multi-line string representing the right-angled triangle.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(width, height, symbol)
        if width == 0 or height == 0:
            return ""
        
        # Calculate symbols per row
        rows = []
        for i in range(height):
            # Calculate number of symbols in current row
            symbols_in_row = max(1, int((i + 1) * width / height))
            rows.append(symbol * symbols_in_row)
        
        return '\n'.join(rows)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid filled with the specified symbol.
        
        The pyramid is centered and grows from top to bottom.
        
        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol used to draw the pyramid.
            
        Returns:
            str: A multi-line string representing the pyramid.
            
        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_input(height, height, symbol)
        if height == 0:
            return ""
        
        rows = []
        for i in range(height):
            # Calculate spaces and symbols for current row
            spaces = height - i - 1
            symbols_count = 2 * i + 1
            
            # Create the row with proper spacing and symbols
            row = ' ' * spaces + symbol * symbols_count
            rows.append(row)
        
        return '\n'.join(rows)


def main():
    """
    Main function to demonstrate the AsciiArt class functionality.
    """
    ascii_art = AsciiArt()
    
    print("\nASCII ART GENERATOR\n")
    
    try:
        while True:
            print("\nChoose a shape to draw:")
            print("1. Square")
            print("2. Rectangle")
            print("3. Parallelogram")
            print("4. Right-angled Triangle")
            print("5. Pyramid")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '6':
                print("Exiting the program. Goodbye!")
                break
            
            symbol = input("Enter a single character to use for drawing: ")
            
            try:
                if choice == '1':
                    width = int(input("Enter the width of the square: "))
                    print("\nHere's your square:")
                    print(ascii_art.draw_square(width, symbol))
                    
                elif choice == '2':
                    width = int(input("Enter the width of the rectangle: "))
                    height = int(input("Enter the height of the rectangle: "))
                    print("\nHere's your rectangle:")
                    print(ascii_art.draw_rectangle(width, height, symbol))
                    
                elif choice == '3':
                    width = int(input("Enter the width of the parallelogram: "))
                    height = int(input("Enter the height of the parallelogram: "))
                    print("\nHere's your parallelogram:")
                    print(ascii_art.draw_parallelogram(width, height, symbol))
                    
                elif choice == '4':
                    width = int(input("Enter the width of the triangle: "))
                    height = int(input("Enter the height of the triangle: "))
                    print("\nHere's your triangle:")
                    print(ascii_art.draw_triangle(width, height, symbol))
                    
                elif choice == '5':
                    height = int(input("Enter the height of the pyramid: "))
                    print("\nHere's your pyramid:")
                    print(ascii_art.draw_pyramid(height, symbol))
                    
                else:
                    print("Invalid choice. Please enter a number between 1 and 6.")
                    
            except ValueError as e:
                print(f"Error: {e}")
                
    except KeyboardInterrupt:
        print("\nProgram terminated by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
