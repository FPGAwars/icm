"""Update command"""
# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import os
import re
import json

from string import Template
import click
import polib


from icm.commands.cmd_validate import validate_collection

# -- Repo default branch. This value is used when the package.json
# -- has not the "branch" field in it
DEFAULT_BRANCH = "main"


def update():
    """ENTRY POINT: Update docs and translation."""

    click.secho("Update the collection", fg="cyan")

    if validate_collection():

        # Read The contents from the package.json file
        # and generate a formated string
        contents = _generate_readme_string()

        # Update README.md (or create a new one if it does not exist)
        _update_file("README.md", contents)

        # Update locale/translation.js
        _update_file("locale/translation.js", _gettext())
    else:
        click.secho("\nThe collection is not valid :(", fg="red")


def _update_file(dest, data):
    """Update the destination file with the data.
    If the file does not exists it is created"""

    # Check if the file exist
    if os.path.exists(dest):

        # Update it!
        _update_existing_file(dest, data)
    else:

        # Create a new one
        _create_new_file(dest, data)


def _update_existing_file(dest, data):
    """Update the dest file with the given data"""

    with open(dest, "r") as file:

        # Read the current data from the fiel and check
        # if it is equal or not to the given data
        if file.read() == data:
            click.secho(
                " - `{}` file already updated".format(dest), fg="yellow"
            )
        # -- The file is outdated
        else:
            if click.confirm(
                "The `{}` file has changes.\n"
                "Do you want to replace it?".format(dest)
            ):
                with open(dest, "w") as file:
                    file.write(data)
                click.secho(" - `{}` file updated".format(dest), fg="green")
            else:
                click.secho(" - `{}` file not updated".format(dest), fg="red")


def _create_new_file(dest, data):
    path = os.path.dirname(dest)
    if path and not os.path.exists(path):
        os.mkdir(path)
    with open(
        dest,
        "w",
    ) as file:
        file.write(data)
    click.secho(" - `{}` file created".format(dest), fg="green")


def _generate_readme_string():
    """Generate the data for the README file from the TEMPLATE file
    The information is read from the package.json file
    It returns a string with the final readme file.
    TEMPLATE file: resources/README.tpl.md"""

    data = ""
    readme_template = os.path.join(
        os.path.dirname(__file__), "..", "resources", "README.tpl.md"
    )

    with open("package.json", "r") as pack:
        package = json.load(pack)

        with open(readme_template, "r") as file:

            # Read the template content
            template = Template(file.read())

            # Substitute the template variables with the data generated
            # from the package.json information
            data = template.safe_substitute(
                name=package["name"],
                version=package["version"].replace("-", "--"),
                description=package["description"],
                license=package.get("license"),
                # -- Add the logo image
                logo=_create_logo(package),
                # -- Add the wiki section
                wiki=_create_wiki(package),
                # -- Create the download link section
                links=_create_links(package),
                # -- Show all the blocks in the collection
                blocks=_create_blocks_section(),
                # -- Show all the examples in the collection
                examples=_create_examples_section(),
                # -- others
                languages=_create_languages_section(),
                authors=_create_authors_section(package),
                contributors=_create_contributor_section(package),
            )

    return data


def _create_wiki(package):
    """README: create the wiki section"""

    data = ""

    # -- Get the wiki URL
    if package.get("wiki"):
        url = package["wiki"]
        data += "## Documentation\n"
        data += "Find more information in the "
        data += f"[WIKI page]({url})  \n"

    return data


def _create_logo(package):
    """README: create the markdown string with the logo"""

    data = ""

    # -- Get the logo
    if package.get("logo"):
        file = package["logo"]
        data += f"![]({file})\n"

    return data


def _create_links(package):
    """README: creates string with the Stable and development URLs
    The data is got from the package structure (form the package.json)
    """

    links = ""

    # It is only done if there is a field `repository` with a fiel "url" inside
    if package.get("repository") and package["repository"].get("url"):
        url = package["repository"]["url"]
        branch = package["repository"].get("branch", DEFAULT_BRANCH)
        version = package["version"]
        stable = "[stable](" + url + "/archive/refs/tags/v" + version + ".zip)"
        dev = (
            "[development](" + url + "/archive/refs/heads/" + branch + ".zip)"
        )
        links = ": " + stable + " or " + dev
    return links


def _create_blocks_section():
    blocks_section = ""
    blocks = _list_recursive_files("blocks")
    if blocks:
        blocks_section = "## Blocks\n"
        blocks_section += blocks
    return blocks_section


def _create_examples_section():
    """Read the examples directoy of the collection and create
    the markdown documentation"""

    examples_section = ""

    # Get all the files in the examples directory (recursivelly)
    examples = _list_recursive_files("examples")

    # If there are no examples, this section is
    # not added to the README file
    if examples:
        examples_section = "## Examples\n"
        examples_section += examples

    return examples_section


def _list_recursive_files(path, ext=".ice"):
    """Get a string with all the icestudio example files in the
    given folder (recursivelly)"""

    data = ""
    for root, dirs, files in sorted(os.walk(path)):

        # -- root contains the path to the current file
        # -- It is split into its components to determine its depth
        path = root.split(os.sep)
        depth = len(path)

        # -- Insert only the elements with depth > 1
        # -- A depth = 1 means the block or example root folder
        if depth > 1:

            # -- Indentation spaces (depending on the depth)
            indent = "  " * (depth - 2)

            # -- Item name in bold (markdown)
            folder_name = f"* **{os.path.basename(root)}**"

            # -- Include the folder in the string
            # -- Ignore the ice-build folder!
            if "ice-build" not in path:
                data += indent + folder_name + "\n"

                # -- Debug!
                # print(f"{indent}{folder_name}")

        # -- Add the .ice files to the output string
        for file in sorted(files):

            # -- Only '.ice' files are included
            if file.endswith(ext):

                # -- Indentation
                indent = "  " * (depth - 1)

                # -- Get the file name
                example_name = f"* {os.path.splitext(file)[0]}"

                # -- The files inside an ice-build folder are ignored
                if "ice-build" not in path:
                    data += indent + example_name + "\n"

                    # -- Debug!
                    # print(f"{indent}{example_name}.ice")

    return data


def _create_languages_section():
    languages_section = ""
    languages = _list_languages("locale")
    if languages:
        languages_section = "## Translations\n"
        languages_section += languages
    return languages_section


def _list_languages(path):
    data = ""
    languages = []
    for lang in os.listdir(path):
        langpath = os.path.join(path, lang, lang + ".po")
        if os.path.isfile(langpath):
            pofile = polib.pofile(langpath)
            if len(pofile.translated_entries()) > 0:
                languages.append((lang, pofile.percent_translated()))
    languages = sorted(languages)
    if languages:
        data = "| Language | Translated strings |\n"
        data += "|:--------:|:------------------:|\n"
        for language in languages:
            data += "| " + language[0] + " | "
            data += "![](https://progress-bar.dev/" + str(language[1]) + ")"
            data += " |\n"
    return data


def _create_authors_section(package):
    authors_section = ""
    authors = package.get("authors")
    default_authors = [{"name": "", "email": "", "url": ""}]
    if authors and isinstance(authors, list) and authors != default_authors:
        authors_section = "## Authors\n"
        for author in authors:
            name = author.get("name")
            url = author.get("url")
            if name:
                if url:
                    authors_section += "* [" + name
                    authors_section += "](" + url
                    authors_section += ")\n"
                else:
                    authors_section += "* " + name
                    authors_section += "\n"
    return authors_section


def _create_contributor_section(package):
    contributors_section = ""
    contributors = package.get("contributors")
    if contributors and isinstance(contributors, list):
        contributors_section = "## Contributors\n"
        for contributor in contributors:
            name = contributor.get("name")
            url = contributor.get("url")
            if name:
                if url:
                    contributors_section += "* [" + name
                    contributors_section += "](" + url
                    contributors_section += ")\n"
                else:
                    contributors_section += "* " + name
                    contributors_section += "\n"
    return contributors_section


def _gettext():
    data = ""
    readme_template = os.path.join(
        os.path.dirname(__file__), "..", "resources", "translation.tpl.js"
    )

    with open(readme_template, "r") as file:
        translations = []
        template = Template(file.read())

        # Read blocks
        _find_texts("blocks", translations)

        # Read examples
        _find_texts("examples", translations)

        # Add gettext function
        translations = ["gettext('" + t + "');" for t in translations]

        # Substitute the template
        data = template.safe_substitute(translations="\n".join(translations))
    return data


def _find_texts(path, translations, ext=".ice"):
    """Find all texts for translation"""
    for root, dirs, files in sorted(os.walk(path)):
        for directory in sorted(dirs):
            # Append directories if diferent thant ice-build
            if directory != "ice-build":
                translations.append(directory)

                # -- Debug
                # -- print(f"{directory}")

        for file in sorted(files):

            # Discard the files inside the ice-build folders
            if root.find("ice-build") == -1:

                # -- Only files with the given extension
                if file.endswith(ext):

                    # Append files
                    translations.append(os.path.splitext(file)[0])
                    filepath = os.path.join(root, file)
                    _find_texts_in_file(filepath, translations)

                    # Debug
                    # print(file)


PATTERN_DESC = r'"description":\s*"(.*?)"'
PATTERN_INFO = r'"info":\s*"(.*?)",[\n|\s]*"readonly": true'


def _find_texts_in_file(filepath, translations):
    with open(filepath, "r") as path:
        project = path.read()
        # Append descriptions
        path = re.compile(PATTERN_DESC)
        descriptions = path.findall(project)
        for description in descriptions:
            if description and description not in translations:
                translations.append(description)
        # Append basic.info blocks
        path = re.compile(PATTERN_INFO)
        infos = path.findall(project)
        for info in infos:
            if info and info not in translations:
                translations.append(info)
