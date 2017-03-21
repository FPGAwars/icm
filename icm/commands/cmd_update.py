# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import os
import click

from icm.commands.cmd_validate import validate_collection


def update():
    """Update docs and translation."""

    click.secho('Update the collection', fg='cyan')

    if validate_collection():

        # Update README.md
        newdata = getdocs()
        if os.path.exists('README.md'):
            with open('README.md', 'r') as data:
                if data.read() == newdata:
                    click.secho('`README.md` file already up-to-date',
                                fg='yellow')
                else:
                    if click.confirm('The `README.md` file has changes.\n'
                                     'Do you want to replace it?'):
                        update_readme(newdata)
                        click.secho('`README.md` updated',
                                    fg='green')
                    else:
                        click.secho('`README.md` not updated',
                                    fg='red')

        else:
            update_readme(newdata)
            click.secho('`README.md` created',
                        fg='green')

        # Update locale/translation.js
        # TODO

    else:
        click.secho('\nThe collection is not valid :(', fg='red')


def update_readme(data):
    with open('README.md', 'w') as f:
        f.write(data)


def getdocs():
    return '# Collection'


def gettext():
    pass
