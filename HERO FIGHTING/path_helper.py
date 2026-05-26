"""
Path helper utility for cross-platform asset loading.

On iOS (and other platforms), the Current Working Directory (CWD) may not be
the script directory, causing FileNotFoundError for relative paths.

This module provides resource_path() which resolves any relative path
against the actual script directory, guaranteeing assets are found regardless
of the CWD at launch.

Usage:
    from path_helper import resource_path
    img = pygame.image.load(resource_path('assets/icons/miku.png'))
"""

import os
import sys

# The root directory of the project — where the Python source files live.
# Works on Windows, macOS, iOS, Linux, and when frozen with PyInstaller/Briefcase.
if getattr(sys, 'frozen', False):
    # Running as a bundled app (PyInstaller, Briefcase, etc.)
    _BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as a normal Python script
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def resource_path(relative_path: str) -> str:
    """Convert a relative asset path to an absolute path based on the project root.

    - Normalises path separators (backslash → os.sep) so paths work on
      Windows *and* Unix/iOS.
    - If the path is already absolute it is returned unchanged.

    Args:
        relative_path: A relative path like 'assets/icons/miku.png'
                       or r'assets\\icons\\miku.png'.

    Returns:
        An absolute filesystem path.
    """
    if os.path.isabs(relative_path):
        return relative_path
    # Normalise separators: replace both / and \\ with os.sep
    normalised = relative_path.replace("\\", os.sep).replace("/", os.sep)
    return os.path.join(_BASE_DIR, normalised)
