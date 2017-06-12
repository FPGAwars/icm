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
        _update_file('README.md', _getdocs())
        # Update locale/translation.js
        _update_file('locale/translation.js', _gettext())
    else:
        click.secho('\nThe collection is not valid :(', fg='red')


def _update_file(dest, data):
    if sys.version_info < (3, 0):
        try:
            data = data.encode('utf-8')
        except Exception:
            pass
    if os.path.exists(dest):
        _update_existing_file(dest, data)
    else:
        _create_new_file(dest, data)


def _update_existing_file(dest, data):
    with open(dest, 'r') as f:
        if f.read() == data:
            click.secho(' - `{}` file already updated'.format(dest),
                        fg='yellow')
        else:
            if click.confirm('The `{}` file has changes.\n'
                             'Do you want to replace it?'.format(dest)):
                with open(dest, 'w', ) as f:
                    f.write(data)
                click.secho(' - `{}` file updated'.format(dest),
                            fg='green')
            else:
                click.secho(' - `{}` file not updated'.format(dest),
                            fg='red')


def _create_new_file(dest, data):
    path = os.path.dirname(dest)
    if path and not os.path.exists(path):
        os.mkdir(path)
    with open(dest, 'w', ) as f:
        f.write(data)
    click.secho(' - `{}` file created'.format(dest),
                fg='green')


def _getdocs():
    data = ''
    readme_template = os.path.join(
        os.path.dirname(__file__), '..', 'resources', 'README.tpl.md')

    with open('package.json', 'r') as p:
        package = json.load(p)

        with open(readme_template, 'r') as f:
            template = Template(f.read())

            # Substitute the template
            data = template.safe_substitute(
                name=package['name'],
                version=package['version'].replace('-', '--'),
                description=package['description'],
                license=package.get('license'),
                links=_create_links(package),
                blocks=_create_blocks_section(),
                examples=_create_examples_section(),
                languages=_create_languages_section(),
                authors=_create_authors_section(package),
                contributors=_create_contributor_section(package))

    return data


def _create_links(package):
    links = ''
    if package.get('repository') and package['repository'].get('url'):
        url = package['repository']['url']
        branch = package['repository'].get('branch', 'master')
        version = package['version']
        stable = '[stable](' + url + '/archive/v' + version + '.zip)'
        dev = '[development](' + url + '/archive/' + branch + '.zip)'
        links = ': ' + stable + ' or ' + dev
    return links


def _create_blocks_section():
    blocks_section = ''
    blocks = _list_recursive_files('blocks')
    if blocks:
        blocks_section = '## Blocks\n'
        blocks_section += blocks
    return blocks_section


def _create_examples_section():
    examples_section = ''
    examples = _list_recursive_files('examples')
    if examples:
        examples_section = '## Examples\n'
        examples_section += examples
    return examples_section


def _list_recursive_files(path, ext='.ice'):
    data = ''
    init = True
    for root, dirs, files in sorted(os.walk(path)):
        path = root.split(os.sep)
        n = len(path)
        if init:
            init = False
        else:
            data += _item_list('*' + os.path.basename(root) + '*', n-2)
        for f in sorted(files):
            if f.endswith(ext):
                data += _item_list(os.path.splitext(f)[0], n-1)
    return data


def _item_list(text, index=0):
    text = re.sub(r'\.', '\.', text)
    return index * '  ' + '* ' + text + '\n'


def _create_languages_section():
    languages_section = ''
    languages = _list_languages('locale')
    if languages:
        languages_section = '## Languages\n'
        languages_section += languages
    return languages_section


def _list_languages(path):
    data = ''
    languages = []
    for lang in os.listdir(path):
        langpath = os.path.join(path, lang, lang + '.po')
        if os.path.isfile(langpath):
            po = polib.pofile(langpath)
            if len(po.translated_entries()) > 0:
                languages.append((lang, po.percent_translated()))
    languages = sorted(languages)
    if languages:
        data = '| Language | Translated strings |\n'
        data += '|:--------:|:------------------:|\n'
        for language in languages:
            data += '| ' + language[0] + ' | '
            data += '![Progress](http://progressed.io/bar/'
            data += str(language[1]) + ') |\n'
    return data


def _create_authors_section(package):
    authors_section = ''
    authors = package.get('authors')
    default_authors = [{"name": "", "email": "", "url": ""}]
    if authors and type(authors) is list and authors != default_authors:
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
    return authors_section


def _create_contributor_section(package):
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
    return contributors_section


def _gettext():
    data = ''
    readme_template = os.path.join(
        os.path.dirname(__file__), '..', 'resources', 'translation.tpl.js')

    with open(readme_template, 'r') as f:
        translations = []
        template = Template(f.read())

        # Read blocks
        _find_texts('blocks', translations)

        # Read examples
        _find_texts('examples', translations)

        # Add gettext function
        translations = ['gettext(\'' + t + '\');' for t in translations]

        # Substitute the template
        data = template.safe_substitute(
            translations='\n'.join(translations))
    return data


def _find_texts(path, translations, ext='.ice'):
    """Find all texts for translation"""
    for root, dirs, files in sorted(os.walk(path)):
        for d in sorted(dirs):
            # Append directories
            translations.append(d)
        for f in sorted(files):
            if f.endswith(ext):
                # Append files
                translations.append(os.path.splitext(f)[0])
                filepath = os.path.join(root, f)
                _find_texts_in_file(filepath, translations)


PATTERN_DESC = '"description":\s*"(.*?)"'
PATTERN_INFO = '"info":\s*"(.*?)",[\n|\s]*"readonly": true'


def _find_texts_in_file(filepath, translations):
    with open(filepath, 'r') as p:
        project = p.read()
        # Append descriptions
        p = re.compile(PATTERN_DESC)
        descriptions = p.findall(project)
        for description in descriptions:
            if description and description not in translations:
                translations.append(description)
        # Append basic.info blocks
        p = re.compile(PATTERN_INFO)
        infos = p.findall(project)
        for info in infos:
            if info and info not in translations:
                translations.append(info)
