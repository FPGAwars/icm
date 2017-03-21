# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

# Collection structure:
#
# - blocks
# - examples
# - locale
# - LICENSE
# - package.json
# - README.md

import os
import click


def create():
    """Create a collection structure."""

    click.secho('Create a collection structure', fg='cyan')

    # Create blocks directory
    create_directory('blocks')

    # Create examples directory
    create_directory('examples')

    # Create locale directory
    create_directory('locale')

    # Create LICENSE file
    local_license = os.path.join(
        os.path.dirname(__file__), '..', 'resources', 'GPL-2.0')
    with open(local_license, 'r') as f:
        license = f.read()
        create_file('LICENSE', license)

    # Create package.json file
    package = """\
{
  "name": "MyCollection",
  "version": "0.1.0",
  "description": "Awesome collection",
  "keywords": "",
  "license": "GPL-2.0",
  "authors": [{
    "name": "",
    "email": "",
    "url": ""
  }],
  "contributors": [],
  "repository": {
    "type": "git",
    "url": ""
  }
}
"""
    create_file('package.json', package)

    # Create README.md file
    create_file(
        'README.md',
        '## MyCollection\nUpdate this file using `icm update`')


def create_directory(name):
    if not os.path.exists(name):
        os.makedirs(name)
        click.secho(' - `{}` directory created'.format(name),
                    fg='green')
    else:
        click.secho(' - `{}` directory already exists'.format(name),
                    fg='yellow')


def create_file(name, content):
    if not os.path.exists(name):
        with open(name, 'w') as f:
            f.write(content)
            click.secho(' - `{}` file created'.format(name),
                        fg='green')
    else:
        click.secho(' - `{}` file already exists'.format(name),
                    fg='yellow')
