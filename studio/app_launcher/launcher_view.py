import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget, QHBoxLayout, QToolButton, QVBoxLayout, QFileDialog, QPushButton
from PySide6.QtGui import QIcon
from launcher import ConfigReader

class Launcher(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("DCC Launcher")
        self.setGeometry(100,100,400,300)

        self.config = ConfigReader()
        self.launchers = self.config.get_launchers()
        self.selected_launcher = self.launchers[0]

        self.draw()

    def draw(self):
        layout = QVBoxLayout(self)

        applications_widget = QWidget()
        application_layout = QHBoxLayout(applications_widget)
        application_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        resources_path = os.path.join(os.path.dirname(__file__), "resources")
        for launcher in self.launchers:
            software_launch_button = QToolButton(self)
            software_launch_button.setIcon(QIcon(os.path.join(resources_path, launcher.__logo__)))
            software_launch_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # Set button style to remove border
            software_launch_button.setAutoRaise(True)  # Remove background color when mouse over
            software_launch_button.setFixedSize(80, 80)  # Set button size
            software_launch_button.setIconSize(software_launch_button.size())  # Set the icon size to match the button size

            software_launch_button.clicked.connect(launcher._default_launch)
            application_layout.addWidget(software_launch_button)
            

        browse_asset_button = QPushButton("Open Asset")
        browse_asset_button.clicked.connect(self.launch_asset)
        layout.addWidget(applications_widget)
        layout.addWidget(browse_asset_button)

    def launch_asset(self):
         asset_path = self.openFile()
         self.selected_launcher.asset_launch(asset_path)

    def openFile(self):
            # Get the path to the resources folder
            resources_path = os.path.join(os.path.dirname(__file__), "resources")

            # Open a file dialog to select a .blend file
            file_dialog = QFileDialog(self)
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter("Blend files (*.blend)")
            if file_dialog.exec():
                selected_files = file_dialog.selectedFiles()
                if selected_files:
                    file_path = selected_files[0]
                    return file_path

        