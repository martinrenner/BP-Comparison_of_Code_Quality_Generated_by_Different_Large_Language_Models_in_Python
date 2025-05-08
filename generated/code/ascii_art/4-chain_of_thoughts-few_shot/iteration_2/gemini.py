class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def _validate_input(self, symbol: str, width: int = 0, height: int = 0):
        """
        Validates the input parameters for drawing functions.
        
        Args:
            symbol (str): The symbol to use for drawing.
            width (int, optional): width.
            height (int, optional): height.

        Raises:
            TypeError: If types are invalid.
            ValueError: If values are invalid.
        """

        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("Width and height must be integers.")
        if width < 0 or height < 0:
            raise ValueError("Width and height cannot be negative.")


    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width using the given symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The character to use for drawing.

        Returns:
            str: A multi-line string representing the square.
        """
        self._validate_input(symbol, width=width, height=0)  # height will be ignored

        if width == 0:
            return ""

        result = ""
        for _ in range(width):
            result += symbol * width + "\n"
        return result


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The character to use.

        Returns:
            str: A multi-line string representing the rectangle.
        """
        self._validate_input(symbol, width, height)

        if width == 0 or height == 0:
            return ""

        result = ""
        for _ in range(height):
            result += symbol * width + "\n"
        return result


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The character to use.

        Returns:
            str: A multi-line string representing the parallelogram.
        """
        self._validate_input(symbol, width, height)

        if width == 0 or height == 0:
            return ""

        result = ""
        for i in range(height):
            result += " " * i + symbol * width + "\n"
        return result


    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
          width (int): The width of the base of the triangle.
          height (int): The height of the triangle
          symbol (str): The character to use.

        Returns:
            str: A multi-line string representing the triangle.
        """
        self._validate_input(symbol, width, height)  # Validate width and height

        if width == 0 or height == 0:
            return ""

        result = ""
        # Determine the number of rows based on the smaller of width and height
        num_rows = min(width, height)
        for i in range(num_rows):
            result += symbol * (i + 1) + "\n"
        return result
        

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The character to use.

        Returns:
            str: A multi-line string representing the pyramid.
        """
        self._validate_input(symbol, height=height, width=0)  # Only height is relevant
        
        if height == 0:
          return ""

        result = ""
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            result += spaces + symbols + "\n"
        return result

# --- Example Usage and Testing ---
if __name__ == '__main__':
    art = AsciiArt()

    # Square
    print("Square:")
    print(art.draw_square(5, "*"))

    # Rectangle
    print("Rectangle:")
    print(art.draw_rectangle(7, 3, "#"))

    # Parallelogram
    print("Parallelogram:")
    print(art.draw_parallelogram(6, 4, "@"))

    # Triangle
    print("Triangle:")
    print(art.draw_triangle(5, 7, "+"))

    print("Triangle (width > height):")
    print(art.draw_triangle(7, 4, "+"))
    
    # Pyramid
    print("Pyramid:")
    print(art.draw_pyramid(5, "$"))

    # Test error handling
    try:
        print(art.draw_square(-5, "*"))  # Negative width
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print(art.draw_square(5, "  "))  # Whitespace symbol
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        print(art.draw_square(5, "**"))  # Multi-character symbol
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    try:
        print(art.draw_square(5, 1))  # Invalid symbol type
    except TypeError as e:
        print(f"Caught expected error: {e}")
    
    try:
        print(art.draw_rectangle("5", 5, "*")) # Invalid with type
    except TypeError as e:
        print(f"Caught expected error: {e}")
    
    #Zero width/height
    print("Square Zero:")
    print(art.draw_square(0, "*"))

    print("Rectangle Zero:")
    print(art.draw_rectangle(0, 3, "#"))
        
    print("Rectangle Zero 2:")
    print(art.draw_rectangle(7, 0, "#"))
            
    print("Parallelogram Zero:")
    print(art.draw_parallelogram(0, 4, "@"))
    
    print("Triangle Zero:")
    print(art.draw_triangle(0, 7, "+"))
        
    print("Pyramid, zero height")
    print(art.draw_pyramid(0, "$"))
