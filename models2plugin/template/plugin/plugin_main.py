from pathlib import Path

from qgis.core import QgsApplication, QgsMessageLog, Qgis
from qgis.gui import QgisInterface

from .provider import Provider
from .qml_parser import replace_qml_paths_in_model_content

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
        # Execute installation script: update QML paths in model files
        # This runs when the plugin is loaded for the first time or after installation
        self._run_installation_script()

    def _run_installation_script(self):
        """Run installation script to update QML paths in model files.
        
        This method executes once when the plugin is loaded and ensures that
        QML paths in .model3 files point to the plugin's models directory.
        This is necessary because the plugin installation path is unknown at generation time.
        
        The script:
        1. Reads all .model3 files in the plugin's models directory
        2. Extracts QML file paths from STYLE blocks
        3. Replaces them with paths pointing to the plugin's models directory
        4. Saves the updated files
        
        This runs every time the plugin is loaded, but only updates files if needed.
        """
        models_dir = DIR_PLUGIN_ROOT / "models"
        
        if not models_dir.exists():
            QgsMessageLog.logMessage(
                f"Models directory not found: {models_dir}",
                level=Qgis.MessageLevel.Info,
                tag="{{plugin_name}}"
            )
            return
        
        QgsMessageLog.logMessage(
            f"Running installation script: updating QML paths in {models_dir}",
            level=Qgis.MessageLevel.Info,
            tag="{{plugin_name}}"
        )
        
        # Process all .model3 files in the models directory
        updated_count = 0
        for model_path in models_dir.glob("*.model3"):
            try:
                # Read the model file content
                with open(model_path, "r", encoding="utf-8") as f:
                    model_content = f.read()
                
                # Replace QML paths with paths to the plugin's models directory
                modified_content = replace_qml_paths_in_model_content(
                    model_content, str(models_dir)
                )
                
                # Only write if content changed (avoid unnecessary file writes)
                if modified_content != model_content:
                    # Write the modified content back to the file
                    with open(model_path, "w", encoding="utf-8") as f:
                        f.write(modified_content)
                    updated_count += 1
                    QgsMessageLog.logMessage(
                        f"Updated QML paths in {model_path.name}",
                        level=Qgis.MessageLevel.Info,
                        tag="{{plugin_name}}"
                    )
                    
            except Exception as e:
                QgsMessageLog.logMessage(
                    f"Error updating QML paths in {model_path.name}: {e}",
                    level=Qgis.MessageLevel.Warning,
                    tag="{{plugin_name}}"
                )
        
        if updated_count > 0:
            QgsMessageLog.logMessage(
                f"Installation script completed: updated {updated_count} model file(s)",
                level=Qgis.MessageLevel.Info,
                tag="{{plugin_name}}"
            )

    def initGui(self):
        self.provider = Provider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)
