
import sys
import os 

from PySide6.QtWidgets import QDialog, QApplication
from launcher_view import Launcher

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = Launcher()
    dialog.show()
    sys.exit(app.exec())