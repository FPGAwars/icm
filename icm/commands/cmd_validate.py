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
        valid = _validate_package_file(valid)

    return valid


def _validate_package_file(valid):
    try:
        with open('package.json', 'r') as data:
            package = json.load(data)
            keys = package.keys()
            valid = _check_key('name', keys, valid,
                               lambda x: package[x])
            valid = _check_key('description', keys, valid,
                               lambda x: package[x])
            valid = _check_key('version', keys, valid,
                               lambda x: semantic_version.validate(package[x]))
            valid = _check_key('keywords', keys, valid)
            valid = _check_key('license', keys, valid)

    except Exception as e:
        valid &= False
        click.secho(str(e), fg='red')

    return valid


def _check_key(key, keys, valid, extra_check=lambda x: x):
    if not (key in keys and extra_check(key)):
        valid &= False
        click.secho(
            ' - Error: not valid {} in `package.json`'.format(key),
            fg='yellow')
    return valid
