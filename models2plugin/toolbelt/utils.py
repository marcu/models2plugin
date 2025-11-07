import re

from qgis.PyQt.QtWidgets import QLineEdit, QTextEdit, QWidget


def get_text_content(widget: QWidget, default_value: str = "") -> str:
    """Retrieve the content of a QLineEdit or a QTextEdi, returning a default value if empty.

    Args:
        widget (QTextEdit or QWidget): The widget to retrieve content from.
        default_value (str): The value to return if the QLineEdit is empty.

    Returns:
        str: The content of the QLineEdit or the default value if empty.
    """

    content = None

    if isinstance(widget, QLineEdit):
        content = widget.text().strip()
    elif isinstance(widget, QTextEdit):
        content = widget.toPlainText().strip()
    else:
        raise TypeError(
            "Unsupported widget type. Only QLineEdit and QTextEdit are supported."
        )

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
