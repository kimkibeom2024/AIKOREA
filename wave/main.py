import sys
from PyQt5.QtWidgets import QApplication
from ui.game_gui import PronunciationGame

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = PronunciationGame()
    game.show()
    sys.exit(app.exec_())