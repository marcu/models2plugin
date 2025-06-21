import os
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

        self.menu_widget.currentRowChanged.connect(self.handle_page_change)

        # display the models in the model list widget
        for model_file in self.modelListFileName():
            self.modelListWidget.addItem(model_file)

    def handle_page_change(self, index: int):
        """Handles page switching and clears selection in all layers."""

        self.stacked_panels_widget.setCurrentIndex(index)

    def modelListFileName(self):
        current_profile = iface.userProfileManager().getProfile()
        current_profile_folder = current_profile.folder()

        models_dir = os.path.join(current_profile_folder, "processing", "models")

        return [
            filename
            for filename in os.listdir(models_dir)
            if filename.endswith(".model3")
        ]
