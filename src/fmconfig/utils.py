import os
import platform


def get_system() -> str:
    """Get the name of the operating system.

    Returns:
        str: The name of the operating system.

    Raises:
        OSError: If the operating system is not supported.
    """
    system = platform.system()
    if system != "Darwin":
        raise OSError("Unsupported operating system")
    return system


def get_graphics_path() -> str:
    """Get the path for the graphics directory based on the operating system.

    Returns:
        str: The path to the graphics directory.

    Raises:
        OSError: If the operating system is not supported.
    """
    system = get_system()
    username = os.getlogin()
    if system == "Darwin":
        return f"/Users/{username}/Library/Application Support/Sports Interactive/Football Manager 2023/graphics"
    raise OSError("Unsupported operating system")
