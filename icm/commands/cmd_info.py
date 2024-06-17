"""info command"""

# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017-19 FPGAwars
# --   Author Jesús Arroyo
# -- (C) 2020-24 FPGAwars
# --   Author Juan Gonzalez (Obijuan)
# -- Licence GPLv2

import platform
import click
from icm.commons import commons


def print_system_info(ctx: commons.Context) -> None:
    """Print System information"""

    # -- Header
    print()
    click.secho(ctx.line, fg="green")
    click.secho("SYSTEM INFORMATION", fg="green")
    click.secho(ctx.line, fg="green")

    # -- Read system information
    plat = platform.uname()

    # -- Print it!
    click.echo(click.style("• Processor: ", fg="green") + f"{plat.processor}")
    click.echo(click.style("• System: ", fg="green") + f"{plat.system}")
    click.echo(click.style("• Release: ", fg="green") + f"{plat.release}")
    click.echo(click.style("• Version: ", fg="green") + f"{plat.version}")


def print_folders_info(ctx: commons.Context, folders: commons.Folders) -> None:
    """Print Sytem folders info"""

    # -- Header
    print()
    click.secho(ctx.line, fg="yellow")
    click.secho("FOLDERS", fg="yellow")
    click.secho(ctx.line, fg="yellow")

    # -- Print the information
    click.echo(
        folders.check(folders.home)
        + click.style("HOME: ", fg="yellow")
        + f"{folders.home}"
    )
    click.echo(
        folders.check(folders.icestudio)
        + click.style("Icestudio: ", fg="yellow")
        + f"{folders.icestudio}"
    )
    click.echo(
        folders.check(folders.collections)
        + click.style("Collections: ", fg="yellow")
        + f"{folders.collections}"
    )

    print()


def main():
    """ENTRY POINT: Show system information"""

    # -- Get context information
    ctx = commons.Context()
    folders = commons.Folders()

    # --------------------------------
    # -- Print System information
    # --------------------------------
    print_system_info(ctx)

    # ----------------------------
    # -- System folders
    # ----------------------------
    print_folders_info(ctx, folders)
