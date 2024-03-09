import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget, QHBoxLayout, QToolButton, QVBoxLayout, QFileDialog, QPushButton
from PySide6.QtGui import QIcon
from launcher import ConfigReader

class Launcher(QDialog):
    "The dialog for Launching applications with environment variables"

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Blender Launcher")
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
        
        #Create a button for all launchers in the config
        for launcher in self.launchers:
            launch_button = QToolButton(self)
            launch_button.setIcon(QIcon(os.path.join(resources_path, launcher.__logo__)))
            launch_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # Set button style to remove border
            launch_button.setAutoRaise(True)  # Remove background color when mouse over
            launch_button.setFixedSize(80, 80)  # Set button size
            launch_button.setIconSize(launch_button.size())  # Set the icon size to match the button size

            launch_button.clicked.connect(launcher._launch)
            application_layout.addWidget(launch_button)
            
        #Create a button for selecting an asset
        browse_asset_button = QPushButton("Open Asset")
        browse_asset_button.clicked.connect(self.asset_launch)

        layout.addWidget(applications_widget)
        layout.addWidget(browse_asset_button)

    def asset_launch(self):
         "Launch the asset with the selected launcher, defaults to first in config"
         asset_path = self.open_file()
         self.selected_launcher.asset_launch(asset_path)

    def open_file(self) -> str:
            "Open File Dialog and return selected items path"
            file_dialog = QFileDialog(self)
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            if file_dialog.exec():
                selected_files = file_dialog.selectedFiles()
                if selected_files:
                    file_path = selected_files[0]
                    return file_path

        