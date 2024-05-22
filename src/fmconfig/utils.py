import os
import platform
import pwd


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


def get_username() -> str:
    """Get the username of the current user.

    Returns:
        str: The username of the current user.
    """
    return os.environ.get("USER") or pwd.getpwuid(os.geteuid()).pw_name


def get_graphics_path() -> str:
    """Get the path for the graphics directory based on the operating system.

    Returns:
        str: The path to the graphics directory.

    Raises:
        OSError: If the operating system is not supported.
    """
    system = get_system()
    username = get_username()
    if system == "Darwin":
        return f"/Users/{username}/Library/Application Support/Sports Interactive/Football Manager 2023/graphics"
    raise OSError("Unsupported operating system")
