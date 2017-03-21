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
        update_file('README.md', getdocs())
        # Update locale/translation.js
        update_file('locale/translation.js', gettext())
    else:
        click.secho('\nThe collection is not valid :(', fg='red')


def update_file(dest, data):
    if os.path.exists(dest):
        with open(dest, 'r') as f:
            if f.read() == data:
                click.secho('`{}` file already up-to-date'.format(dest),
                            fg='yellow')
            else:
                if click.confirm('The `{}` file has changes.\n'
                                 'Do you want to replace it?'.format(dest)):
                    with open(dest, 'w') as f:
                        f.write(data)
                    click.secho('`{}` updated'.format(dest),
                                fg='green')
                else:
                    click.secho('`{}` not updated'.format(dest),
                                fg='red')
    else:
        path = os.path.dirname(dest)
        if not os.path.exists(path):
            os.mkdir(path)
        with open(dest, 'w') as f:
            f.write(data)
        click.secho('`{}` created'.format(dest),
                    fg='green')


def getdocs():
    return '# Collection'


def gettext():
    return '// Translation document of the collection'
