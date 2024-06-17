"""Install command"""

import zipfile
import os
import requests
from tqdm import tqdm
from icm.commons import commons

# -- Information about collections
icek = {"name": "iceK", "version": "0.1.4"}

# -- Collection file
COLLECTION_FILE = "v"

# -- Template URL
# -- Full collection download url: PREFIX + NAME + SUFFIX + FILE
TEMPLATE_URL_PREFIX = "https://github.com/FPGAwars/"
TEMPLATE_URL_SUFFIX = "/archive/refs/tags/"


def main():
    """ENTRY POINT: Install collections"""

    # -- Get context information
    folders = commons.Folders()

    print("Install!!!")

    # --- Scafold for the installation of collections
    # -- Download url:
    #   https://github.com/FPGAwars/iceK/archive/refs/tags/v0.1.4.zip
    # -- Build the collection filename
    filename = f"v{icek['version']}.zip"
    print(f"Colection file: {filename}")

    absolut_filename = f"{folders.collections}/{filename}"
    print(f"Absolut filename: {absolut_filename}")

    url = f"{TEMPLATE_URL_PREFIX}{icek['name']}{TEMPLATE_URL_SUFFIX}{filename}"
    print(f"Url: {url}")

    # -- Download the collection
    # Realizar la solicitud HTTP para obtener el contenido del archivo
    response = requests.get(url, stream=True, timeout=10)

    # Verificar que la solicitud se completó correctamente
    if response.status_code == 200:

        # Obtener el tamaño total del archivo desde los headers
        total_size = int(response.headers.get("content-length", 0))

        # Abrir un archivo local con el nombre especificado en
        # modo escritura binaria
        with open(absolut_filename, "wb") as file:

            # Crear una barra de progreso con tqdm
            with tqdm(
                total=total_size, unit="B", unit_scale=True, desc=filename
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
        print(f"Archivo descargado y guardado como {filename}")
    else:
        print(
            f"Error al descargar el archivo. "
            f"Código de estado: {response.status_code}"
        )

    # -- Uncompress the collection

    # Nombre del archivo ZIP
    zip_filename = absolut_filename

    # Directorio de destino para descomprimir los archivos
    extract_to = folders.collections

    # Abrir el archivo ZIP y extraer su contenido con barra de progreso
    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        # Obtener la lista de archivos en el archivo ZIP
        file_list = zip_ref.namelist()

        # Crear una barra de progreso
        with tqdm(
            total=len(file_list), desc="Descomprimiendo", unit="file"
        ) as pbar:
            # Iterar sobre cada archivo en el archivo ZIP
            for file in file_list:
                # Extraer cada archivo
                zip_ref.extract(file, extract_to)
                # Actualizar la barra de progreso
                pbar.update(1)

    # -- Borrar el archivo zip
    os.remove(zip_filename)
