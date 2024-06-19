"""Install command"""

import os
import sys

import click
from icm.commons import commons


def main(coltag: str, dev: bool) -> None:
    """ENTRY POINT: Install collections
    * coltag: Nombre de la coleccion + tag opcional
      Ex. iceK, iceK@0.1.4
    * dev: Install development version
    """

    # -- Get context information
    folders = commons.Folders()
    collection = commons.Collection(folders)

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
    collection: commons.Collection, coltag: str, dev: bool = False
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


def install(collection: commons.Collection, name: str, version="") -> None:
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
