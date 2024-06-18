"""Install command"""

import zipfile
import os
import sys
import re
from pathlib import Path

import requests
import click
from tqdm import tqdm
from icm.commons import commons


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

    def __init__(self, folders: commons.Folders) -> None:
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


def main(coltag: str, dev: bool) -> None:
    """ENTRY POINT: Install collections
    * coltag: Nombre de la coleccion + tag opcional
      Ex. iceK, iceK@0.1.4
    * dev: Install development version
    """

    # -- Get context information
    folders = commons.Folders()
    collection = Collection(folders)

    print()

    # -- Install the collection!
    install_main(collection, coltag, dev)

    # -- Test
    # -- TODO: Move it to a test python file
    # install_main(collection, "iceK@0.1.4", True)
    # install_main(collection, "iceK", True)
    # install_main(collection, "iceK@0.1.3")
    # install_main(collection, "iceK")
    # install_main(collection, "iceWires")
    # install_main(collection, "iceIO")
    # install_main(collection, "iceGates")
    # install_main(collection, "iceMux")
    # install_main(collection, "iceCoders")
    # install_main(collection, "iceFF")
    # install_main(collection, "iceRegs")
    # install_main(collection, "iceSRegs")


def install_main(
    collection: Collection, coltag: str, dev: bool = False
) -> None:
    """Main function for installing collections
    * collection: Collection class (context)
    * coltag: name + version tag (Ex. iceK@0.1.4)
    * dev: Development flag
      * True: Install latest version from the repo
      * False: Install a stable version

    Main use cases:
      1. If dev flag active: highest priority. Install dev collection
         (the version is ignored, if given)
      2. "name@version" is given --> Install the given version of collection
      3. "name" is given --> Install the latest stable version
    """

    # -- Parse the collection + tag
    coltag = collection.parse_coltag(coltag)

    if not coltag:
        print("---> coleccion incorrecta!")
        sys.exit(1)

    # -- Get the collection name and version:
    name, version = (coltag["name"], coltag["version"])

    # -- Analyze all the cases
    # -- The --dev flag has the highest priority. If it is set,
    # -- it does not matter which version was specified (if any)
    if dev:

        # -- Conflict! Both version and --dev are specified
        # -- --dev has the highest priority. Warn the user
        if version:
            click.secho(
                f"Warning! Installing dev version instead of {version}",
                fg="red",
            )

        # -- Case 1: Install development version
        install(collection, name)
        return

    # -- Case 2: collection name + version given
    if version:
        install(collection, name, version)
        return

    # -- Case 3: Only collection name given

    # Calculate the url for the collection package.json file
    url = collection.package_url(name)

    # -- Download the package.json
    package = collection.download_package(url)

    # -- Get the latest version
    if package:
        version = package["version"]

        # --  Install the collection!
        install(collection, name, version)
    else:
        click.secho(f"Collection: {name}", fg="red")
        click.secho("No package.json downloaded", fg="red")
        click.secho(f"URL: {url}", fg="red")


def install(collection: Collection, name: str, version="") -> None:
    """Install the given collection by name + version
    * collection: Collection class (Context)
    * Name: Collection name (ex. 'iceK')
    * Version: (Optional) (ex. '0.1.4')
    The collection is downloaded and unziped in the icestudio
      collection folder
    """

    # -- Get the name+tag
    nametag = collection.nametag(name, version)
    click.secho(f"Installing collection {nametag}", fg="yellow")

    abs_filename = collection.abs_filename(version)
    url = collection.url(name, version)

    # -- DEBUG!
    # print(f"* File: {abs_filename}")
    # print(f"* Url: {url}")

    # -- Download the collection
    collection.download(url, abs_filename)

    # -- Uncompress the collection
    collection.uncompress(abs_filename)

    # -- Remove the .zip file
    os.remove(abs_filename)

    click.secho("Done!", fg="green")
