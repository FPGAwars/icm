"""Data structures common to all the modules"""

from typing import NamedTuple
import shutil
from pathlib import Path


# -- Context information
class Context(NamedTuple):
    """general Context information"""

    @property
    def terminal_width(self) -> int:
        """Get the terminal with in columns"""
        return shutil.get_terminal_size().columns

    @property
    def line(self) -> str:
        """Return a line as long as the terminal width"""
        return "─" * self.terminal_width


# -- Folder information
class Folders(NamedTuple):
    """Icestudio related folders"""

    @property
    def home(self) -> Path:
        """Return the home user folder"""
        return Path.home()

    @property
    def icestudio(self) -> Path:
        """Return the icestudio data folder"""
        return self.home / ".icestudio"

    @property
    def collections(self) -> Path:
        """Return the icestudio collections folder"""
        return self.icestudio / "collections"

    @staticmethod
    def check(folder: Path) -> str:
        """Return a check character depending if the folder exists
        ✅ : Folder exists
        ❌ : Folder does NOT exist
        """
        return "✅ " if folder.exists() else "❌ "
