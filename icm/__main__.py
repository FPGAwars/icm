# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import click

from icm.commands import cmd_create, cmd_validate


@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
def create():
    """Create a collection structure."""
    cmd_create.create()


@cli.command()
def validate():
    """Validate a collection structure."""
    cmd_validate.validate()
