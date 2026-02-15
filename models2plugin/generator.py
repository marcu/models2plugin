import mimetypes
import os
import re
import shutil
from pathlib import Path

from qgis.core import Qgis, QgsApplication

from models2plugin.__about__ import DIR_PLUGIN_ROOT
from models2plugin.toolbelt import PlgLogger

plugin_template_dir = Path(
    DIR_PLUGIN_ROOT, "template/plugin"
)  # Directory containing the plugin template files


logger = PlgLogger()


# Render the template by replacing variables in the content
def render_template(contenu, variables):
    """Function that replaces variables in the template content with their values.

    Args:
        contenu (str): The content of the template.
        variables (dict): A dictionary containing variable names as keys and their values.
    Returns:
        str: The content with variables replaced by their values.
    """
    for cle, valeur in variables.items():
        contenu = re.sub(r"{{\s*" + re.escape(cle) + r"\s*}}", valeur, contenu)
    return contenu


def generate(plugin_output_dir, context, models_to_include: list[str] = []):

    plugin_output_dir: Path = Path(plugin_output_dir)
    plugin_output_dir.mkdir(parents=True, exist_ok=True)

    """Generate a QGIS plugin from a template by replacing variables in the template files."""
    # Walking through the source template dir
    for root, _, files in os.walk(plugin_template_dir):
        for file_name in files:
            absolute_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(absolute_path, plugin_template_dir)
            destination_file = os.path.join(plugin_output_dir, relative_path)

            # Ensure the destination directory exists
            os.makedirs(os.path.dirname(destination_file), exist_ok=True)

            mime_type, _ = mimetypes.guess_type(absolute_path)
            # Check if the file is an image
            if mime_type and mime_type.startswith("image/"):
                # In that case, we just copy the file
                shutil.copyfile(absolute_path, destination_file)
            else:
                # Otherwise, we assume it's a text file and generate the content using the template
                with open(absolute_path, "r", encoding="utf-8") as f:
                    content = f.read()
                rendered_content = render_template(content, context)

                # Write the rendered content to the destination file
                with open(destination_file, "w", encoding="utf-8") as f:
                    f.write(rendered_content)

    plutin_output_models_dir = plugin_output_dir / "models"
    os.makedirs(plutin_output_models_dir, exist_ok=True)

    for model_to_include in models_to_include:
        logger.log(
            f"Processing model: {model_to_include}", log_level=Qgis.MessageLevel.Info
        )

        models_dir = os.path.join(
            QgsApplication.qgisSettingsDirPath(), "processing", "models"
        )

        model_path = Path(models_dir, model_to_include)

        if model_path.exists():
            # Copy the model file to the plugin output directory
            shutil.copy(model_path, plutin_output_models_dir / model_path.name)
        else:
            logger.log(
                f"Model file {model_to_include} does not exist and will not be copied.",
                log_level=Qgis.MessageLevel.Critical,
            )
