"""Install command"""

import zipfile
import os
from typing import NamedTuple
from pathlib import Path

import requests
from tqdm import tqdm
from icm.commons import commons


class Collection(NamedTuple):
    """Manage collections"""

    #   Oficial icestudio Collection are zip files downloaded
    #   from https://github.com/FPGAwars/

    #   There are two types or URL:

    #   * Dev URL:  Latest version in the main branch
    #     https://github.com/FPGAwars/iceK/archive/refs/heads/main.zip

    #   * Version URL:  Specific stable version
    #     https://github.com/FPGAwars/iceK/archive/refs/tags/v0.1.4.zip

    GITHUB_FPGAWARS = "https://github.com/FPGAwars/"
    GITHUB_PREFIX = "/archive/refs/"
    GITHUB_TYPE_DEV = "heads/"
    GITHUB_TYPE_VER = "tags/"

    def filename(self, version="") -> str:
        """Return the coleccion filename, according to its version
         No Path. No url. Just the .zip filename

        * No version given --> assume dev collection. filename = "main.zip"
        * version given --> filename = "v{version}.zip"

        Ex. col.filename("0.1.4) --> "v0.1.4.zip"
        """

        # -- Filename for the dev collection
        name_dev = "main.zip"

        # -- Filename for the version (stable) collection
        name_ver = f"v{version}.zip"

        # -- Return the name according to the version type
        return name_ver if version else name_dev

    def abs_filename(self, folders: commons.Folders, version="") -> Path:
        """Return the absolute path of the collection target filename
        ex: /home/obijuan/.icestudio/collections/v0.1.4.zip
        """
        abs_file = folders.collections / self.filename(version)
        return abs_file

    def url(self, name: str, version="") -> str:
        """Return the url of the given collection
        * name: Collection name (Ex. "iceK")
        * version (optional) (Ex. 0.1.4)

        It return the url as a string
        """

        # -- Get the colection filename
        filename = self.filename(version)

        # -- Get the type string
        github_type = self.GITHUB_TYPE_VER if version else self.GITHUB_TYPE_DEV

        # -- Build the url
        url = (
            f"{self.GITHUB_FPGAWARS}{name}{self.GITHUB_PREFIX}"
            f"{github_type}{filename}"
        )

        # -- Return the url
        return url


# -- Information about collections
icek = {"name": "iceK", "version": "0.1.4"}

# -- Collection filefo
COLLECTION_FILE = "v"


def main():
    """ENTRY POINT: Install collections"""

    # -- Get context information
    folders = commons.Folders()
    colection = Collection()

    print()
    print("Install!!!\n")

    abs_filename = colection.abs_filename(folders, icek["version"])
    print(f"* File: {abs_filename}")

    url = colection.url(icek["name"], icek["version"])
    print(f"* Url: {url}")

    # -- Download the collection
    # Realizar la solicitud HTTP para obtener el contenido del archivo
    response = requests.get(url, stream=True, timeout=10)

    # Verificar que la solicitud se completó correctamente
    if response.status_code == 200:

        # Obtener el tamaño total del archivo desde los headers
        total_size = int(response.headers.get("content-length", 0))

        # Abrir un archivo local con el nombre especificado en
        # modo escritura binaria
        with open(abs_filename, "wb") as file:

            # Crear una barra de progreso con tqdm
            with tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                desc="  Downloading",
            ) as pbar:
                # Iterar sobre el contenido en bloques
                for chunk in response.iter_content(chunk_size=1024):
                    # Filtrar bloques vacíos
                    if chunk:
                        # Escribir el contenido del bloque en el archivo local
                        file.write(chunk)
                        # Actualizar la barra de progreso
                        pbar.update(len(chunk))

        # shutil.copyfileobj(response.raw, file)
    else:
        print(
            f"Error al descargar el archivo. "
            f"Código de estado: {response.status_code}"
        )

    # -- Uncompress the collection

    # Nombre del archivo ZIP
    zip_filename = abs_filename

    # Directorio de destino para descomprimir los archivos
    extract_to = folders.collections

    # Abrir el archivo ZIP y extraer su contenido con barra de progreso
    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        # Obtener la lista de archivos en el archivo ZIP
        file_list = zip_ref.namelist()

        # Crear una barra de progreso
        with tqdm(
            total=len(file_list), desc="  Uncompressing", unit="file"
        ) as pbar:
            # Iterar sobre cada archivo en el archivo ZIP
            for file in file_list:
                # Extraer cada archivo
                zip_ref.extract(file, extract_to)
                # Actualizar la barra de progreso
                pbar.update(1)

    # -- Borrar el archivo zip
    os.remove(zip_filename)
