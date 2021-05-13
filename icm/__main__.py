"""Icestudio Collection Manager"""
# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import click

from icm.commands import cmd_create, cmd_validate, cmd_update


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
