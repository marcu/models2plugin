import os
from pathlib import Path

from qgis.core import QgsProcessingModelAlgorithm, QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

DIR_PLUGIN_ROOT: Path = Path(__file__).parent


class Provider(QgsProcessingProvider):
    """The provider of our plugin."""

    def loadAlgorithms(self):
        for model_path in DIR_PLUGIN_ROOT.glob("models/*.model3"):
            model = QgsProcessingModelAlgorithm()
            if model.fromFile(str(model_path)):
                self.addAlgorithm(model)

    def id(self) -> str:
        """The ID of the provider"""
        return "{{ plugin_provider_id }}"

    def name(self) -> str:
        """Human friendly name for the provider in Processing."""
        return self.tr("{{plugin_name}}")

    def icon(self) -> QIcon:
        """The icon for your plugin in Processing."""
        icon_path = os.path.join(os.path.dirname(__file__), "icon.svg")
        return QIcon(icon_path)
