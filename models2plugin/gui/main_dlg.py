import os
from pathlib import Path

from qgis.core import (
    QgsApplication,
    QgsExpression,
    QgsExpressionContext,
    QgsExpressionContextUtils,
)
from qgis.gui import QgsFileWidget
from qgis.PyQt import QtWidgets, uic

from models2plugin.__about__ import DIR_PLUGIN_ROOT
from models2plugin.toolbelt.utils import get_text_content, to_snake_case

FORM_CLASS, _ = uic.loadUiType(
    Path(__file__).parent / "{}.ui".format(Path(__file__).stem)
)


class MainDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.authorLineEdit.setText(self.current_qgis_user())
        self.outputDirectoryFileWidget.setStorageMode(
            QgsFileWidget.StorageMode.GetDirectory
        )

        self.menu_widget.currentRowChanged.connect(self.display_page)
        self.nextButton.clicked.connect(self.go_to_next_page)
        self.previousButton.clicked.connect(self.go_to_previous_page)

        self.display_page(0)

        # display the models in the model list widget
        for model_file in self.modelListFileName():
            self.modelListWidget.addItem(model_file)

        self.pluginNameLineEdit.editingFinished.connect(
            self.updateOutputDirectoryFileSlot
        )

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

    def current_qgis_user(self) -> str:
        """With a QGIS Expression, returns the current user name."""
        context = QgsExpressionContext()
        context.appendScope(QgsExpressionContextUtils.globalScope())
        expression = QgsExpression("@user_full_name")
        return expression.evaluate(context)

    def modelListFileName(self):
        models_dir = os.path.join(
            QgsApplication.qgisSettingsDirPath(), "processing", "models"
        )

        return [
            filename
            for filename in os.listdir(models_dir)
            if filename.endswith(".model3")
        ]

    def updateOutputDirectoryFileSlot(self):
        """Update the output directory based on the plugin name."""

        plugin_name = get_text_content(self.pluginNameLineEdit, "MyPlugin")
        plugin_folder_name = to_snake_case(plugin_name)
        plugin_template_dir = Path(DIR_PLUGIN_ROOT, "output", plugin_folder_name)
        self.outputDirectoryFileWidget.setFilePath(str(plugin_template_dir))
