"""List installed collections command"""

from icm.commons import commons


def main():
    """ENTRY POINT: List collections"""

    print()
    print("--> LS!!!!!")
    print()

    # -- Get context information
    folders = commons.Folders()

    # -- Get a list with all the collections (folders)
    list_col = [
        file.name for file in folders.collections.glob("*") if file.is_dir()
    ]

    # -- Sort the list of collections
    list_col.sort()

    # -- Print all the available collections
    for colection in list_col:
        print(f"* {colection}")
