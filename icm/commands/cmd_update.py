# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import os
import re
import sys
import json
import click
import polib

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
    if sys.version_info < (3, 0):
        data = data.encode('utf-8')
    if os.path.exists(dest):
        with open(dest, 'r') as f:
            if f.read() == data:
                click.secho('`{}` file already updated'.format(dest),
                            fg='yellow')
            else:
                if click.confirm('The `{}` file has changes.\n'
                                 'Do you want to replace it?'.format(dest)):
                    with open(dest, 'w', ) as f:
                        f.write(data)
                    click.secho('`{}` updated'.format(dest),
                                fg='green')
                else:
                    click.secho('`{}` not updated'.format(dest),
                                fg='red')
    else:
        path = os.path.dirname(dest)
        if path and not os.path.exists(path):
            os.mkdir(path)
        with open(dest, 'w', ) as f:
            f.write(data)
        click.secho('`{}` created'.format(dest),
                    fg='green')


def getdocs():
    data = ''
    readme_template = os.path.join(
        os.path.dirname(__file__), '..', 'resources', 'README.tpl.md')

    with open('package.json', 'r') as p:
        package = json.load(p)

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
            languages = list_languages('locale')
            if languages:
                languages_section = '## Languages\n'
                languages_section += languages

            # Create the Authors section
            authors_section = ''
            authors = package.get('authors')
            if authors and type(authors) is list:
                authors_section = '## Authors\n'
                for author in authors:
                    name = author.get('name')
                    url = author.get('url')
                    if name:
                        if url:
                            authors_section += '* [' + name
                            authors_section += '](' + url
                            authors_section += ')\n'
                        else:
                            authors_section += '* ' + name
                            authors_section += '\n'

            # Create the Contributors section
            contributors_section = ''
            contributors = package.get('contributors')
            if contributors and type(contributors) is list:
                contributors_section = '## Contributors\n'
                for contributor in contributors:
                    name = contributor.get('name')
                    url = contributor.get('url')
                    if name:
                        if url:
                            contributors_section += '* [' + name
                            contributors_section += '](' + url
                            contributors_section += ')\n'
                        else:
                            contributors_section += '* ' + name
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
    data = ''
    init = True
    for root, dirs, files in sorted(os.walk(path)):
        path = root.split(os.sep)
        n = len(path)
        if init:
            init = False
        else:
            data += item_list(os.path.basename(root), n-2)
        for f in sorted(files):
            if f.endswith(ext):
                data += item_list(os.path.splitext(f)[0], n-1)
    return data


def item_list(text, index=0):
    return index * '  ' + '* ' + text + '\n'


def list_languages(path):
    data = ''
    languages = []
    for lang in os.listdir(path):
        langpath = os.path.join(path, lang, lang + '.po')
        if os.path.isfile(langpath):
            po = polib.pofile(langpath)
            languages.append({
                'lang': lang,
                'progress': po.percent_translated()
            })
    languages = sorted(languages)
    data = '| Language | Translated strings |\n'
    data += '|:--------:|:------------------:|\n'
    for language in languages:
        data += '| ' + language['lang'] + ' | '
        data += '![Progress](http://progressed.io/bar/'
        data += str(language['progress']) + ') |\n'
    return data


PATTERN_DESC = '"description":\s*"(.*?)"'
PATTERN_INFO = '"info":\s*"(.*?)"'


def gettext():
    data = ''
    readme_template = os.path.join(
        os.path.dirname(__file__), '..', 'resources', 'translation.tpl.js')

    with open(readme_template, 'r') as f:
        translations = []
        template = Template(f.read())

        # Read blocks
        find_texts('blocks', translations)

        # Read examples
        find_texts('examples', translations)

        # Add gettext function
        translations = ['gettext(\'' + t + '\');' for t in translations]

        # Substitute the template
        data = template.safe_substitute(
            translations='\n'.join(translations))
    return data


def find_texts(path, translations, ext='.ice'):
    for root, dirs, files in sorted(os.walk(path)):
        for d in sorted(dirs):
            # - Append directories
            translations.append(d)
        for f in sorted(files):
            if f.endswith(ext):
                # - Append files
                translations.append(os.path.splitext(f)[0])
                filepath = os.path.join(root, f)
                with open(filepath, 'r') as p:
                    project = p.read()
                    # - Append descriptions
                    p = re.compile(PATTERN_DESC)
                    descriptions = p.findall(project)
                    for description in descriptions:
                        if description and description not in translations:
                            translations.append(description)
                    # - Append basic.info blocks
                    p = re.compile(PATTERN_INFO)
                    infos = p.findall(project)
                    for info in infos:
                        if info and info not in translations:
                            translations.append(info)
