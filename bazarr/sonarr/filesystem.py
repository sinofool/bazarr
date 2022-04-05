# coding=utf-8

import os
import requests
import logging

from bazarr.config import settings, url_sonarr
from bazarr.sonarr.info import get_sonarr_info

headers = {"User-Agent": os.environ["SZ_USER_AGENT"]}


def browse_sonarr_filesystem(path='#'):
    if path == '#':
        path = ''
    if get_sonarr_info.is_legacy():
        url_sonarr_api_filesystem = url_sonarr() + "/api/filesystem?path=" + path + \
                                    "&allowFoldersWithoutTrailingSlashes=true&includeFiles=false&apikey=" + \
                                    settings.sonarr.apikey
    else:
        url_sonarr_api_filesystem = url_sonarr() + "/api/v3/filesystem?path=" + path + \
                                    "&allowFoldersWithoutTrailingSlashes=true&includeFiles=false&apikey=" + \
                                    settings.sonarr.apikey
    try:
        r = requests.get(url_sonarr_api_filesystem, timeout=60, verify=False, headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        logging.exception("BAZARR Error trying to get series from Sonarr. Http error.")
        return
    except requests.exceptions.ConnectionError:
        logging.exception("BAZARR Error trying to get series from Sonarr. Connection Error.")
        return
    except requests.exceptions.Timeout:
        logging.exception("BAZARR Error trying to get series from Sonarr. Timeout Error.")
        return
    except requests.exceptions.RequestException:
        logging.exception("BAZARR Error trying to get series from Sonarr.")
        return

    return r.json()