from pathlib import Path


def url_to_name(url: str) -> str:
    return url.split(':')[1].split('.git')[0].split('/')[1]


def read_suffix(name: str) -> str:
    return Path(name).suffix.strip('.')


__all__ = ['url_to_name', 'read_suffix']
