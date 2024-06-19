"""List available collections"""

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


def list_collections(collection: commons.Collection, typec: str) -> None:
    """List all the collections of a given type
    * collection: Context information
    * typec: Type of collections
      'stable': Estable collections
      'dev'   : Development collections
    """

    print(f"{'Name':<15}   {'Version':<8}  Description")
    print(f"{'-'*15:<15}   {'-'*8:<8}  ----------")
    for name in COLLECTION_STORE[typec]:

        # Calculate the url for the collection package.json file
        url = collection.package_url(name)

        # -- Download the package.json
        package = collection.download_package(url)

        # -- Get the collection information
        if package:
            version = package["version"]
            desc = package["description"]

            print(f"* {name:<15} {version:<8}  {desc}")

        # -- There was an error
        else:
            print(f"* {name:<15} {'xxx':<8}  {'xxx'}")


def main():
    """ENTRY POINT: List available collections"""

    # -- Get context information
    # ctx = commons.Context()
    folders = commons.Folders()
    collection = commons.Collection(folders)

    print()

    # -- Header
    print("-----------------------------------------")
    print("AVAILABE COLLECTIONS")
    print("-----------------------------------------")
    print("STABLE  ")
    print("--------------------------")
    print()
    list_collections(collection, "stable")

    print()
    print("--------------------------")
    print("DEV  ")
    print("--------------------------")
    print()
    list_collections(collection, "dev")
