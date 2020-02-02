from .process import process
from pathlib import Path


def build_parser():
    pass


def main():
    here = Path(__file__).parent
    manifest_path = here / 'terraform.json'
    process(manifest_path)
