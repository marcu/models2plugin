import mimetypes
import os
import re
import shutil
from pathlib import Path

from models2plugin.__about__ import DIR_PLUGIN_ROOT

# Chemins
plugin_template_dir = Path(
    DIR_PLUGIN_ROOT, "template/plugin"
)  # Directory containing the plugin template files
plugin_output_dir = Path(
    DIR_PLUGIN_ROOT, "output/blabla"
)  # Directory where the generated plugin will be saved


contexte = {  # to be configure by user
    "plugin_name": "TestPlugin",
    "qgis_minimum_version": "3.22",
    "plugin_description": "Bla bla bla",
    "about": "Bla bla about",
    "plugin_version": "1.0.0",
    "author": "ICI Moi",
    "author_email": "Email",
}


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


def generate():
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
                    contenu = f.read()
                rendu = render_template(contenu, contexte)

                # Write the rendered content to the destination file
                with open(destination_file, "w", encoding="utf-8") as f:
                    f.write(rendu)
