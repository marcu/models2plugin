#! python3  # noqa: E265

"""Main plugin module."""

import os

# standard
from functools import partial
from pathlib import Path

# PyQGIS
from qgis.core import QgsApplication, QgsSettings
from qgis.gui import QgisInterface
from qgis.PyQt.QtCore import QCoreApplication, QLocale, QTranslator, QUrl
from qgis.PyQt.QtGui import QDesktopServices, QIcon
from qgis.PyQt.QtWidgets import QAction

# project
from models2plugin.__about__ import (
    DIR_PLUGIN_ROOT,
    __icon_path__,
    __title__,
    __uri_homepage__,
)
from models2plugin.gui.dlg_settings import PlgOptionsFactory
from models2plugin.gui.main_dlg import MainDialog
from models2plugin.toolbelt import PlgLogger
from models2plugin.toolbelt.utils import get_line_edit_content, to_snake_case

from .generator import generate

# ############################################################################
# ########## Classes ###############
# ##################################


class Models2PluginPlugin:
    def __init__(self, iface: QgisInterface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class which \
        provides the hook by which you can manipulate the QGIS application at run time.
        :type iface: QgsInterface
        """
        self.iface = iface
        self.log = PlgLogger().log
        self.model_list_dlg = None

        self.actions: list[QAction] = []

        # translation
        # initialize the locale
        self.locale: str = QgsSettings().value("locale/userLocale", QLocale().name())[
            0:2
        ]
        locale_path: Path = (
            DIR_PLUGIN_ROOT
            / "resources"
            / "i18n"
            / f"{__title__.lower()}_{self.locale}.qm"
        )
        self.log(message=f"Translation: {self.locale}, {locale_path}", log_level=4)
        if locale_path.exists():
            self.translator = QTranslator()
            self.translator.load(str(locale_path.resolve()))
            QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        """Set up plugin UI elements."""

        # settings page within the QGIS preferences menu
        self.options_factory = PlgOptionsFactory()
        self.iface.registerOptionsWidgetFactory(self.options_factory)

        # -- Actions
        self.action_help = QAction(
            QgsApplication.getThemeIcon("mActionHelpContents.svg"),
            self.tr("Help"),
            self.iface.mainWindow(),
        )
        self.action_help.triggered.connect(
            partial(QDesktopServices.openUrl, QUrl(__uri_homepage__))
        )

        self.action_settings = QAction(
            QgsApplication.getThemeIcon("console/iconSettingsConsole.svg"),
            self.tr("Settings"),
            self.iface.mainWindow(),
        )
        self.action_settings.triggered.connect(
            lambda: self.iface.showOptionsDialog(
                currentPage="mOptionsPage{}".format(__title__)
            )
        )

        # Main Dialog
        self.main_dlg = MainDialog()

        self.main_dlg.generatePushButton.clicked.connect(self.generate_slot)

        main_dlg_icon_path = os.path.join(DIR_PLUGIN_ROOT, "resources/images/icon.png")

        self.action_main_dialog = QAction(
            QIcon(main_dlg_icon_path),
            self.tr("Main Dialog"),
            self.iface.mainWindow(),
        )

        self.action_main_dialog.triggered.connect(lambda: self.main_dlg.show())

        self.iface.addToolBarIcon(self.action_main_dialog)

        self.actions.append(self.action_main_dialog)

        # -- Menu
        self.iface.addPluginToMenu(__title__, self.action_settings)
        self.iface.addPluginToMenu(__title__, self.action_help)

        # -- Help menu

        # documentation
        self.iface.pluginHelpMenu().addSeparator()
        self.action_help_plugin_menu_documentation = QAction(
            QIcon(str(__icon_path__)),
            f"{__title__} - Documentation",
            self.iface.mainWindow(),
        )
        self.action_help_plugin_menu_documentation.triggered.connect(
            partial(QDesktopServices.openUrl, QUrl(__uri_homepage__))
        )

        self.iface.pluginHelpMenu().addAction(
            self.action_help_plugin_menu_documentation
        )

    def tr(self, message: str) -> str:
        """Get the translation for a string using Qt translation API.

        :param message: string to be translated.
        :type message: str

        :returns: Translated version of message.
        :rtype: str
        """
        return QCoreApplication.translate(self.__class__.__name__, message)

    def unload(self):
        """Cleans up when plugin is disabled/uninstalled."""
        # -- Clean up menu
        self.iface.removePluginMenu(__title__, self.action_help)
        self.iface.removePluginMenu(__title__, self.action_settings)

        # -- Clean up preferences panel in QGIS settings
        self.iface.unregisterOptionsWidgetFactory(self.options_factory)

        # remove from QGIS help/extensions menu
        if self.action_help_plugin_menu_documentation:
            self.iface.pluginHelpMenu().removeAction(
                self.action_help_plugin_menu_documentation
            )

        # remove actions
        del self.action_settings
        del self.action_help

        for action in self.actions:
            self.iface.removeToolBarIcon(action)
            self.iface.removePluginMenu(__title__, action)

    def generate_slot(self):

        plugin_name = get_line_edit_content(
            self.main_dlg.pluginNameLineEdit, "MyPlugin"
        )

        plugin_folder_name = to_snake_case(plugin_name)

        context = {  # to be configure by user
            "plugin_name": plugin_name,
            "plugin_folder_name": plugin_folder_name,
            "qgis_minimum_version": "3.22",
            "plugin_description": "Bla bla bla",
            "about": "Bla bla about",
            "plugin_version": "1.0.0",
            "author": get_line_edit_content(
                self.main_dlg.authorLineEdit, "Author Name"
            ),
            "author_email": get_line_edit_content(self.main_dlg.emailLineEdit, "Email"),
        }

        generate(context)
