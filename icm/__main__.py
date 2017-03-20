# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import click

from sys import exit as sys_exit


@click.group()
@click.version_option()
def cli():
    pass
