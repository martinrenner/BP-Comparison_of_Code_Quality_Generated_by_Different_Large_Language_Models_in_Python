class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """Draws a square of the specified width filled with the given symbol."""
        pass  # Implementation to be added later

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a rectangle of the specified width and height filled with the given symbol."""
        pass  # Implementation to be added later

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """Draws a parallelogram with the specified width and height, filled with the symbol."""
        pass  # Implementation to be added later

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a right-angled triangle with the specified width and height, filled with the symbol."""
        pass # Implementation to be added later
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """Draws a pyramid of the specified height filled with the given symbol."""
        pass  # Implementation to be added later


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None):
        """
        Validates the input parameters for the drawing functions.

        Args:
            symbol (str): The symbol to use for drawing.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If the input is invalid.
        """
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if width is not None and width <= 0:
            raise ValueError("Width must be a positive integer.")
        if height is not None and height <= 0:
            raise ValueError("Height must be a positive integer.")

    # ... (rest of the class definition - methods from Step 1) ...


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def _validate_input(self, symbol: str, width: int = None, height: int = None):
        """
        Validates the input parameters for the drawing functions.

        Args:
            symbol (str): The symbol to use for drawing.
            width (int, optional): The width of the shape.
            height (int, optional): The height of the shape.

        Raises:
            ValueError: If the input is invalid.
        """
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")
        if width is not None and width <= 0:
            raise ValueError("Width must be a positive integer.")
        if height is not None and height <= 0:
            raise ValueError("Height must be a positive integer.")
    
    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the specified width filled with the given symbol.

        Args:
            width (int): The width of the square.
            symbol (str): The symbol to fill the square with.

        Returns:
            str: A multi-line string representing the ASCII art square.

        Raises:
            ValueError: If input is invalid.        
        """
        self._validate_input(symbol, width=width)
        return '\n'.join([symbol * width for _ in range(width)])

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the specified width and height filled with the given symbol.

        Args:
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            symbol (str): The symbol to fill the rectangle with.

        Returns:
            str: A multi-line string representing the ASCII art rectangle.

        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(symbol, width=width, height=height)
        return '\n'.join([symbol * width for _ in range(height)])

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the specified width and height, filled with the symbol.

        Args:
            width (int): The width of the parallelogram.
            height (int): The height of the parallelogram.
            symbol (str): The symbol to use for drawing.

        Returns:
            str: A multi-line string representing the ASCII art parallelogram.

        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(symbol, width=width, height=height)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return '\n'.join(result)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width (int): The width of the triangle.
            height (int): The height of the triangle
            symbol (str): The symbol to use.

        Returns:
            str: Multiline string: ASCII art of the triangle.

        Raises:
            ValueError: If input is invalid
        """
        self._validate_input(symbol, width=width, height=height)
        # Ensure that triangle makes sense geometrically.
        if width > height:
            raise ValueError("For the triangle, height must be == with or greater than width ")

        result = []
        for i in range(1, width + 1):
            result.append(symbol * i)

        # Pad shorter lines according to height of rectangle to create shape of a right-angled triangle
        # Pad to the maximum width (last line of the output) 
        max_width = len(result[-1])  
        padded_result = [line.ljust(max_width) for line in result]
        return '\n'.join(padded_result)
    
    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a pyramid of the specified height filled with the given symbol.

        Args:
            height (int): The height of the pyramid.
            symbol (str): The symbol to fill the pyramid with.

        Returns:
            str: A multi-line string representing the ASCII art pyramid.
        
        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(symbol, height=height)
        result = []
        for i in range(1, height + 1):
            padding = " " * (height - i)
            result.append(padding + symbol * (2 * i - 1) + padding)
        return '\n'.join(result)


# Example usage
if __name__ == "__main__":
    art = AsciiArt()

    try:
        print("Square:")
        print(art.draw_square(5, "#"))

        print("\nRectangle:")
        print(art.draw_rectangle(7, 3, "*"))

        print("\nParallelogram:")
        print(art.draw_parallelogram(6, 4, "@"))
        
        print("\nTriangle:")
        print(art.draw_triangle(5, 5, "+"))

        print("\nPyramid:")
        print(art.draw_pyramid(5, "$"))

        # Example of invalid input
        # print("\nInvalid Square:")
        # print(art.draw_square(-5, "#"))  # This will raise a ValueError

        # print(art.draw_square(5, "##")) # This will raise a ValueError
    except ValueError as e:
        print(f"Error: {e}")
