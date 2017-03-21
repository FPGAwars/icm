# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import os
import json
import click

from string import Template

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
            if f.read() == data.encode('utf8'):
                click.secho('`{}` file already up-to-date'.format(dest),
                            fg='yellow')
            else:
                if click.confirm('The `{}` file has changes.\n'
                                 'Do you want to replace it?'.format(dest)):
                    with open(dest, 'w') as f:
                        f.write(data.encode('utf8'))
                    click.secho('`{}` updated'.format(dest),
                                fg='green')
                else:
                    click.secho('`{}` not updated'.format(dest),
                                fg='red')
    else:
        path = os.path.dirname(dest)
        if not os.path.exists(path):
            os.mkdir(path)
        with open(dest, 'w', ) as f:
            f.write(data.encode('utf8'))
        click.secho('`{}` created'.format(dest),
                    fg='green')


def getdocs():
    data = ''
    readme_template = os.path.join(
        os.path.dirname(__file__), '..', 'resources', 'README.tpl.md')

    with open('package.json', 'r') as p:
        package = json.loads(p.read().decode('utf-8'))

        with open(readme_template, 'r') as f:
            template = Template(f.read())

            # Create the link
            link = ''
            if package.get('repository') and package['repository'].get('url'):
                url = package['repository']['url']
                version = package['version']
                link = '[collection]('
                link += url
                link += '/archive/v'
                link += version
                link += '.zip)'
            else:
                link = 'collection'

            # Create the Blocks section
            blocks_section = ''
            blocks = list_recursive_files('blocks')
            if blocks:
                blocks_section = '## Blocks\n'
                blocks_section += blocks

            # Create the Examples section
            examples_section = ''
            examples = list_recursive_files('examples')
            if examples:
                examples_section = '## Examples\n'
                examples_section += examples

            # Create the Languages section
            languages_section = ''
            # TODO

            # Create the Authors section
            authors_section = ''
            authors = package.get('authors')
            if authors and type(authors) is list:
                authors_section = '## Authors\n'
                for author in authors:
                    if author.get('name'):
                        if author.get('url'):
                            authors_section += '* [' + author['name']
                            authors_section += '](' + author['url']
                            authors_section += ')\n'
                        else:
                            authors_section += '* ' + author['name']
                            authors_section += '\n'

            # Create the Contributors section
            contributors_section = ''
            contributors = package.get('contributors')
            if contributors and type(contributors) is list:
                contributors_section = '## Contributors\n'
                for contributor in contributors:
                    if contributor.get('name'):
                        if contributor.get('url'):
                            contributors_section += '* [' + contributor['name']
                            contributors_section += '](' + contributor['url']
                            contributors_section += ')\n'
                        else:
                            contributors_section += '* ' + contributor['name']
                            contributors_section += '\n'

            # Substitute the template
            data = template.safe_substitute(
                name=package['name'],
                version=package['version'],
                description=package['description'],
                license=package.get('license'),
                link=link,
                blocks=blocks_section,
                examples=examples_section,
                languages=languages_section,
                authors=authors_section,
                contributors=contributors_section)

    return data


def list_recursive_files(path, ext='.ice'):
    tree = ''
    init = True
    for root, dirs, files in os.walk(path):
        path = root.split(os.sep)
        n = len(path)
        if init:
            init = False
        else:
            tree += item_list(os.path.basename(root), n-2)
        for f in files:
            if f.endswith(ext):
                tree += item_list(os.path.splitext(f)[0], n-1)
    return tree


def item_list(text, index=0):
    return index * '  ' + '* ' + text + '\n'


def gettext():
    return '// Translation document of the collection'
