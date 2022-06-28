import logging

from custom_typing import T_URLS


def get_target_sites_from_file(file_path: str) -> T_URLS:
    with open(file_path, 'r') as file:
        target_sites = []
        for site in file.readlines():
            target_sites.append(site.strip())
        return target_sites
