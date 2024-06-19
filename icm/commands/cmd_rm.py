"""Remove installed collections"""

import shutil
from icm.commons import commons

import click


def main(coltag: str) -> None:
    """ENTRY POINT: Remove collections
    * coltag: Name+version of the collection to remove
      (Ex. iceK-0.1.4)
    """

    # -- Get context information
    # ctx = commons.Context()
    folders = commons.Folders()
    collection = commons.Collection(folders)
    print()

    # -- Build the Path to the collection
    abs_collection = folders.collections / coltag

    # -- Check if the collection exists, as it was typed bye the user
    if abs_collection.exists():
        # -- Remove it!
        shutil.rmtree(abs_collection)
        return

    # -- Manage other cases
    # -- Case 1: Remove the first collection that has the same name
    # --    Ignore the version

    # -- Parse the collection name: Get the name and version
    parsed_coltag = collection.parse_coltag2(coltag)
    name = parsed_coltag['name']
    version = parsed_coltag['version']

    # -- If there is name and version: The collection does not exists
    if name and version:
        print(f"rm: cannot remove {coltag}: No such collection")
        return

    # -- List all the collections that starts with "name-"
    list_col = [
        file.name for file in folders.collections.glob(f"{name}-*") if file.is_dir()
    ]

    # -- No collection has a name that starts with "<name>-"
    if not list_col:
        print(f"rm: cannot remove {coltag}: No such collection")
        return

    # -- There are collection with that name
    # -- TODO: Remove ALL the collections, not just the first

    # -- Get the first collection name
    coltag = list_col[0]

    # -- Build the full path to the collection
    abs_collection = folders.collections / coltag

    # -- Ask for confirmation!
    if click.confirm(f"{coltag}: Remove?"):
        # -- Remove the collection!
        shutil.rmtree(abs_collection)
        return

    print("Aborted.")
