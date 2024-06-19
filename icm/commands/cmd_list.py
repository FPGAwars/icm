"""List available collections"""

import click
from icm.commons import commons


# -- AVAILABLE collections
COLLECTION_STORE = {
    "stable": [
        "iceK",
        "iceWires",
        "iceIO",
        "iceGates",
        "iceMux",
        "iceCoders",
        "iceFF",
        "iceRegs",
        "iceSRegs",
    ],
    "dev": [
        "iceBoards",
        "iceComp",
        "iceArith",
        "iceCounters",
        "iceSignals",
        "icePLL",
        "iceLEDOscope",
        "iceLEDs",
        "iceHearts",
        "iceInputs",
        "iceRok",
        "iceMachines",
        "iceSerial",
        "iceMem",
        "iceMeassure",
        "iceStack",
        "iceFlash",
        "iceBus",
        "iceLCD",
        "iceSynth",
        "icecrystal",
        "icebreaker",
        "Collection-stdio",
        "LOVE-FPGA-Collection",
        "Collection-Jedi",
        "CT11-collection",
        "collection-generic",
        "collection-logic",
        "ice-chips-verilog",
        "Icestudio-ArithmeticBlocks",
    ],
}


def list_collections(
    collection: commons.Collection, typec: str, fg="white"
) -> None:
    """List all the collections of a given type
    * collection: Context information
    * typec: Type of collections
      'stable': Estable collections
      'dev'   : Development collections
    """

    click.secho(f"{'Name':<15}   {'Version':<8}  Description", fg=fg)
    click.secho(f"{'─'*15:<15}   {'─'*8:<8}  {'─'*20}", fg=fg)
    for name in COLLECTION_STORE[typec]:

        # Calculate the url for the collection package.json file
        url = collection.package_url(name)

        # -- Download the package.json
        package = collection.download_package(url)

        # -- Get the collection information
        if package:
            version = package["version"]
            desc = package["description"]

            click.secho(f"• {name:<15} {version:<8}  {desc}", fg=fg)

        # -- There was an error
        else:
            click.secho(f"• {name:<15} {'xxx':<8}  {'xxx'}", fg="red")


def main():
    """ENTRY POINT: List available collections"""

    # -- Get context information
    ctx = commons.Context()
    folders = commons.Folders()
    collection = commons.Collection(folders)

    print()

    # -- Header
    click.secho(ctx.line, fg="yellow")
    click.secho("AVAILABLE COLLECTIONS", fg="yellow")
    click.secho(ctx.line, fg="yellow")

    print()
    click.secho("─" * 50, fg="green")
    click.secho("STABLE", fg="green")
    click.secho("─" * 50, fg="green")
    list_collections(collection, "stable", fg="green")

    print()
    click.secho("─" * 50, fg="blue")
    click.secho("DEV", fg="blue")
    click.secho("─" * 50, fg="blue")
    list_collections(collection, "dev", fg="blue")
