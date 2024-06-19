"""Remove installed collections"""

import shutil
from icm.commons import commons


def main(name: str) -> None:
    """ENTRY POINT: Remove collections
    * name: Name of the collection to remove
    """

    # -- Get context information
    # ctx = commons.Context()
    folders = commons.Folders()
    print()

    # -- Build the Path to the collection
    abs_collection = folders.collections / name

    # -- Check if the collection exists, as it was type byte the user
    if not abs_collection.exists():
        print(f"rm: cannot remove {name}: No such collection")
        return

    # -- Remove the collection folder, along with all its files
    shutil.rmtree(abs_collection)
