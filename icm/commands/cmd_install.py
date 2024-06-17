"""Install command"""

import zipfile
import os
import sys
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


def main():
    """ENTRY POINT: Install collections"""

    # -- Get context information
    folders = commons.Folders()
    collection = Collection(folders)

    # -- Install the collection iceK-0.1.4
    install(collection, "iceK", "0.1.4")
    install(collection, "iceK")
    install(collection, "iceK", "0.1.3")
    install(collection, "iceWires")
    install(collection, "iceIO")
    install(collection, "iceGates", "0.3.1")
    install(collection, "iceMux")
    install(collection, "iceCoders")
    install(collection, "iceFF")
    install(collection, "iceRegs")
    install(collection, "iceSRegs")


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
    print()
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
