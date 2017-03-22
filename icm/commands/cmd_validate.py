# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

# Validate a collection:
#
# - Required: blocks | examples
# - Required: package.json
#              - name
#              - (semantic) version
#              - description

import os
import json
import click
import semantic_version


def validate():
    """Validate a collection."""

    click.secho('Validate the collection', fg='cyan')

    if validate_collection():
        click.secho('\nThe collection is valid :)', fg='green')
    else:
        click.secho('\nThe collection is not valid :(', fg='red')


def validate_collection():
    valid = True

    if not (os.path.isdir('blocks') or os.path.isdir('examples')):
        valid &= False
        click.secho(
            ' - Error: no directory `blocks` or `examples` found',
            fg='yellow')

    if not os.path.isfile('package.json'):
        valid &= False
        click.secho(' - Error: no file `package.json` found', fg='yellow')
    else:
        try:
            with open('package.json', 'r') as data:
                package = json.load(data)
                keys = package.keys()
                if not ('name' in keys and package['name']):
                    valid &= False
                    click.secho(
                        ' - Error: not valid name in `package.json`',
                        fg='yellow')

                if not ('version' in keys and
                   semantic_version.validate(package['version'])):
                    valid &= False
                    click.secho(
                        ' - Error: not valid version in `package.json`',
                        fg='yellow')

                if not ('description' in keys and package['description']):
                    valid &= False
                    click.secho(
                        ' - Error: not valid description in `package.json`',
                        fg='yellow')

                if not ('keywords' in keys):
                    valid &= False
                    click.secho(
                        ' - Error: not valid keywords in `package.json`',
                        fg='yellow')

                if not ('license' in keys):
                    valid &= False
                    click.secho(
                        ' - Error: not valid license in `package.json`',
                        fg='yellow')

        except Exception as e:
            valid &= False
            click.secho(str(e), fg='red')

    return valid
