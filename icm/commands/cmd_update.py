# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import click


def update():
    """Update docs and translation."""

    click.secho('Update the collection', fg='cyan')

    getdocs()
    gettext()


def getdocs():
    pass


def gettext():
    pass
