"""info command"""

# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017-19 FPGAwars
# --   Author Jesús Arroyo
# -- (C) 2020-24 FPGAwars
# --   Author Juan Gonzalez (Obijuan)
# -- Licence GPLv2

import platform
import shutil

# -- Terminal width
TERMINAL_WIDTH = shutil.get_terminal_size().columns

# -- Horizontal line
HLINE = "─" * TERMINAL_WIDTH


def main():
    """ENTRY POINT: Show system information"""

    print()
    print("----------------")
    print("icm info")
    print("----------------")
    print("")

    print(HLINE)
    print(platform.uname())
    print(HLINE)
