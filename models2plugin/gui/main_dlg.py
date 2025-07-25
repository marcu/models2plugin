import os
from functools import partial
from pathlib import Path

from qgis.PyQt import QtWidgets, uic
from qgis.utils import iface

FORM_CLASS, _ = uic.loadUiType(
    Path(__file__).parent / "{}.ui".format(Path(__file__).stem)
)


class MainDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.menu_widget.currentRowChanged.connect(self.display_page)
        self.nextButton.clicked.connect(self.go_to_next_page)
        self.previousButton.clicked.connect(self.go_to_previous_page)

        self.display_page(0)

        # display the models in the model list widget
        for model_file in self.modelListFileName():
            self.modelListWidget.addItem(model_file)

    def go_to_next_page(self):
        """Switches to the next page in the stacked widget."""
        current_index = self.stacked_panels_widget.currentIndex()
        next_index = current_index + 1
        self.display_page(next_index)

    def go_to_previous_page(self):
        """Switches to the previous page in the stacked widget."""
        current_index = self.stacked_panels_widget.currentIndex()
        previous_index = current_index - 1
        self.display_page(previous_index)

    def display_page(self, index: int):
        """Displays the specified page in the stacked widget."""

        if 0 <= index < self.stacked_panels_widget.count():
            self.stacked_panels_widget.setCurrentIndex(index)

        self.menu_widget.setCurrentRow(index)

        previous_button_enabled = index > 0
        self.previousButton.setEnabled(previous_button_enabled)

        next_button_enabled = index < self.stacked_panels_widget.count() - 1
        self.nextButton.setEnabled(next_button_enabled)

    def modelListFileName(self):
        current_profile = iface.userProfileManager().getProfile()
        current_profile_folder = current_profile.folder()

        models_dir = os.path.join(current_profile_folder, "processing", "models")

        return [
            filename
            for filename in os.listdir(models_dir)
            if filename.endswith(".model3")
        ]
