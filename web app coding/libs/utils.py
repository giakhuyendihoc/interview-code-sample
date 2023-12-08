def strip_strings_recursively(data):
    """
    Strip all strings in the given data.
    """

    if isinstance(data, str):
        return data.strip()

    if isinstance(data, list):
        return [strip_strings_recursively(item) for item in data]

    if isinstance(data, dict):
        return {k: strip_strings_recursively(v) for k, v in data.items()}

    return data
