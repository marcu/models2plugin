"""Processing algorithm for plugin initialization.

This module provides a Processing algorithm to manually initialize the plugin
by updating QML paths in model files.
"""

from pathlib import Path

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterBoolean,
    QgsProcessingOutputString,
    QgsMessageLog,
    Qgis,
)
from qgis.PyQt.QtCore import QCoreApplication

from .qml_parser import replace_qml_paths_in_model_content

DIR_PLUGIN_ROOT: Path = Path(__file__).parent


class InitializePluginAlgorithm(QgsProcessingAlgorithm):
    """Algorithm to initialize the plugin by updating QML paths in model files."""

    OUTPUT = "OUTPUT"

    def tr(self, string):
        """Translate string."""
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        """Return a new instance of the algorithm."""
        return InitializePluginAlgorithm()

    def name(self):
        """Algorithm name."""
        return "initialize_plugin"

    def displayName(self):
        """Algorithm display name."""
        return self.tr("Initialisation du plugin")

    def group(self):
        """Algorithm group."""
        return self.tr("{{plugin_name}}")

    def groupId(self):
        """Algorithm group ID."""
        return "{{plugin_provider_id}}"

    def shortHelpString(self):
        """Return help string."""
        return self.tr(
            "Cet algorithme met à jour les chemins des fichiers QML dans les fichiers de modèle (.model3).\n\n"
            "Il doit être exécuté après l'installation du plugin pour s'assurer que les chemins QML "
            "pointent vers le dossier models du plugin installé.\n\n"
            "Vous pouvez également l'exécuter manuellement si les chemins QML doivent être mis à jour."
        )

    def initAlgorithm(self, config=None):
        """Define inputs and outputs."""
        self.addParameter(
            QgsProcessingParameterBoolean(
                "FORCE_UPDATE",
                self.tr("Forcer la mise à jour (même si les fichiers sont déjà à jour)"),
                defaultValue=False,
            )
        )
        self.addOutput(QgsProcessingOutputString(self.OUTPUT, self.tr("Résultat")))

    def processAlgorithm(self, parameters, context, feedback):
        """Process the algorithm."""
        models_dir = DIR_PLUGIN_ROOT / "models"
        
        if not models_dir.exists():
            result_message = f"Le dossier models n'existe pas : {models_dir}"
            QgsMessageLog.logMessage(
                result_message,
                level=Qgis.MessageLevel.Warning,
                tag="{{plugin_name}}"
            )
            return {self.OUTPUT: result_message}
        
        force_update = self.parameterAsBool(parameters, "FORCE_UPDATE", context)
        
        feedback.pushInfo(f"Mise à jour des chemins QML dans {models_dir}")
        feedback.setProgress(0)
        
        # Process all .model3 files in the models directory
        model_files = list(models_dir.glob("*.model3"))
        total_files = len(model_files)
        
        if total_files == 0:
            result_message = "Aucun fichier .model3 trouvé dans le dossier models"
            QgsMessageLog.logMessage(
                result_message,
                level=Qgis.MessageLevel.Info,
                tag="{{plugin_name}}"
            )
            return {self.OUTPUT: result_message}
        
        updated_count = 0
        for idx, model_path in enumerate(model_files):
            if feedback.isCanceled():
                break
            
            try:
                feedback.pushInfo(f"Traitement de {model_path.name}...")
                
                # Read the model file content
                with open(model_path, "r", encoding="utf-8") as f:
                    model_content = f.read()
                
                # Replace QML paths with paths to the plugin's models directory
                modified_content = replace_qml_paths_in_model_content(
                    model_content, str(models_dir)
                )
                
                # Only write if content changed or if force update is requested
                if modified_content != model_content or force_update:
                    # Write the modified content back to the file
                    with open(model_path, "w", encoding="utf-8") as f:
                        f.write(modified_content)
                    updated_count += 1
                    feedback.pushInfo(f"  ✓ Chemins QML mis à jour dans {model_path.name}")
                else:
                    feedback.pushInfo(f"  - {model_path.name} est déjà à jour")
                    
            except Exception as e:
                error_message = f"Erreur lors de la mise à jour de {model_path.name}: {e}"
                feedback.reportError(error_message)
                QgsMessageLog.logMessage(
                    error_message,
                    level=Qgis.MessageLevel.Warning,
                    tag="{{plugin_name}}"
                )
            
            feedback.setProgress(int((idx + 1) / total_files * 100))
        
        if updated_count > 0:
            result_message = f"Initialisation terminée : {updated_count} fichier(s) de modèle mis à jour"
        else:
            result_message = "Initialisation terminée : tous les fichiers sont déjà à jour"
        
        QgsMessageLog.logMessage(
            result_message,
            level=Qgis.MessageLevel.Info,
            tag="{{plugin_name}}"
        )
        
        return {self.OUTPUT: result_message}

