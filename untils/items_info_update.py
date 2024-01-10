import requests
from io import BytesIO
from zipfile import ZipFile

import shutil

url = 'https://codeload.github.com/42bytes-team/wfm-items/zip/refs/heads/master'
extract_to = './temple'


def items_download():
    try:
        shutil.rmtree(f'{extract_to}/wfm-items-master')
    except:
        pass
    download_and_unzip()
    return 'completed'


def download_and_unzip():
    http_response = requests.get(url)
    zipfile = ZipFile(BytesIO(http_response.content))

    for file in zipfile.namelist():
        if file.startswith('wfm-items-master/tracked/'):
            zipfile.extract(file, path=extract_to)
