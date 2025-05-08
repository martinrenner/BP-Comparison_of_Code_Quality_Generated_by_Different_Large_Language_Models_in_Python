class AsciiArt:
    """
    A class for generating various ASCII art shapes.
    """

    def _validate_input(self, symbol: str):
        """Validates the input symbol.

        Args:
            symbol: The symbol to use for drawing.

        Raises:
            ValueError: If the symbol is invalid.
        """
        if len(symbol) != 1:
            raise ValueError("Symbol must be exactly one character long.")
        if symbol.isspace():
            raise ValueError("Symbol cannot be whitespace.")

    def _validate_dimensions(self, width: int, height: int = None):
        """Validates the width and height.

        Args:
            width: The width of the shape.
            height: The height of the shape (optional for shapes like squares).

        Raises:
            ValueError: If width or height is invalid.
        """
        if width < 0:
            raise ValueError("Width cannot be negative.")
        if height is not None and height < 0:
            raise ValueError("Height cannot be negative.")
        
    def _validate_height(self, height: int):
      """Validates the height"""

      if height < 0:
        raise ValueError("Height cannot be negative")

    def draw_square(self, width: int, symbol: str) -> str:
        """Draws a square of the given width using the specified symbol.

        Args:
            width: The width of the square.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the square.

        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(symbol)
        self._validate_dimensions(width)

        if width == 0:  # Handle edge Case
            return ""

        square = (symbol * width + "\n") * width
        return square.rstrip("\n") #removing last \n to follow the requirements


    def draw_rectangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a rectangle of the given width and height using the specified symbol.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the rectangle.

        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(symbol)
        self._validate_dimensions(width, height)

        if width == 0 or height == 0: # Handle edge Case
            return ""

        rectangle = (symbol * width + "\n") * height
        return rectangle.rstrip("\n") #removing last \n to follow the requirements

    def draw_parallelogram(self, width: int, height: int, symbol: str) -> str:
        """Draws a parallelogram.

        Args:
            width: The width of the parallelogram.
            height: The height of the parallelogram.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the parallelogram.

        Raises:
             ValueError: If input is invalid.
        """
        self._validate_input(symbol)
        self._validate_dimensions(width, height)
        if width == 0 or height == 0:  # Handle edge case
            return ""

        parallelogram = ""
        for i in range(height):
            parallelogram += " " * i + symbol * width + "\n"
        return parallelogram.rstrip("\n") #removing last \n to follow the requirements

    def draw_triangle(self, width: int, height: int, symbol: str) -> str:
        """Draws a right-angled triangle.

         Args:
            width: Max width of the triangle.
            height: The height of the triangle.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the triangle.

        Raises:
            ValueError: If input is invalid.
        """
        self._validate_input(symbol)
        self._validate_dimensions(width, height)

        if width == 0 or height == 0: # Handle edge Case
            return ""

        triangle = ""
        for i in range(height):
          current_width = int(width * (i+1) / height) #calculating current width and converting to int
          if current_width > 0: #prevent adding lines with 0 width
            triangle += symbol * current_width + "\n"

        return triangle.rstrip("\n") #removing last \n to follow the requirements

    def draw_pyramid(self, height: int, symbol: str) -> str:
        """Draws a symmetrical pyramid.

        Args:
            height: The height of the pyramid.
            symbol: The character to use for drawing.

        Returns:
            A multi-line string representing the pyramid.

        Raises:
            ValueError: If input is invalid.
        """

        self._validate_input(symbol)
        self._validate_height(height)

        if height == 0:
            return ""
        
        pyramid = ""
        for i in range(height):
            spaces = " " * (height - 1 - i)
            symbols = symbol * (2 * i + 1)
            pyramid += spaces + symbols + "\n"
        return pyramid.rstrip("\n")  #removing last \n to follow the requirements


# Example Usage
if __name__ == "__main__":
    art_generator = AsciiArt()

    try:
        print("Square:\n" + art_generator.draw_square(5, "*"))
        print("\nRectangle:\n" + art_generator.draw_rectangle(7, 3, "#"))
        print("\nParallelogram:\n" + art_generator.draw_parallelogram(6, 4, "@"))
        print("\nTriangle:\n" + art_generator.draw_triangle(5, 5, "+"))  # Classic triangle
        print("\nTriangle (Different Width/Height):\n" + art_generator.draw_triangle(10, 5, "+")) # Wider triangle
        print("\nTriangle (Different Width/Height):\n" + art_generator.draw_triangle(3, 6, "+")) # Taller triangle
        print("\nPyramid:\n" + art_generator.draw_pyramid(5, "$"))
        print("\nSquare (Zero Size):\n" + art_generator.draw_square(0, "*")) #Testing edge case
        print("\nRectangle (Zero Width):\n" + art_generator.draw_rectangle(0,4,"+")) #Testing edge case
        print("\nRectangle (Zero height):\n" + art_generator.draw_rectangle(4,0,"+"))#Testing edge case
        print("\nParalelogram (Zero Size):" + art_generator.draw_parallelogram(0,0,"+"))  #Testing edge case
        print("\nTriangle (Zero Size):" + art_generator.draw_triangle(0,10,"+"))#Testing edge case
        print("\nPyramid:\n" + art_generator.draw_pyramid(0, "$")) #Testing edge case

        # Example of invalid input (uncomment to test)
        #print("\nInvalid Input:\n" + art_generator.draw_square(4, "  "))
        # print("\nInvalid Input:\n" + art_generator.draw_square(4, "AB"))
        #print("\nInvalid Input:\n" + art_generator.draw_square(-4, "*"))


    except ValueError as e:
        print(f"Error: {e}")
