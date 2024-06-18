"""Icestudio Collection Manager"""

# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import click

from icm.commands import (
    cmd_create,
    cmd_validate,
    cmd_update,
    cmd_info,
    cmd_install,
)


@click.group()
@click.version_option()
def cli():
    """Icestudio collections manager"""


@cli.command()
def create():
    """Create a collection structure."""
    cmd_create.create()


@cli.command()
def update():
    """Update docs and translation."""
    cmd_update.update()


@cli.command()
def validate():
    """Validate a collection."""
    cmd_validate.validate()


@cli.command()
def info():
    """Show system information"""
    cmd_info.main()


@cli.command()
@click.argument("coltag", nargs=1)
@click.option(
    "-d", "--dev", is_flag=True, help="Install latest development version"
)
def install(coltag, dev):
    """Install collections"""

    cmd_install.main(coltag, dev)
