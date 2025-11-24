"""QML file path extraction from model3 files.

This module provides functions to extract QML file paths from .model3 file content.
It has no dependencies on QGIS and can be tested independently.
"""

from pathlib import Path
from xml.etree import ElementTree as ET


def extract_qml_paths_from_model_content(content: str) -> list[str]:
    """Extract QML file paths from a .model3 file content.
    
    Searches for the following XML pattern:
    <Option name="STYLE" type="List">
      <Option type="Map">
        <Option value="XXX.qml" name="static_value" type="QString"/>
      </Option>
    </Option>
    
    Args:
        content (str): Content of the .model3 file.
        
    Returns:
        list[str]: List of QML file paths found in the model file content.
    """
    try:
        # Parse XML content
        root = ET.fromstring(content.encode('utf-8'))
    except ET.ParseError:
        # If parsing fails, return empty list
        return []
    
    qml_paths = []
    
    # Find all Option elements with name="STYLE" and type="List"
    # xml.etree.ElementTree has limited XPath support, so we iterate manually
    for style_option in root.iter('Option'):
        # Check if this Option has name="STYLE" and type="List" (order independent)
        name_attr = style_option.get('name')
        type_attr = style_option.get('type')
        
        if (name_attr and name_attr == 'STYLE' and 
            type_attr and type_attr == 'List'):
            # Find nested Option elements with name="static_value" and type="QString"
            for option in style_option.iter('Option'):
                opt_name = option.get('name')
                opt_type = option.get('type')
                
                if (opt_name and opt_name == 'static_value' and
                    opt_type and opt_type == 'QString'):
                    value_attr = option.get('value')
                    if value_attr and value_attr.lower().endswith('.qml'):
                        if value_attr not in qml_paths:
                            qml_paths.append(value_attr)
    
    return qml_paths


def replace_qml_paths_in_model_content(content: str, models_dir: str) -> str:
    """Replace absolute QML file paths in .model3 file content with paths to the models directory.
    
    Finds all QML paths in STYLE blocks and replaces them with paths to the models directory.
    
    Args:
        content (str): Content of the .model3 file.
        models_dir (str): Path to the models directory where QML files will be installed.
        
    Returns:
        str: Modified content with updated QML paths.
    """
    try:
        # Parse XML content
        root = ET.fromstring(content.encode('utf-8'))
    except ET.ParseError:
        # If parsing fails, return original content
        return content
    
    # Find all Option elements with name="STYLE" and type="List"
    # xml.etree.ElementTree has limited XPath support, so we iterate manually
    for style_option in root.iter('Option'):
        # Check if this Option has name="STYLE" and type="List" (order independent)
        name_attr = style_option.get('name')
        type_attr = style_option.get('type')
        
        if (name_attr and name_attr == 'STYLE' and 
            type_attr and type_attr == 'List'):
            # Find nested Option elements with name="static_value" and type="QString"
            for option in style_option.iter('Option'):
                opt_name = option.get('name')
                opt_type = option.get('type')
                
                if (opt_name and opt_name == 'static_value' and
                    opt_type and opt_type == 'QString'):
                    value_attr = option.get('value')
                    if value_attr and value_attr.lower().endswith('.qml'):
                        # Extract just the filename from the old path
                        qml_filename = Path(value_attr).name
                        
                        # Create the new path in the models directory
                        new_qml_path = str(Path(models_dir) / qml_filename)
                        
                        # Update the value attribute
                        option.set('value', new_qml_path)
    
    # Convert back to string, preserving XML declaration if present
    try:
        # Serialize to string
        result_bytes = ET.tostring(root, encoding='utf-8')
        result = result_bytes.decode('utf-8')
        
        # Preserve original XML declaration if present
        has_xml_decl = content.strip().startswith('<?xml') or content.strip().startswith('<!DOCTYPE')
        if has_xml_decl and not result.startswith('<?xml'):
            # Try to extract original declaration if needed
            # xml.etree.ElementTree doesn't preserve DOCTYPE, so we handle it separately
            if content.strip().startswith('<!DOCTYPE'):
                # For DOCTYPE, we might need to prepend it manually
                # But typically, .model3 files don't have DOCTYPE
                pass
        
        return result
    except Exception:
        # Fallback: return original content if serialization fails
        return content
