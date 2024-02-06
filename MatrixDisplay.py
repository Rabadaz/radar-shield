from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class MatrixDisplay:

    #Color deffinitions
    GREEN = graphics.Color(0,255,0)
    YELLOW = graphics.Color(255,165,0)
    RED = graphics.Color(255,0,0)
    WHITE = graphics.Color(255,255,255)
    BLACK = graphics.Color(0,0,0)

    def __init__(self, nRows=32, nCols=64, font_path="/home/pi/rpi-rgb-led-matrix/fonts/7x13.bdf"):
        self.options = RGBMatrixOptions()
        self.options.rows = nRows
        self.options.cols = nCols
        self.options.chain_length=1
        self.options.parallel = 1
        self.options.hardware_mapping= 'regular'

        self.font = graphics.Font()
        self.font.LoadFont(font_path)

        self.matrix = RGBMatrix(options=self.options)
        self.canvas = self.matrix.CreateFrameCanvas()

    def _drawRect(self, x1, y1, x2, y2):
        for y in range(y1, y2):
            graphics.DrawLine(self.canvas, x1, y, x2, y, self.BLACK)

    def update(self, value, highScore):
        self._drawRect(0,15,31,31)

        #Postitions von originalem Radarshield übernommen ??
        graphics.DrawText(self.canvas, self. font, (self.matrix.width /15), (self.matrix.height -5),self.GREEN, '{0:.1f}'.format(value))
        graphics.DrawLine(self.canvas, 0, 13, 64, 13, self.RED)
        graphics.DrawText(self.canvas, self.font, (self.matrix.width / 15 -5), (self.matrix.height -20),self.RED, "Score")
        graphics.DrawText(self.canvas, self.font, (self.matrix.width/1.8), (self.matrix.height-5), self.GREEN, "km/h")
        graphics.DrawText(self.canvas, self.font, (self.matrix.width/1.7), (self.matrix.height-20), self.RED, '{0:.1f}'.format(highScore))
        self.matrix.SwapOnVSync(self.canvas)

