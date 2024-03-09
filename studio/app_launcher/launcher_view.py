from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout, QPushButton
from launcher import ConfigReader
class Launcher(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("DCC Launcher")
        self.setGeometry(100,100,100,100)

        self.config = ConfigReader()
        self.launchers = self.config.get_launchers()
        self.draw()

    def draw(self):
        layout = QVBoxLayout(self)
        for launcher in self.launchers:
            button = QPushButton(launcher.__name__, self)
            button.clicked.connect(launcher._default_launch)
            layout.addWidget(button)

        