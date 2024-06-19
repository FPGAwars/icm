"""List installed collections command"""

import click
from icm.commons import commons


def main():
    """ENTRY POINT: List collections"""

    # -- Get context information
    ctx = commons.Context()
    folders = commons.Folders()

    # -- Header
    print()
    click.secho(ctx.line, fg="blue")
    click.secho("INSTALLED COLLECTIONS", fg="blue")
    click.secho(ctx.line, fg="blue")

    # -- Get a list with all the collections (folders)
    list_col = [
        file.name for file in folders.collections.glob("*") if file.is_dir()
    ]

    # -- Sort the list of collections
    list_col.sort()

    # -- List not empty: Print it!
    if list_col:
        # -- Print all the available collections
        for colection in list_col:
            click.secho(f"• {colection}", fg="blue")

    else:
        print("No installed collections")
