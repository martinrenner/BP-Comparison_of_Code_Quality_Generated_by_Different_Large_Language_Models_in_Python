class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """
        Draws a square of the given width using the specified symbol.

        Args:
            width: The width of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A string representing the ASCII art square.

        Raises:
            ValueError: If width is not positive or symbol is invalid.
        """
        self._validate_input(width, symbol)
        return self._draw_rectangle(width, width, symbol)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a rectangle of the given width and height using the specified symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A string representing the ASCII art rectangle.

        Raises:
           ValueError: If width or height is not positive or symbol is invalid.
        """

        self._validate_input(width, symbol)
        self._validate_positive_dimension(height, "Height")

        rows = []
        for _ in range(height):
            rows.append(symbol * width)
        return "\n".join(rows)
      
    def _draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """
        Internal function that draws a rectangle of the given width and height using the specified symbol.
        Note: It does not validate input and should be used only by class's methods

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing the rectangle.

        Returns:
            A string representing the ASCII art rectangle.
        """

        rows = []
        for _ in range(height):
            rows.append(symbol * width)
        return "\n".join(rows)


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a parallelogram with the given width, height, and symbol.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width or height is not positive or symbol is invalid.
        """
        self._validate_input(width, symbol)
        self._validate_positive_dimension(height, "Height")

        rows = []
        for i in range(height):
            rows.append(" " * i + symbol * width)
        return "\n".join(rows)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """
        Draws a right-angled triangle.

        Args:
            width: The max width of the triangle.
            height: The height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art triangle.

        Raises:
            ValueError: If width or height is not positive or symbol is invalid.
        """
        self._validate_input(width, symbol)
        self._validate_positive_dimension(height, "Height")

        rows = []
        for i in range(height):
          row_width = int(width * (i+1) / height) #scale width
          rows.append(symbol*row_width)
        return "\n".join(rows)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """
        Draws a symmetrical pyramid with the given height and symbol.

        Args:
            height: The height of the pyramid.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is not positive or symbol is invalid.
        """
        self._validate_input(1, symbol) #use dummy width 1
        self._validate_positive_dimension(height, "Height")
        rows = []
        for i in range(height):
            width = 2 * i + 1
            padding = height - 1 - i
            rows.append(" " * padding + symbol * width)
        return "\n".join(rows)


    def _validate_input(self, dimension: int, symbol: str):
        """Validates the input parameters."""
        self._validate_positive_dimension(dimension, "Width/Dimension")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")

    def _validate_positive_dimension(self, dimension: int, dimension_name: str):
       """Validates that dimension is a positive integer"""
       if not isinstance(dimension, int) or dimension <= 0:
            raise ValueError(f"{dimension_name} must be a positive integer.")


# Example Usage (and basic testing)
if __name__ == '__main__':
    art = AsciiArt()

    try:
        square = art.draw_square(5, "*")
        print("Square:\n" + square)

        rectangle = art.draw_rectangle(7, 3, "#")
        print("\nRectangle:\n" + rectangle)

        parallelogram = art.draw_parallelogram(6, 4, "+")
        print("\nParallelogram:\n" + parallelogram)

        triangle = art.draw_triangle(5,5, "X")
        print("\nTriangle:\n" + triangle)


        pyramid = art.draw_pyramid(5, "O")
        print("\nPyramid:\n" + pyramid)
        
        # Test cases with invalid input
        print("\n--Testing invalid inputs--")
        try:
             art.draw_square(-5, "*")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            art.draw_rectangle(4, 6, "##")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        try:
            art.draw_pyramid(5, " ")
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        try:
            art.draw_triangle(5.5, 5, " ")
        except ValueError as e:
            print(f"Caught expected error: {e}")   

        try:
            art.draw_triangle(5, 5.66, " ")
        except ValueError as e:
            print(f"Caught expected error: {e}")            

    except ValueError as e:
        print(f"Error: {e}")
