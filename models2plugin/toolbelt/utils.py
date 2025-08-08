import re

from qgis.PyQt.QtWidgets import QLineEdit


def get_line_edit_content(line_edit: QLineEdit, default_value: str = "") -> str:
    """Retrieve the content of a QLineEdit, returning a default value if empty.

    Args:
        line_edit (QLineEdit): The QLineEdit widget to retrieve content from.
        default_value (str): The value to return if the QLineEdit is empty.

    Returns:
        str: The content of the QLineEdit or the default value if empty.
    """
    content = line_edit.text().strip()
    return content if content else default_value


def to_snake_case(name) -> str:
    """Convert a string to snake_case.

    Args:
        name (str): The string to convert.
    Returns:
        str: The converted string in snake_case.
    """
    # Add underscores before uppercase letters, except the first letter
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    # Replace spaces
    name = re.sub("[\s-]+", "_", name)
    # Then lowercase the entire string
    return name.lower()
