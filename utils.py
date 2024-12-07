import re


def escape_xml_string(xml_string):
    """
    Escape special characters in XML string.

    Args:
        xml_string (str): Raw XML string

    Returns:
        str: Escaped XML string
    """
    # Common XML escapes
    replacements = {
        "&": "&amp;",
    }

    # Replace special characters with their escaped versions
    for char, escape in replacements.items():
        xml_string = xml_string.replace(char, escape)

    # Remove any invalid XML characters
    xml_string = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", xml_string)
    return xml_string.strip()
