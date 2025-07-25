from pathlib import Path

from qgis.gui import QgisInterface
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox

DIR_PLUGIN_ROOT: Path = Path(__file__).parent


class MainPlugin:

    def __init__(self, iface: QgisInterface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class which \
        provides the hook by which you can manipulate the QGIS application at run time.
        :type iface: QgsInterface
        """
        self.iface = iface
        self.dlg = None

    def initGui(self):
        # create action that will start plugin configuration
        main_action_icon_path = DIR_PLUGIN_ROOT / "icon.png"
        self.action = QAction(
            QIcon(str(main_action_icon_path)),
            "Generated plugin",
            self.iface.mainWindow(),
        )

        self.action.setObjectName("runAction")
        self.action.setWhatsThis("Configuration for test plugin")
        self.action.setStatusTip("This is status tip")
        self.action.triggered.connect(self.run)

        # add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Generated plugin", self.action)

    def unload(self):
        # remove the plugin menu item and icon
        self.iface.removePluginMenu("&Generated plugin", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        # create and show a configuration dialog or something similar

        QMessageBox.information(
            self.iface.mainWindow(),
            "Info",
            "The action of the generated plugin has been triggered.",
        )
