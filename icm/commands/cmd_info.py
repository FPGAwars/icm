"""info command"""

# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017-19 FPGAwars
# --   Author Jesús Arroyo
# -- (C) 2020-24 FPGAwars
# --   Author Juan Gonzalez (Obijuan)
# -- Licence GPLv2

import platform
import shutil
from pathlib import Path

import click


# -- Terminal width
TERMINAL_WIDTH = shutil.get_terminal_size().columns

# -- Horizontal line
HLINE = "─" * TERMINAL_WIDTH

# -- Home user folder
HOME = Path.home()

# -- Icestudio HOME dir
ICESTUDIO_HOME = HOME / ".icestudio"

# -- Icestudio root for collections
COLLECTIONS = ICESTUDIO_HOME / "collections"


def main():
    """ENTRY POINT: Show system information"""

    # --------------------------------
    # -- Print System information
    # --------------------------------
    # -- Header
    print()
    click.secho(HLINE, fg="green")
    click.secho("SYSTEM INFORMATION", fg="green")
    click.secho(HLINE, fg="green")

    # -- Read system information
    plat = platform.uname()

    # -- Print it!
    click.echo(click.style("• Processor: ", fg="green") + f"{plat.processor}")
    click.echo(click.style("• System: ", fg="green") + f"{plat.system}")
    click.echo(click.style("• Release: ", fg="green") + f"{plat.release}")
    click.echo(click.style("• Version: ", fg="green") + f"{plat.version}")

    # ----------------------------
    # -- System folders
    # ----------------------------
    # -- Header
    print()
    click.secho(HLINE, fg="yellow")
    click.secho("FOLDERS", fg="yellow")
    click.secho(HLINE, fg="yellow")

    # -- Check if all the folders exist or not
    ok_home = HOME.exists()
    ok_icestudio = ICESTUDIO_HOME.exists()
    ok_collections = COLLECTIONS.exists()

    # -- Choose the correct bullet for the folder
    home_check = "✅ " if ok_home else "❌ "
    icestudio_check = "✅ " if ok_icestudio else "❌ "
    collections_check = "✅ " if ok_collections else "❌ "

    # -- Print the information
    click.echo(home_check + click.style("HOME: ", fg="yellow") + f"{HOME}")
    click.echo(
        icestudio_check
        + click.style("Icestudio: ", fg="yellow")
        + f"{ICESTUDIO_HOME}"
    )
    click.echo(
        collections_check
        + click.style("Collections: ", fg="yellow")
        + f"{COLLECTIONS}"
    )

    print()
