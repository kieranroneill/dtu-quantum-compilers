def read_file(path: str) -> str:
    """
    Reads a file at the given path and returns its contents as a string.

    Parameters
    ----------
    path : str
        The path to the file.

    Returns
    -------
    result : str
        The contents of the file as a string.
    """

    with open(path, "r") as f:
        return f.read()
