"""
All configuration constants/parameters
"""

class ChessConfig:

    def __init__(self):
        """
        """
        self.AI_THINKING = False
        self.ANIMATE = False
        self.BOARD_HEIGHT = 512
        self.BOARD_WIDTH = 512
        self.CHECKMATE = 1000
        self.DEPTH = 3
        self.DIMENSION = 8
        self.IMAGES = {}
        self.IMAGES_SET = "set-a"
        self.MAX_FPS = 10
        self.MOVE_PANEL_HEIGHT = self.BOARD_HEIGHT
        self.MOVE_PANEL_WIDTH = 250
        self.PLAYER_ONE = False
        self.PLAYER_TWO = False
        self.SQUARE_SIZE = self.BOARD_HEIGHT // self.DIMENSION
        self.STALEMATE = 0
        self.WITH_UI = False

        # COLORS
        self.COLOR_BLACK = "black"
        self.COLOR_FONT = "black"
        self.COLOR_HISTORY = "gray"
        self.COLOR_PATH = "yellow"
        self.COLOR_SCREEN = "white"
        self.COLOR_SELECTED = "red"
        self.COLOR_SQUARE_BLACK = "chocolate"
        self.COLOR_SQUARE_WHITE = "papayawhip"
        self.COLOR_TARGET = "green"
        self.COLOR_WHITE = "white"

        # FONTS
        self.FONT_ENDTEXT = "Helvetica"
        self.FONT_HISTORY = "Arial"