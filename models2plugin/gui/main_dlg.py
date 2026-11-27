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
from models2plugin.toolbelt import PlgOptionsManager
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

        self.modelsFolderFileWidget.setStorageMode(
            QgsFileWidget.StorageMode.GetDirectory
        )
        # Force Qt's own directory picker: the system/KDE native one ignores the
        # suggested starting folder and reopens on its own last-used location.
        self.modelsFolderFileWidget.setOptions(
            QtWidgets.QFileDialog.Option.DontUseNativeDialog
        )
        initial_models_folder = self.initial_models_folder()
        self.modelsFolderFileWidget.setDefaultRoot(initial_models_folder)
        self.modelsFolderFileWidget.setFilePath(initial_models_folder)
        self.modelsFolderFileWidget.fileChanged.connect(self.on_models_folder_changed)

        self.menu_widget.currentRowChanged.connect(self.display_page)
        self.nextButton.clicked.connect(self.go_to_next_page)
        self.previousButton.clicked.connect(self.go_to_previous_page)

        self.display_page(0)

        # display the models in the model list widget
        self.reload_model_list()

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

    def default_models_folder(self) -> str:
        """Returns QGIS' own models folder, used when no custom folder is set."""
        return os.path.join(
            QgsApplication.qgisSettingsDirPath(), "processing", "models"
        )

    def initial_models_folder(self) -> str:
        """Returns the models folder to pre-fill the widget with: the last folder
        the user picked, or QGIS' own models folder if none was saved yet."""
        saved_folder = PlgOptionsManager.get_plg_settings().models_folder
        return saved_folder or self.default_models_folder()

    def on_models_folder_changed(self, path: str):
        """Keeps the browse dialog anchored to the chosen folder and refreshes the list."""
        self.modelsFolderFileWidget.setDefaultRoot(path or self.default_models_folder())
        self.reload_model_list()

    def reload_model_list(self):
        """Refreshes the model list widget from the currently selected models folder."""
        self.modelListWidget.clear()
        for model_file in self.model_list_file_name():
            self.modelListWidget.addItem(model_file)

    def model_list_file_name(self):
        models_dir = (
            self.modelsFolderFileWidget.filePath() or self.default_models_folder()
        )

        if not os.path.isdir(models_dir):
            return []

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
