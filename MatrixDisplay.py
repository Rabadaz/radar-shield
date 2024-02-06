from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics


class MatrixDisplay:
    # Color deffinitions
    GREEN = graphics.Color(0, 255, 0)
    YELLOW = graphics.Color(255, 165, 0)
    RED = graphics.Color(255, 0, 0)
    WHITE = graphics.Color(255, 255, 255)
    BLACK = graphics.Color(0, 0, 0)

    def __init__(self, n_rows=32, n_cols=64, font_path="/home/pi/rpi-rgb-led-matrix/fonts/7x13.bdf"):
        self.options = RGBMatrixOptions()
        self.options.rows = n_rows
        self.options.cols = n_cols
        self.options.chain_length = 1
        self.options.parallel = 1
        self.options.hardware_mapping = 'regular'

        self.font = graphics.Font()
        self.font.LoadFont(font_path)

        self.matrix = RGBMatrix(options=self.options)
        self.canvas = self.matrix.CreateFrameCanvas()

    def _drawRect(self, x1, y1, x2, y2):
        for y in range(y1, y2):
            graphics.DrawLine(self.canvas, x1, y, x2, y, self.BLACK)

    def __draw_base_image(self, speed):
        #self._drawRect(0, 15, 31, 31)
        self.canvas.Clear()
        graphics.DrawLine(self.canvas, 0, 13, 64, 13, self.RED)
        graphics.DrawText(self.canvas, self.font, (self.matrix.width / 15), (self.matrix.height - 5), self.GREEN,
                          '{0:.1f}'.format(speed))
        graphics.DrawText(self.canvas, self.font, (self.matrix.width / 1.8), (self.matrix.height - 5), self.GREEN,
                          "km/h")

    def display_measurement(self, value, high_score, beating_score):
        # Postitions von originalem Radarshield übernommen ??
        self.__draw_base_image(value)
        graphics.DrawText(self.canvas, self.font, (self.matrix.width / 1.7), (self.matrix.height - 20),
                          self.RED if beating_score else self.GREEN, '{0:.1f}'.format(high_score))
        graphics.DrawText(self.canvas, self.font, (self.matrix.width / 15 - 5), (self.matrix.height - 20),
                          self.RED if beating_score else self.GREEN, "Score")
        self.matrix.SwapOnVSync(self.canvas)

    def display_print_message(self, high_score):
        self.__draw_base_image(high_score)
        graphics.DrawText(self.canvas, self.font, (self.matrix.width / 1.7), (self.matrix.height - 20), self.RED,
                          "Print?")
        self.matrix.SwapOnVSync(self.canvas)

    def display_high_score(self, high_score):
        self.__draw_base_image(high_score)
        graphics.DrawText(self.canvas, self.font, (self.matrix.width / 1.7), (self.matrix.height - 20), self.RED,
                          "Highscore!")
        self.matrix.SwapOnVSync(self.canvas)
