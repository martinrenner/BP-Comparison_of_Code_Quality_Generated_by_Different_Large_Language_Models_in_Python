class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def draw_square(self, width: int, symbol: str) -> str:
        """Draws a square of the given width using the specified symbol.

        Args:
            width: The width of the square.
            symbol: The character to use for drawing the square.

        Returns:
            A string representing the ASCII art square.

        Raises:
            ValueError: If width is not positive or symbol is invalid.
        """
        raise NotImplementedError()

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a rectangle of the given dimensions using the specified symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art rectangle.

        Raises:
            ValueError: If width/height are not positive or symbol is invalid.
        """
        raise NotImplementedError()

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """Draws a parallelogram.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art parallelogram.

        Raises:
            ValueError: If width/height are not positive or symbol is invalid.
        """
        raise NotImplementedError()

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a right-angled triangle.

        Args:
            width: The width of the triangle's base.
            height: The height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art triangle.
        Raises:
            ValueError: If width/height are not positive or symbol is invalid.
        """
        raise NotImplementedError()


    def draw_pyramid(self, height: int, symbol: str) -> str:
        """Draws a symmetrical pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The character to use for drawing.

        Returns:
            A string representing the ASCII art pyramid.

        Raises:
            ValueError: If height is not positive or symbol is invalid.

        """
        raise NotImplementedError()


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def _validate_input(self, dimensions: list[int], symbol: str):
        """Validates the input parameters for drawing functions.

        Args:
            dimensions: A list of integer dimensions (width, height, etc.).
            symbol: The drawing symbol.

        Raises:
            ValueError: If dimensions are not positive or symbol is invalid.
        """

        for dim in dimensions:
            if not isinstance(dim, int) or dim <= 0:
                raise ValueError("Dimensions must be positive integers.")

        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")

        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """Draws a square of the given width, filled with symbol."""
        raise NotImplementedError()

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a rectangle, filled with symbol."""
        raise NotImplementedError()

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """Draws a parallelogram, filled with symbol."""
        raise NotImplementedError()

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a right-angled triangle, filled with symbol."""
        raise NotImplementedError()

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """Draws a symmetrical pyramid filled with symbol."""
        raise NotImplementedError()


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def _validate_input(self, dimensions: list[int], symbol: str):
        """Validates the input parameters for drawing functions."""

        for dim in dimensions:
            if not isinstance(dim, int) or dim <= 0:
                raise ValueError("Dimensions must be positive integers.")

        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")

        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """Draws a square of the given width, filled with symbol."""
        self._validate_input([width], symbol)
        return (symbol * width + "\n") * width

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a rectangle, filled with symbol."""
        self._validate_input([width, height], symbol)
        return (symbol * width + "\n") * height

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """Draws a parallelogram, filled with symbol."""
        self._validate_input([width, height], symbol)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return "\n".join(result)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a right-angled triangle, filled with symbol."""
        self._validate_input([width, height], symbol)
        result = []

        # Check that the triangle can be drawn
        if width > height:
            raise ValueError("In a right-angled triangle, height must be bigger or equal to width.")

        for i in range(height):
            if i < width:
              result.append(symbol * (i + 1))
            else:
              result.append(symbol * width)
        return "\n".join(result)
        

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """Draws a symmetrical pyramid filled with symbol."""
        self._validate_input([height], symbol)
        result = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            result.append(spaces + symbols)
        return "\n".join(result)


if __name__ == "__main__":
    art = AsciiArt()

    # Test Cases
    try:
        print("Square (5x5, '*'):")
        print(art.draw_square(5, "*"))

        print("\nRectangle (7x3, '#'):")
        print(art.draw_rectangle(7, 3, "#"))

        print("\nParallelogram (4x6, '+'):")
        print(art.draw_parallelogram(4, 6, "+"))

        print("\nTriangle (5x5, 'X'):")
        print(art.draw_triangle(5, 5, "X"))
        
        print("\nPyramid (5, '@'):")
        print(art.draw_pyramid(5, "@"))

        # Example of invalid input
        print("\nInvalid Input Test (Square with negative width):")
        print(art.draw_square(-5, "*"))  # This will raise a ValueError

    except ValueError as e:
        print(f"Error: {e}")


class AsciiArt:
    """
    A class for generating ASCII art shapes.
    """

    def _validate_input(self, dimensions: list[int], symbol: str):
        """Validates the input parameters for drawing functions."""

        for dim in dimensions:
            if not isinstance(dim, int) or dim <= 0:
                raise ValueError("Dimensions must be positive integers.")

        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")

        if symbol.isspace():
            raise ValueError("Symbol cannot be a whitespace character.")

    def draw_square(self, width: int, symbol: str) -> str:
        """Draws a square of the given width, filled with symbol."""
        self._validate_input([width], symbol)
        return (symbol * width + "\n") * width

    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a rectangle, filled with symbol."""
        self._validate_input([width, height], symbol)
        return (symbol * width + "\n") * height

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """Draws a parallelogram, filled with symbol."""
        self._validate_input([width, height], symbol)
        result = []
        for i in range(height):
            result.append(" " * i + symbol * width)
        return "\n".join(result)

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a right-angled triangle, filled with symbol."""
        self._validate_input([width, height], symbol)
        result = []

        # Check that the triangle can be drawn
        if width > height:
            raise ValueError("In a right-angled triangle, height must be bigger or equal to width.")

        for i in range(height):
            if i < width:
              result.append(symbol * (i + 1))
            else:
              result.append(symbol * width)
        return "\n".join(result)

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """Draws a symmetrical pyramid filled with symbol."""
        self._validate_input([height], symbol)
        result = []
        for i in range(height):
            spaces = " " * (height - i - 1)
            symbols = symbol * (2 * i + 1)
            result.append(spaces + symbols)
        return "\n".join(result)
        

if __name__ == "__main__":
    art = AsciiArt()

    # Test Cases
    try:
        print("Square (5x5, '*'):")
        print(art.draw_square(5, "*"))

        print("\nRectangle (7x3, '#'):")
        print(art.draw_rectangle(7, 3, "#"))

        print("\nParallelogram (4x6, '+'):")
        print(art.draw_parallelogram(4, 6, "+"))

        print("\nTriangle (5x5, 'X'):")
        print(art.draw_triangle(5, 5, "X"))
        
        print("\nPyramid (5, '@'):")
        print(art.draw_pyramid(5, "@"))

        # Example of invalid input
        print("\nInvalid Input Test (Square with negative width):")
        print(art.draw_square(-5, "*"))  # This will raise a ValueError

    except ValueError as e:
        print(f"Error: {e}")
