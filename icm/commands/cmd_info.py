"""info command"""

# -*- coding: utf-8 -*-
# -- This file is part of the Icestudio project
# -- (C) 2017-19 FPGAwars
# --   Author Jesús Arroyo
# -- (C) 2020-24 FPGAwars
# --   Author Juan Gonzalez (Obijuan)
# -- Licence GPLv2

from pathlib import Path
from tqdm import tqdm
import platform
import shutil
import requests
import zipfile
import os

import click


# -- Terminal width
TERMINAL_WIDTH = shutil.get_terminal_size().columns

# -- Horizontal line
HLINE = "─" * TERMINAL_WIDTH

# -- Home user folder
HOME = Path.home()

# -- Icestudio HOME dir
ICESTUDIO_HOME = HOME / ".icestudio"

# -- Icestudio root for collections
COLLECTIONS = ICESTUDIO_HOME / "collections"

# -- Information about collections
icek = {
    "name": "iceK",
    "version": "0.1.4"
}

# -- Collection file
COLLECTION_FILE = "v"

# -- Template URL
# -- Full collection download url: PREFIX + NAME + SUFFIX + FILE
TEMPLATE_URL_PREFIX = "https://github.com/FPGAwars/"
TEMPLATE_URL_SUFFIX = "/archive/refs/tags/"


# Función para dibujar la barra de progreso
def print_progress_bar(iteration, total, length=50):
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = '#' * filled_length + '-' * (length - filled_length)
    print(f"\r|{bar}| {percent}%", end='')


def main():
    """ENTRY POINT: Show system information"""

    # --------------------------------
    # -- Print System information
    # --------------------------------
    # -- Header
    print()
    click.secho(HLINE, fg="green")
    click.secho("SYSTEM INFORMATION", fg="green")
    click.secho(HLINE, fg="green")

    # -- Read system information
    plat = platform.uname()

    # -- Print it!
    click.echo(click.style("• Processor: ", fg="green") + f"{plat.processor}")
    click.echo(click.style("• System: ", fg="green") + f"{plat.system}")
    click.echo(click.style("• Release: ", fg="green") + f"{plat.release}")
    click.echo(click.style("• Version: ", fg="green") + f"{plat.version}")

    # ----------------------------
    # -- System folders
    # ----------------------------
    # -- Header
    print()
    click.secho(HLINE, fg="yellow")
    click.secho("FOLDERS", fg="yellow")
    click.secho(HLINE, fg="yellow")

    # -- Check if all the folders exist or not
    ok_home = HOME.exists()
    ok_icestudio = ICESTUDIO_HOME.exists()
    ok_collections = COLLECTIONS.exists()

    # -- Choose the correct bullet for the folder
    home_check = "✅ " if ok_home else "❌ "
    icestudio_check = "✅ " if ok_icestudio else "❌ "
    collections_check = "✅ " if ok_collections else "❌ "

    # -- Print the information
    click.echo(home_check + click.style("HOME: ", fg="yellow") + f"{HOME}")
    click.echo(
        icestudio_check
        + click.style("Icestudio: ", fg="yellow")
        + f"{ICESTUDIO_HOME}"
    )
    click.echo(
        collections_check
        + click.style("Collections: ", fg="yellow")
        + f"{COLLECTIONS}"
    )

    print()

    # --- Scafold for the installation of collections
    # -- Download url: https://github.com/FPGAwars/iceK/archive/refs/tags/v0.1.4.zip
    # -- Build the collection filename
    filename = f"v{icek['version']}.zip"
    print(f"Colection file: {filename}")

    absolut_filename = f"{COLLECTIONS}/{filename}"
    print(f"Absolut filename: {absolut_filename}")

    url = f"{TEMPLATE_URL_PREFIX}{icek['name']}{TEMPLATE_URL_SUFFIX}{filename}"
    print(f"Url: {url}")

    # -- Download the collection
    # Realizar la solicitud HTTP para obtener el contenido del archivo
    response = requests.get(url, stream=True)

    # Verificar que la solicitud se completó correctamente
    if response.status_code == 200:

        # Obtener el tamaño total del archivo desde los headers
        total_size = int(response.headers.get('content-length', 0))

        # Abrir un archivo local con el nombre especificado en modo escritura binaria
        with open(absolut_filename, 'wb') as file:

            # Crear una barra de progreso con tqdm
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                # Iterar sobre el contenido en bloques
                for chunk in response.iter_content(chunk_size=1024):
                    # Filtrar bloques vacíos
                    if chunk:
                        # Escribir el contenido del bloque en el archivo local
                        file.write(chunk)
                        # Actualizar la barra de progreso
                        pbar.update(len(chunk))

        # Utilizar shutil.copyfileobj para copiar el contenido del archivo descargado al archivo local
        #shutil.copyfileobj(response.raw, file)
        print(f"Archivo descargado y guardado como {filename}")
    else:
        print(f"Error al descargar el archivo. Código de estado: {response.status_code}")

    # -- Uncompress the collection
    
    # Nombre del archivo ZIP
    zip_filename = absolut_filename

    # Directorio de destino para descomprimir los archivos
    extract_to = COLLECTIONS

    # Abrir el archivo ZIP y extraer su contenido con barra de progreso
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        # Obtener la lista de archivos en el archivo ZIP
        file_list = zip_ref.namelist()
        
        # Crear una barra de progreso
        with tqdm(total=len(file_list), desc='Descomprimiendo', unit='file') as pbar:
            # Iterar sobre cada archivo en el archivo ZIP
            for file in file_list:
                # Extraer cada archivo
                zip_ref.extract(file, extract_to)
                # Actualizar la barra de progreso
                pbar.update(1)

    # -- Borrar el archivo zip
    os.remove(zip_filename)





