"""Data structures common to all the modules"""

import re
import sys
import zipfile
import shutil
from typing import NamedTuple
from pathlib import Path

import requests
import click
from tqdm import tqdm


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


class Collection:
    """Manage collections"""

    #   Oficial icestudio Collection are zip files downloaded
    #   from https://github.com/FPGAwars/

    #   There are two types or URL:

    #   * Dev URL:  Latest version in the main branch
    #     https://github.com/FPGAwars/iceK/archive/refs/heads/main.zip

    #   * Version URL:  Specific stable version
    #     https://github.com/FPGAwars/iceK/archive/refs/tags/v0.1.4.zip

    GITHUB_FPGAWARS = "https://github.com/FPGAwars/"
    GITHUB_PREFIX = "/archive/refs/"
    GITHUB_TYPE_DEV = "heads/"
    GITHUB_TYPE_VER = "tags/"
    PACKAGEJSON = "/raw/main/package.json"

    def __init__(self, folders: Folders) -> None:
        self.folders = folders

    def filename(self, version="") -> str:
        """Return the coleccion filename, according to its version
         No Path. No url. Just the .zip filename

        * No version given --> assume dev collection. filename = "main.zip"
        * version given --> filename = "v{version}.zip"

        Ex. col.filename("0.1.4) --> "v0.1.4.zip"
        """

        # -- Filename for the dev collection
        name_dev = "main.zip"

        # -- Filename for the version (stable) collection
        name_ver = f"v{version}.zip"

        # -- Return the name according to the version type
        return name_ver if version else name_dev

    def abs_filename(self, version="") -> Path:
        """Return the absolute path of the collection target filename
        ex: /home/obijuan/.icestudio/collections/v0.1.4.zip
        """
        abs_file = self.folders.collections / self.filename(version)
        return abs_file

    def url(self, name: str, version="") -> str:
        """Return the url of the given collection
        * name: Collection name (Ex. "iceK")
        * version (optional) (Ex. 0.1.4)

        It return the url as a string
        """

        # -- Get the colection filename
        filename = self.filename(version)

        # -- Get the type string
        github_type = self.GITHUB_TYPE_VER if version else self.GITHUB_TYPE_DEV

        # -- Build the url
        url = (
            f"{self.GITHUB_FPGAWARS}{name}{self.GITHUB_PREFIX}"
            f"{github_type}{filename}"
        )

        # -- Return the url
        return url

    def package_url(self, name: str) -> str:
        """Return the url of the package.json file for the given
        collection
          * name: Collection name (Ex. "iceK")
        """
        # -- Example of url for the iceK collection:
        # https://github.com/FPGAwars/iceK/raw/main/package.json

        # -- Construct the URL
        url = f"{self.GITHUB_FPGAWARS}{name}{self.PACKAGEJSON}"

        # -- Return the URL
        return url

    def nametag(self, name: str, version=""):
        """Return the collection name+tag:
        * version Given:
          name+tag = 'name-version' (Ex. iceK-0.1.4)
        * version NOT Given:
          name+tag = 'name-main' (Ex. iceK-main)
        """
        return f"{name}-{version}" if version else f"{name}-main"

    def download(self, url: str, destfile: Path):
        """Download the collection given by its url.
        Store it in the given file
        A download bar is shown
        """

        # -- Generate an http request
        response = requests.get(url, stream=True, timeout=10)

        # -- Check the status. If not ok, exit!
        if response.status_code != 200:
            click.secho(
                f"ERROR when downloading. Code: {response.status_code}",
                fg="red",
            )
            sys.exit(1)

        # Get the file size (from the headers)
        total_size = int(response.headers.get("content-length", 0))

        # -- Open the destination file
        with open(destfile, "wb") as file:

            # Use a progress bar...
            with tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                desc="• Download",
            ) as pbar:

                # Iterate over the blocks
                for chunk in response.iter_content(chunk_size=1024):

                    # -- Make sure the block is not empty
                    if chunk:

                        # Write data!
                        file.write(chunk)

                        # Update pogress bar
                        pbar.update(len(chunk))

    def download_package(self, url: str) -> object:  # Or  None:
        """Download the package.json as an object
        url: package.json url
        Returns: The package.json as an object
          or None if there was an error
        """
        # -- Generate an http request
        response = requests.get(url, timeout=10)

        # -- Check the status. If not ok, exit!
        if response.status_code != 200:
            return None

        # -- Return the package object
        package = response.json()
        return package

    # -- Uncompress the collection zip file
    def uncompress(self, zip_file: Path):
        """Uncompress the given zip file. The destination folder is
        the icestudio collection folder
        """

        # -- Open the zip file and extract it with progress bar
        with zipfile.ZipFile(zip_file, "r") as zip_ref:

            # Get the file list in the zip file
            file_list = zip_ref.namelist()

            # Use a progress bar
            with tqdm(
                total=len(file_list), desc="• Unzip", unit="file"
            ) as pbar:

                # -- Iterate over each file in the zip
                for file in file_list:

                    # Extract the file!
                    zip_ref.extract(file, self.folders.collections)

                    # -- Update progress bar!
                    pbar.update(1)

    def parse_coltag(self, coltag: str) -> dict:  # or | None:
        """Parse a collection name with optional tag version
        Ex: "iceK@0.1.4"
        Return:
          None: There is an error
          result: Dictionary with the calculated values
            result['name']: Collection name
            result['version']: Collection version (it could be "")
        """
        # -- Pattern for parsing strings in the format <name>[@<version>]
        pattern = r"^(?P<name>[a-zA-Z0-9]+)(@(?P<version>\d+\.\d+(\.\d+)?))?$"

        # Busca coincidencias en la cadena de entrada
        match = re.match(pattern, coltag)

        # -- TODO: Raise an exception!
        if match:
            return match.groupdict()

        # -- No match. Incorrect collection tag
        return None

    def parse_coltag2(self, coltag: str) -> dict:  # or | None:
        """Parse a collection name with optional tag version
        Ex: "iceK-0.1.4"
        Return:
          None: There is an error
          result: Dictionary with the calculated values
            result['name']: Collection name
            result['version']: Collection version (it could be "")
        """
        # -- Pattern for parsing strings in the format <name>[@<version>]
        pattern = r"^(?P<name>[a-zA-Z0-9]+)(-(?P<version>\d+\.\d+(\.\d+)?))?$"

        # Busca coincidencias en la cadena de entrada
        match = re.match(pattern, coltag)

        # -- TODO: Raise an exception!
        if match:
            return match.groupdict()

        # -- No match. Incorrect collection tag
        return None
