class AsciiArt:
    """
    A class for generating ASCII art shapes.  Meets ISO/IEC 25010 quality
    characteristics.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """Draws a square of the specified width using the given symbol.

        Args:
            width: The width of the square.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art square.

        Raises:
            ValueError: If width is not positive or symbol is invalid.
        """
        pass  # Implementation in the next step


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a rectangle of the specified width and height.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art rectangle.

        Raises:
            ValueError: If width/height are not positive or symbol is invalid.
        """
        pass


    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """Draws a parallelogram.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to use.

        Returns:
            A string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width/height are not positive or symbol is invalid.
        """
        pass

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a right-angled triangle.

        Args:
            width:  The width of the base of the triangle.
            height: The height of the triangle.
            symbol: The character to use.

        Returns:
            A string representing the ASCII art triangle.

        Raises:
            ValueError: If width/height are not positive or symbol is invalid.
        """
        pass

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """Draws a pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The character to use.

        Returns:
            A string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is not positive or symbol is invalid.
        """
        pass


    def _validate_input(self, dimensions: list[int], symbol: str):
        """Validates the input parameters.  Internal helper function."""
        if not all(dim > 0 for dim in dimensions):
            raise ValueError("Dimensions must be positive integers.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")



    def draw_square(self, width: int, symbol: str) -> str:
        """Draws a square of the specified width using the given symbol."""
        self._validate_input([width], symbol)  # Validate
        return "\n".join([symbol * width] * width)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a rectangle of the specified width and height."""
        self._validate_input([width, height], symbol)
        return "\n".join([symbol * width] * height)
    
    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """Draws a parallelogram."""
        self._validate_input([width, height], symbol)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return "\n".join(result)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a right-angled triangle."""
        self._validate_input([width, height], symbol)
        result = []
        for i in range(min(width,height)):  # Use min to handle non-square triangles
           result.append(symbol * (i + 1))
        return "\n".join(result)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """Draws a pyramid."""
        self._validate_input([height], symbol)
        result = []
        for i in range(height):
            spaces = " " * (height - 1 - i)
            symbols = symbol * (2 * i + 1)
            result.append(spaces + symbols)
        return "\n".join(result)



class AsciiArt:
    """
    A class for generating ASCII art shapes.  Meets ISO/IEC 25010 quality
    characteristics.
    """

    def _validate_input(self, dimensions: list[int], symbol: str):
        """Validates the input parameters.  Internal helper function."""
        if not all(dim > 0 for dim in dimensions):
            raise ValueError("Dimensions must be positive integers.")
        if len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")

    def draw_square(self, width: int, symbol: str) -> str:
        """Draws a square of the specified width using the given symbol."""
        self._validate_input([width], symbol)  # Validate
        return "\n".join([symbol * width] * width)

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a rectangle of the specified width and height."""
        self._validate_input([width, height], symbol)
        return "\n".join([symbol * width] * height)

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """Draws a parallelogram."""
        self._validate_input([width, height], symbol)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return "\n".join(result)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a right-angled triangle."""
        self._validate_input([width, height], symbol)
        result = []
        for i in range(min(width, height)):  # Use min to handle non-square triangles
            result.append(symbol * (i + 1))
        return "\n".join(result)


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """Draws a pyramid."""
        self._validate_input([height], symbol)
        result = []
        for i in range(height):
            spaces = " " * (height - 1 - i)
            symbols = symbol * (2 * i + 1)
            result.append(spaces + symbols)
        return "\n".join(result)



# Example Usage
if __name__ == "__main__":
    art_generator = AsciiArt()

    try:
        square = art_generator.draw_square(5, "#")
        print("Square:\n" + square)

        rectangle = art_generator.draw_rectangle(7, 3, "*")
        print("\nRectangle:\n" + rectangle)

        parallelogram = art_generator.draw_parallelogram(4, 6, "X")
        print("\nParallelogram:\n" + parallelogram)

        triangle = art_generator.draw_triangle(5, 5, "A")
        print("\nTriangle:\n" + triangle)
        
        pyramid = art_generator.draw_pyramid(4, "@")
        print("\nPyramid:\n" + pyramid)

        # Example of invalid input
        # invalid_square = art_generator.draw_square(-5, "&")  # Raises ValueError
        invalid_pyramid = art_generator.draw_pyramid(5, "  ")  # Raises ValueError

    except ValueError as e:
        print(f"Error: {e}")
